import os
import re
import shutil
import time
from openpyxl import load_workbook
import pandas as pd
from zoomin_client import client

# =============================================================
# Importing data and SOI metadata
# =============================================================

# Get SOI calculation excel sheet
soi_metadata_df = pd.read_excel(
    os.path.join(
        "..",
        "data",
        "input",
        "variables_with_details_and_tags.xlsx",
    ),
    sheet_name="admin_business_and_social_KPIs",
)

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
        "energy_demand_in_transport_from_belended_biogasoline": "energy_demand_in_transport_from_blended_biogasoline",
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


def get_dsp_value(variable):
    if variable.startswith("eucalc_"):
        sub_region_data = region_data[
            (region_data["var_name"] == variable) & (region_data["year"] == 2020)
        ]  # 2020 value is taken

        dsp_value = sub_region_data["value"].item()

    elif variable.startswith("cproj_"):
        sub_region_data = region_data[
            (region_data["var_name"] == variable)
            & (region_data["year"] == 2020)
            & (region_data["climate_experiment"] == "RCP4.5")  # 2020 value is taken
        ]  #  RCP4.5 scenario is considered

        dsp_value = sub_region_data["value"].item()

    elif variable.startswith("cimp_"):
        sub_region_data = region_data[
            (region_data["var_name"] == variable)
            & (region_data["climate_experiment"].isin(("RCP4.5", "Historical")))
        ]  # Historical or RCP4.5 value is taken
        # for climate impact data

        if ("historical_probability" in variable) or ("impact" in variable):
            int_value = int(sub_region_data["value"].item())
            dsp_value = probability_impact_string_mapping[int_value]

        elif ("change_in_frequency" in variable) or ("change_in_intensity" in variable):
            int_value = int(sub_region_data["value"].item())
            dsp_value = intensity_frequency_string_mapping[int_value]

        elif "time_frame" in variable:
            int_value = int(sub_region_data["value"].item())
            dsp_value = timeframe_string_mapping[int_value]

    else:
        sub_region_data = region_data[region_data["var_name"] == variable]
        dsp_value = sub_region_data["value"].item()

    return dsp_value


soi_value_dict = {}

# SOI calculations using collected and EUCalc data
soi_vars_with_dsp_input = soi_metadata_df[
    (~soi_metadata_df["var_name"].isna())
    & (~soi_metadata_df["calculation"].isin(["BLANK", "TBD"]))
    & (  # some SOIs are decided to be left blank or TBD yet
        soi_metadata_df["data_source"] != "TOTAL"
    )  # some SOIs are sum of other SOIs
][["var_name", "calculation"]]

for idx, row in soi_vars_with_dsp_input.iterrows():

    soi_name = row["var_name"]
    equation = row["calculation"]

    equation = equation.replace("\n", " ")

    try:
        # cases where calculations are required
        if any(symbol in equation for symbol in ["+", "/", "*"]):
            input_vars = extract_variables(equation)

            for input_var in input_vars:
                value = get_dsp_value(input_var)

                equation = equation.replace(input_var, str(value))

            # Evaluate the equation and append calculated value to the SOI dict
            value = eval(equation)
            soi_value_dict[soi_name] = value

        # cases when its directly a variable from DSP
        else:
            dsp_value = get_dsp_value(equation)
            soi_value_dict[soi_name] = dsp_value

    # some of the ratio calculations have 0/(0+0). This should result in 0
    except ZeroDivisionError:
        soi_value_dict[soi_name] = 0


# SOI calculations using other SOIs - Totals
soi_vars_with_totals = soi_metadata_df[soi_metadata_df["data_source"] == "TOTAL"][
    ["var_name", "calculation"]
]

for idx, row in soi_vars_with_totals.iterrows():

    soi_name = row["var_name"]
    equation = row["calculation"]

    equation = equation.replace("\n", " ")

    input_vars = extract_variables(equation)

    for input_var in input_vars:

        value = soi_value_dict[input_var]

        equation = equation.replace(input_var, str(value))

    value = eval(equation)
    soi_value_dict[soi_name] = value

# save calculated SOIs as excel
soi_calc_df = pd.DataFrame(list(soi_value_dict.items()), columns=["var_name", "value"])

soi_calc_df.to_excel(
    os.path.join("..", "data", "output", f"SOIs_{region_code}.xlsx"), index=False
)

# =============================================================
# Filling CoM template
# =============================================================

start = time.time()

# Define file paths
original_file_path = os.path.join(
    "..", "data", "input", "CoM-Europe_reporting_template_2023_v3.xlsx"
)
output_file_path = os.path.join("..", "data", "output", f"CoM_{region_code}.xlsx")

# Make a copy of the original file (otherwise it overwrites the original one!)
shutil.copy(original_file_path, output_file_path)

# Open the copied file
workbook = load_workbook(output_file_path)

# fill sheets
for sheet_name in [
    "GHG emissions",
    "Risks & vulnerabilities",
    "Energy poverty assessment",
]:

    sheet = workbook[sheet_name]

    # Get used range
    # Ensure we only loop up to column Z (26)
    # NOTE: although the unused columns were hidden, it still looped through all of them!
    # So it is being stopped at Z here which is more columns than currently used.
    # If this changes in the future templates, this needs to be changed.
    max_row = sheet.max_row
    max_column = min(sheet.max_column, 26)  # Limit to column Z (26)

    for row in sheet.iter_rows(
        min_row=1, max_row=max_row, min_col=1, max_col=max_column
    ):
        for cell in row:
            if cell.value in soi_value_dict.keys():
                cell.value = soi_value_dict[cell.value]

            elif cell.value in region_data["var_name"].values:
                dsp_value = get_dsp_value(cell.value)
                cell.value = dsp_value

    print(f"Finished filling {sheet_name}")

# Save and close the workbook
workbook.save(output_file_path)
workbook.close()

end = time.time()

print(f"time taken {end-start} s")
