"""Data acess functions are present in this module."""
import os
from typing import Optional, Union, Any, Literal
import json
import requests
import pandas as pd
from zoomin_client.utils import measure_time


def save_json(data: dict, save_path: str, save_name: str) -> None:
    """
    Save the response in a json file.

    :param data: data dictionary to be saved
    :type data: dict

    :param save_path: the folder path in which to save
    :type save_path: str

    :param save_name: the file name
    :type save_name: str
    """
    file_name = os.path.join(save_path, save_name)

    with open(file_name, "w", encoding="utf-8") as f_name:
        json.dump(data, f_name)


def save_df(data_df: pd.DataFrame, save_path: str, save_name: str) -> None:
    """
    Save the data in a csv file.

    :param data_df: dataframe to be saved
    :type data_df: pd.DataFrame

    :param save_path: the folder path in which to save
    :type save_path: str

    :param save_name: the file name
    :type save_name: str
    """
    file_name = os.path.join(save_path, save_name)
    data_df.to_csv(file_name)


def get_region_metadata(
    api_key: str,
    country_code: str,
    spatial_resolution: str,
    region_code: Optional[str] = None,
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "region_metadata",
) -> Union[list, dict]:
    """
    Return list of regions of a specified country, at a specified spatial resolution.

    :param api_key: the secret api key
    :type api_key: str

    :param country_code: the code of the required country. NOTE: must be in lower case
    :type region_code: str

    :param spatial_resolution: the required spatial resolution
    :type spatial_resolution: str, one of {'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    **Default arguments:**

    :param region_code: the code of the region to filter on
        |br| * the default value is None. If None, all regions are returned.
    :type region_code: str

    :param save_result: indicates whether the result should be saved.
        The result is saved as .json if `result_format` is 'json'
        and as .csv if `result_format` is 'df'
        |br| * the default value is False
    :type save_result: bool

    :param save_path: the folder path in which to save the result.
        If None, the result is save in the same folder as this file- `client.py`
        |br| * the default value is None
    :type save_path: str

    :param save_name: the file name of the result
        |br| * the default value is 'region_list'
    :type save_path: str

    :returns: The result
    :rtype: list/dict
    """
    # request
    next_request_url = (
        "http://data.localised-project.eu/dsp/v1/" + country_code.lower() + "/"
        "region_metadata/?"
        "api_key=" + api_key + "&"
        "resolution=" + spatial_resolution
    )
    print(next_request_url)

    if region_code is not None:
        next_request_url = f"{next_request_url}&region={region_code}"

    result_collection = []
    while next_request_url is not None:
        response = requests.get(next_request_url, stream=True, timeout=240)
        response.raise_for_status()

        response = response.json()

        next_request_url = response["next"]
        response_data = response["results"]

        result_collection.extend(response_data)

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        save_json(
            data=result_collection, save_path=save_path, save_name=f"{save_name}.json"
        )

    return result_collection


