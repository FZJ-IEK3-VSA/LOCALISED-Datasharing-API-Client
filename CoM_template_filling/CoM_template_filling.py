import os
import sys

# Add parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


import re
import shutil
import time
from openpyxl import load_workbook
import pandas as pd
import logging

from zoomin_client import client


# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('CoM_template_filling.log'),
        logging.StreamHandler()  # Also print to console
    ]
)


def get_region_data(region_code, pathway_description="national", result_format="df"):
    """
    Get region data from the DSP
    """
    region_data = client.get_region_data(
        version="v1",
        country_code=region_code[:2].lower(),
        region_code=region_code,
        pathway_description=pathway_description,
        result_format=result_format,
    )
    return region_data

def clean_region_data(region_data):
    """
    Clean region data to reflect change in names. Next DSP deploy will have it changed
    """
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
    return region_data


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
    """
    Extract variables from an equation
    """
    # Define a regex pattern for variable names (letters, numbers, and underscores)
    variable_pattern = r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
    # Find all matches
    matches = re.findall(variable_pattern, equation)
    # Remove keywords that are not variables (e.g., "100" or operators)
    return [var.strip() for var in matches if not var.strip().isdigit()]


def get_dsp_value(variable, region_data, year=2020, climate_experiment="RCP4.5"):
    """
    Get value from DSP for a variable
    """
    try:
        if variable.startswith("eucalc_"):
            sub_region_data = region_data[
                (region_data["var_name"] == variable) & (region_data["year"] == year)
            ]  # 2020 value is taken

            if len(sub_region_data) == 0:
                logger.warning(f"No data found for variable {variable}")
                return 0
            
            dsp_value = sub_region_data["value"].iloc[0]

        elif variable.startswith("cproj_"):
            sub_region_data = region_data[
                (region_data["var_name"] == variable)
                & (region_data["year"] == year)
                & (region_data["climate_experiment"] == climate_experiment)  # 2020 value is taken
            ]  #  RCP4.5 scenario is considered
            
            if len(sub_region_data) == 0:
                logger.warning(f"No data found for variable {variable}")
                return 0
                
            dsp_value = sub_region_data["value"].iloc[0]

        elif variable.startswith("cimp_"):
            sub_region_data = region_data[
                (region_data["var_name"] == variable)
                & (region_data["climate_experiment"].isin(("RCP4.5", "Historical")))
            ]  # Historical or RCP4.5 value is taken
            # for climate impact data
            
            if len(sub_region_data) == 0:
                logger.warning(f"No data found for variable {variable}")
                return 0

            if ("historical_probability" in variable) or ("impact" in variable):
                int_value = int(sub_region_data["value"].iloc[0])
                dsp_value = probability_impact_string_mapping[int_value]

            elif ("change_in_frequency" in variable) or ("change_in_intensity" in variable):
                int_value = int(sub_region_data["value"].iloc[0])
                dsp_value = intensity_frequency_string_mapping[int_value]

            elif "time_frame" in variable:
                int_value = int(sub_region_data["value"].iloc[0])
                dsp_value = timeframe_string_mapping[int_value]

        else:
            sub_region_data = region_data[region_data["var_name"] == variable]
            if len(sub_region_data) == 0:
                logger.warning(f"No data found for variable {variable}")
                return 0
                
            dsp_value = sub_region_data["value"].iloc[0]

        return dsp_value
        
    except Exception as e:
        logger.error(f"Error getting DSP value for {variable}: {str(e)}")
        return 0

def calculate_sois(region_code: str, region_data: pd.DataFrame) -> dict:
    """
    Calculate SOIs for a region.
    """
    soi_value_dict = {}

    # Get SOI calculation excel sheet
    soi_metadata_df = pd.read_excel(
        os.path.join(
            "./CoM_template_filling",
            "data",
            "input",
            "variables_with_details_and_tags.xlsx",
        ),
        sheet_name="admin_business_and_social_KPIs",
    )

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
                    value = get_dsp_value(input_var, region_data)

                    equation = equation.replace(input_var, str(value))

                # Evaluate the equation and append calculated value to the SOI dict
                value = eval(equation)
                soi_value_dict[soi_name] = value

            # cases when its directly a variable from DSP
            else:
                dsp_value = get_dsp_value(equation, region_data)
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
        os.path.join("./CoM_template_filling", "data", "output", f"SOIs_{region_code}.xlsx"), index=False
    )
    return soi_value_dict


def fill_com_template(region_code, soi_value_dict, region_data):
    """
    Fill the CoM template with calculated values.
    """
    logger.info(f"Starting CoM template filling for {region_code}")
    start = time.time()

    try:
        # Define file paths
        original_file_path = os.path.join(
            "./CoM_template_filling", "data", "input", "CoM-Europe_reporting_template_2023_v3.xlsx"
        )
        output_dir = os.path.join("./CoM_template_filling", "data", "output")
        output_file_path = os.path.join(output_dir, f"CoM_{region_code}.xlsx")

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Make a copy of the original file
        try:
            shutil.copy2(original_file_path, output_file_path)
            logger.info(f"Template copied to {output_file_path}")
        except Exception as e:
            logger.error(f"Failed to copy template: {str(e)}")
            raise

        # Open the copied file
        try:
            workbook = load_workbook(output_file_path)
        except Exception as e:
            logger.error(f"Failed to load workbook: {str(e)}")
            raise

        # fill sheets
        sheets_to_fill = [
            "GHG emissions",
            "Risks & vulnerabilities",
            "Energy poverty assessment",
        ]

        for sheet_name in sheets_to_fill:
            try:
                sheet = workbook[sheet_name]
                logger.info(f"Filling sheet: {sheet_name}")

                # Get used range
                max_row = sheet.max_row
                max_column = min(sheet.max_column, 26)  # Limit to column Z

                for row in sheet.iter_rows(
                    min_row=1, max_row=max_row, min_col=1, max_col=max_column
                ):
                    for cell in row:
                        if cell.value in soi_value_dict:
                            cell.value = soi_value_dict[cell.value]
                        elif isinstance(cell.value, str) and cell.value in region_data["var_name"].values:
                            dsp_value = get_dsp_value(cell.value, region_data)
                            cell.value = dsp_value

                logger.info(f"Finished filling {sheet_name}")
            except Exception as e:
                logger.error(f"Error filling sheet {sheet_name}: {str(e)}")
                raise

        # Save and close the workbook
        try:
            # Try to save with a temporary name first
            temp_path = output_file_path + '.tmp'
            workbook.save(temp_path)
            
            # If save successful, rename to final name
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
            os.rename(temp_path, output_file_path)
            
            logger.info(f"Successfully saved workbook to {output_file_path}")
        except Exception as e:
            logger.error(f"Failed to save workbook: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
        finally:
            workbook.close()

        end = time.time()
        logger.info(f"Template filling completed in {end-start:.2f} seconds")
        
        return output_file_path

    except Exception as e:
        logger.error(f"Failed to fill template: {str(e)}")
        raise RuntimeError(f"Failed to fill CoM template: {str(e)}")

if __name__ == "__main__":
    region_code = "DEA23"
    region_data = clean_region_data(get_region_data(region_code))
    soi_value_dict = calculate_sois(region_code, region_data)
    fill_com_template(region_code, soi_value_dict, region_data)
