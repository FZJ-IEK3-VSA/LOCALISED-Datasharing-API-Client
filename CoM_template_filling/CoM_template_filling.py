import os
import re
import shutil
import time
import xlwings as xw
import pandas as pd
from zoomin_client import client

# =============================================================
# Importing data and SOI metadata
# =============================================================

# Get SOI calculation excel sheet and
# filter on the variables that can actually be filled using DSP data
soi_metadata_df = pd.read_excel(
    os.path.join(
        "..",
        "..",
        "ETHOS.RegionData",
        "data",
        "input",
        "01_raw",
        "variables_with_details_and_tags.xlsx",
    ),
    sheet_name="admin_business_and_social_KPIs",
)

soi_vars_with_dsp_input = soi_metadata_df[
    (~soi_metadata_df["soi_name"].isna())
    & (~soi_metadata_df["calculation"].isin(["BLANK", "TBD"]))
    & (  # some SOIs are decided to be left blank or TBD yet
        soi_metadata_df["data_source"] != "TOTAL"
    )  # some SOIs are sum of other SOIs, the CoM template fills these automatically
][["soi_name", "calculation"]]

# get DSP data for a region
region_code = "DEA23"
region_data = client.get_region_data(
    country_code="de",
    region_code=region_code,
    pathway_description="national",  # National pathway is considered for SOIs
    result_format="df",
)


# temp fix to reflect change in names. Next DSP deploy will have it changed
region_data["var_name"] = region_data["var_name"].replace(
    {
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_liquefied_petroleum_gases": "final_energy_consumption_from_manufacture_of_chemicals_using_liquefied_petroleum_gases",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_gas_oil_and_diesel_oil": "final_energy_consumption_from_manufacture_of_chemicals_using_gas_oil_and_diesel_oil",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_fuel_oil": "final_energy_consumption_from_manufacture_of_chemicals_using_fuel_oil",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_gas_oil_and_diesel_oil": "final_energy_consumption_from_manufacture_of_chemicals_using_gas_oil_and_diesel_oil",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_motor_gasoline": "final_energy_consumption_from_manufacture_of_chemicals_using_motor_gasoline",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_lignite": "final_energy_consumption_from_manufacture_of_chemicals_using_lignite",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_anthracite": "final_energy_consumption_from_manufacture_of_chemicals_using_anthracite",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_coking_coal": "final_energy_consumption_from_manufacture_of_chemicals_using_coking_coal",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_other_bituminous_coal": "final_energy_consumption_from_manufacture_of_chemicals_using_other_bituminous_coal",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_sub_bituminous_coal": "final_energy_consumption_from_manufacture_of_chemicals_using_sub_bituminous_coal",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_solar_thermal": "final_energy_consumption_from_manufacture_of_chemicals_using_solar_thermal",
        "final_energy_consumption_from_manufacture_of_chemical_and_chemical_products_using_geothermal": "final_energy_consumption_from_manufacture_of_chemicals_using_geothermal",
    }
)

# =============================================================
# Calculating SOI values
# =============================================================

# Probability of hazard -  Low; Moderate; High; Not known
# Impact of hazard  -  Low; Moderate; High; Not known
# Expected change in hazard intensity - Increase; Decrease; No change; Not known
# Expected change in hazard frequency - Increase; Decrease; No change; Not known
# Timeframe(s) - Short-term; Mid-term; Long-term; Not known

probability_impact_string_mapping = {
    2: "High",
    1: "Moderate",
    0: "Low",
    -5: "Uncertain",
    -10: "Not known",
}

intensity_frequency_string_mapping = {
    1: "Increase",
    0: "No change",
    -1: "Decrease",
    -5: "Uncertain",
    -10: "Not known",
}

timeframe_string_mapping = {
    0: "Short-term",
    1: "Mid-term",
    2: "Long-term",
    -5: "Uncertain",
    -10: "Not known",
}


def extract_variables(equation):
    # Define a regex pattern for variable names (letters, numbers, and underscores)
    variable_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
    # Find all matches
    matches = re.findall(variable_pattern, equation)
    # Remove keywords that are not variables (e.g., "100" or operators)
    return [var.strip() for var in matches if not var.strip().isdigit()]