@measure_time
def get_region_data(
    api_key: str,
    country_code: str,
    region_code: str,
    variable: Optional[str] = None,
    pathway_description: Literal["national", "with_behavioural_changes"] = None,
    climate_experiment: Optional[str] = None,
    mini_version: Optional[bool] = True,
    result_format: Literal["json", "df"] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "region_data",
) -> Union[list, pd.DataFrame]:
    """
    Return all the data for a specified region of a specified country, at a specified spatial resolution.

    :param api_key: the secret api key
    :type api_key: str

    :param country_code: the code of the required country. NOTE: must be in lower case
    :type region_code: str

    :param region_code: the code of the region to filter on
    :type region_code: str

    **Default arguments:**

    :param variable: the variable to filter on
        |br| * the default value is None
    :type variable: str

    :param pathway_description: the EUCalc pathway on which to filter data. Options: "national" or "with_behavioural_changes".
        |br| * the default value is None
    :type pathway_description: str

    :param climate_experiment: the climate experiment on which to filter climate data. For example: "RCP2.6"
        |br| * the default value is None
    :type climate_experiment: str

    :param mini_version: indicates if a reduced number of fields on data should be returned
        |br| * the default value is True
    :type mini_version: bool

    :param result_format: the format of the resulting data
        |br| * the default value is 'json'
    :type result_format: str, one of {'json', 'df'}

    :param save_result: indicates whether the result should be saved.
        The result is saved as .json if `result_format` is 'json'
        and as .csv if `result_format` is 'df'
        |br| * the default value is False
    :type save_result: bool

    :param save_path: the folder path in which to save the result.
        If None, the result is save in the same folder as this file- `client.py`
        |br| * the default value is None
    :type save_path: str

    :param save_name: the file name of the result
        |br| * the default value is 'region_data'
    :type save_path: str

    :returns: The result
    :rtype: list/pd.DataFrame
    """
    # base URL
    base_url = (
        f"http://data.localised-project.eu/dsp/v1/{country_code.lower()}/region_data/"
    )
    # mini version
    if mini_version:
        base_url = f"{base_url}mini_version/"

    # default URL
    next_request_url = f"{base_url}?api_key={api_key}&region={region_code}"

    # optional filters
    ## variable
    if variable is not None:
        next_request_url = f"{next_request_url}&variable={variable}"

    ## pathway
    if pathway_description is not None:
        if pathway_description not in ["national", "with_behavioural_changes"]:
            raise ValueError(
                "pathway_description should be one of national, with_behavioural_changes"
            )

        next_request_url = f"{next_request_url}&pathway={pathway_description}"

    ## climate experiment
    if climate_experiment is not None:
        if climate_experiment not in ["RCP2.6", "RCP4.5", "RCP8.5", "Historical"]:
            raise ValueError(
                "climate_experiment should be one of RCP2.6, RCP4.5, RCP8.5, Historical"
            )

        next_request_url = f"{next_request_url}&climate_experiment={climate_experiment}"

    result_collection = []
    while next_request_url is not None:
        print(next_request_url)
        response = requests.get(next_request_url, stream=True, timeout=240)

        response.raise_for_status()

        response = response.json()

        next_request_url = response["next"]
        response_data = response["results"]

        if result_format == "json":
            result_collection.extend(response_data)
        elif result_format == "df":
            result_collection.append(pd.json_normalize(response_data))

    if result_format == "df":
        result_collection = pd.concat(result_collection)

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(
                data=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.json",
            )
        else:
            save_df(
                data_df=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.csv",
            )

    return result_collection


def get_variable_metadata(
    api_key: str,
    country_code: str,
    variable: Optional[str] = None,
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "variable_metadata",
    result_format: Literal["json", "df"] = "json",
) -> Any:
    """
    Return data for a specified variable at a specified resolution, for a specified country.

    :param api_key: the secret api key
    :type api_key: str

    :param country_code: the code of the country for which data should be returned. NOTE: must be in lower case
    :type country_code: str

    **Default arguments:**

    :param variable: the variable to filter on.
        |br| * the default value is None
    :type variable: str

    :param save_result: indicates whether the result should be saved.
        The result is saved as .json
        |br| * the default value is False
    :type save_result: bool

    :param save_path: the folder path in which to save the result.
        If None, the result is save in the same folder as this file- `client.py`
        |br| * the default value is None
    :type save_path: str

    :param save_name: the file name of the result
        |br| * the default value is 'variable_metadata'
    :type save_path: str

    :returns: The result
    :rtype: Any
    """
    # request
    next_request_url = (
        "http://data.localised-project.eu/dsp/v1/" + country_code.lower() + "/"
        "variable_metadata/?"
        "api_key=" + api_key
    )

    # optional filter - variable
    if variable is not None:
        next_request_url = f"{next_request_url}&variable={variable}"

    result_collection = []
    while next_request_url is not None:
        print(next_request_url)
        response = requests.get(next_request_url, stream=True, timeout=240)

        response.raise_for_status()

        response = response.json()

        next_request_url = response["next"]
        response_data = response["results"]

        if result_format == "json":
            result_collection.extend(response_data)
        elif result_format == "df":
            result_collection.append(pd.json_normalize(response_data))

    if result_format == "df":
        result_collection = pd.concat(result_collection)

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(
                data=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.json",
            )
        else:
            save_df(
                data_df=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.csv",
            )

    return result_collection


def get_proxy_details(
    api_key: str,
    country_code: str,
    variable,
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "proxy_details",
    result_format: Literal["json", "df"] = "json",
) -> Any:
    """
    Return proxy details for a specified variable, for a specified country. Since there is a possibility to have different proxies
    for different years (present and future data), information for each year is returned.

    :param api_key: the secret api key
    :type api_key: str

    :param country_code: the code of the country for which data should be returned. NOTE: must be in lower case
    :type country_code: str

    :param variable: the variable to filter on.
    :type variable: str

    **Default arguments:**

    :param save_result: indicates whether the result should be saved.
        The result is saved as .json
        |br| * the default value is False
    :type save_result: bool

    :param save_path: the folder path in which to save the result.
        If None, the result is save in the same folder as this file- `client.py`
        |br| * the default value is None
    :type save_path: str

    :param save_name: the file name of the result
        |br| * the default value is 'variable_metadata'
    :type save_path: str

    :returns: The result
    :rtype: Any
    """
    # request
    request_url = (
        "http://data.localised-project.eu/dsp/v1/" + country_code.lower() + "/"
        "proxy_details/?"
        "api_key=" + api_key + "&"
        "variable=" + variable
    )

    response = requests.get(request_url, stream=True, timeout=240)

    response.raise_for_status()

    response = response.json()

    response_data = response["results"]

    if result_format == "df":
        response_data = pd.json_normalize(response_data)

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(
                data=response_data,
                save_path=save_path,
                save_name=f"{save_name}.json",
            )
        else:
            save_df(
                data_df=response_data,
                save_path=save_path,
                save_name=f"{save_name}.csv",
            )

    return response_data


@measure_time
def get_variable_data(
    api_key: str,
    country_code: str,
    spatial_resolution: str,
    variable: str,
    pathway_description: Literal["national", "with_behavioural_changes"] = None,
    climate_experiment: Optional[str] = None,
    result_format: Literal["json", "df"] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = os.path.dirname(__file__),
    save_name: Optional[str] = "variable_data",
) -> Union[list, pd.DataFrame]:
    """
    Return data for a specified variable at LAU level.

    :param api_key: the secret api key
    :type api_key: str

    :param country_code: the code of the country for which data should be returned. NOTE: must be in lower case
    :type country_code: str

    :param spatial_resolution: the required spatial resolution
    :type spatial_resolution: str, one of {'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    :param variable: the required variable
    :type variable: str

    **Default arguments:**

    :param pathway_description: the EUCalc pathway on which to filter data. Options: "national" or "with_behavioural_changes".
        |br| * the default value is None
    :type pathway_description: str

    :param climate_experiment: the climate experiment on which to filter data. For example: "RCP2.6"
        |br| * the default value is None
    :type climate_experiment: str

    :param result_format: the format of the resulting data
        |br| * the default value is 'json'
    :type result_format: str, one of {'json', 'df'}

    :param save_result: indicates whether the result should be saved.
        The result is saved as .json if `result_format` is 'json'
        and as .csv if `result_format` is 'df'
        |br| * the default value is False
    :type save_result: bool

    :param save_path: the folder path in which to save the result.
        If None, the result is save in the same folder as this file- `client.py`
        |br| * the default value is None
    :type save_path: str

    :param save_name: the file name of the result
        |br| * the default value is 'variable_data'
    :type save_path: str

    :returns: The result
    :rtype: list/pd.DataFrame
    """
    # default URL
    next_request_url = (
        "http://data.localised-project.eu/dsp/v1/" + country_code.lower() + "/"
        "variable_data/?"
        "api_key=" + api_key + "&"
        "resolution=" + spatial_resolution + "&"
        "variable=" + variable
    )

    # optional filters
    ## pathway
    if pathway_description is not None:
        if pathway_description not in ["national", "with_behavioural_changes"]:
            raise ValueError(
                "pathway_description should be one of national, with_behavioural_changes"
            )

        next_request_url = f"{next_request_url}&pathway={pathway_description}"

    ## climate experiment
    if climate_experiment is not None:
        if climate_experiment not in ["RCP2.6", "RCP4.5", "RCP8.5", "Historical"]:
            raise ValueError(
                "climate_experiment should be one of RCP2.6, RCP4.5, RCP8.5, Historical"
            )

        next_request_url = f"{next_request_url}&climate_experiment={climate_experiment}"

    result_collection = []
    while next_request_url is not None:
        print(next_request_url)
        response = requests.get(next_request_url, stream=True, timeout=240)

        response.raise_for_status()

        response = response.json()

        next_request_url = response["next"]
        response_data = response["results"]

        if result_format == "json":
            result_collection.extend(response_data)
        elif result_format == "df":
            result_collection.append(pd.json_normalize(response_data))

    if result_format == "df":
        result_collection = pd.concat(result_collection)

    # save
    if save_result:
        if result_format == "json":
            save_json(
                data=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.json",
            )
        else:
            save_df(
                data_df=result_collection,
                save_path=save_path,
                save_name=f"{save_name}.csv",
            )

    return result_collection