soi_value_dict = {}

for idx, row in soi_vars_with_dsp_input.iterrows():

    soi_name = row["soi_name"]
    equation = row["calculation"]

    equation = equation.replace("\n", " ")

    try:
        # cases where calculations are required
        if any(symbol in equation for symbol in ["+", "/", "*"]):
            input_vars = extract_variables(equation)

            for input_var in input_vars:
                if input_var.startswith("eucalc_"):
                    sub_region_data = region_data[
                        (region_data["var_name"] == input_var)
                        & (region_data["year"] == 2020)
                    ]  # EUCalc 2020 value is taken
                else:
                    sub_region_data = region_data[region_data["var_name"] == input_var]

                value = sub_region_data["value"].item()

                equation = equation.replace(input_var, str(value))

            # Evaluate the equation and append calculated value to the SOI dict
            value = eval(equation)
            soi_value_dict[soi_name] = value

        # cases when its directly a variable from DSP
        else:
            if equation.startswith("eucalc_"):
                sub_region_data = region_data[
                    (region_data["var_name"] == equation)
                    & (region_data["year"] == 2020)
                ]  # 2020 value is taken

                value = sub_region_data["value"].item()

            elif equation.startswith("cproj_"):
                sub_region_data = region_data[
                    (region_data["var_name"] == equation)
                    & (region_data["year"] == 2020)
                    & (  # 2020 value is taken
                        region_data["climate_experiment"] == "RCP4.5"
                    )
                ]  #  RCP4.5 scenario is considered

                value = sub_region_data["value"].item()

            elif equation.startswith("cimp_"):
                sub_region_data = region_data[
                    (region_data["var_name"] == equation)
                    & (region_data["climate_experiment"].isin(("RCP4.5", "Historical")))
                ]  # Historical or RCP4.5 value is taken
                # for climate impact data

                if ("historical_probability" in equation) or ("impact" in equation):
                    int_value = int(sub_region_data["value"].item())
                    value = probability_impact_string_mapping[int_value]

                elif ("change_in_frequency" in equation) or (
                    "change_in_intensity" in equation
                ):
                    int_value = int(sub_region_data["value"].item())
                    value = intensity_frequency_string_mapping[int_value]

                elif "time_frame" in equation:
                    int_value = int(sub_region_data["value"].item())
                    value = timeframe_string_mapping[int_value]

            else:
                sub_region_data = region_data[region_data["var_name"] == equation]
                value = sub_region_data["value"].item()

            soi_value_dict[soi_name] = value

    # some of the ratio calculations have 0/(0+0). This should result in 0
    except ZeroDivisionError:
        soi_value_dict[soi_name] = 0

# =============================================================
# Filling CoM template
# =============================================================

start = time.time()

# Define file paths
original_file_path = os.path.join(
    "..", "data", "input", "CoM-Europe_reporting_template_2023_final_with_tags.xlsx"
)
output_file_path = os.path.join("..", "data", "output", f"CoM_{region_code}.xlsx")

# Make a copy of the original file (otherwise it overwrites the original one!)
shutil.copy(original_file_path, output_file_path)

# Open the copied file
app = xw.App(visible=False)  # Run Excel in the background
workbook = app.books.open(output_file_path)

# fill sheets
for sheet_name in [
    "GHG emissions",
    "Risks & vulnerabilities",
    "Energy poverty assessment",
]:

    sheet = workbook.sheets[sheet_name]

    # Get used range
    used_range = sheet.used_range
    last_column = used_range.last_cell.column

    # Ensure we only loop up to column Z (26)
    # NOTE: although the unused columns were hidden, it still looped through all of them!
    # So it is being stopped at Z here which is more columns than currently used.
    # If this changes in the future templates, this needs to be changed.
    max_column = min(last_column, 26)

    for row in sheet.range((1, 1), (used_range.last_cell.row, max_column)):
        for cell in row:
            if cell.value in soi_value_dict.keys():
                soi_value = soi_value_dict[cell.value]

                cell.value = soi_value

    print(f"Finished filling {sheet_name}")

# Close Excel
workbook.close()
app.quit()

end = time.time()

print(f"time taken {end-start} s")
