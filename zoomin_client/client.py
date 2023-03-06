"""Data acess functions are present in this module."""
import os
import logging
import http.client
from typing import Optional, Union
import json
import requests
import pandas as pd

http.client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


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


def get_region_list(
    api_key: str,
    spatial_resolution: str,
    country_code: str,
    result_format: Optional[str] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "region_list",
) -> Union[dict, pd.DataFrame]:
    """
    Return list of regions of a specified country, at a specified spatial resolution.

    :param api_key: the secret api key
    :type api_key: str

    :param spatial_resolution: the required spatial level
    :type spatial_resolution: str, one of {'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    :param country_code: the code of the required country
    :type region_code: str

    **Default arguments:**

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
        |br| * the default value is 'region_list'
    :type save_path: str

    :returns: The result
    :rtype: dict/pd.DataFrame
    """
    # request
    request_url = f"http://data.localised-project.eu/api/v1/region_list/?api_key={api_key}&resolution={spatial_resolution}&country={country_code}"

    response = requests.get(request_url, timeout=240)

    # required format
    if result_format == "json":
        result = response.json()
    elif result_format == "df":
        response_data = response.json()
        result = pd.json_normalize(response_data)
    else:
        raise ValueError("Unrecognised result_format. Available options: json and df")

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(data=result, save_path=save_path, save_name=f"{save_name}.json")
        else:
            save_df(data_df=result, save_path=save_path, save_name=f"{save_name}.csv")

    return result


def get_region_data(
    api_key: str,
    spatial_resolution: str,
    region_code: str,
    country_code: str,
    result_format: Optional[str] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "region_data",
) -> Union[dict, pd.DataFrame]:
    """
    Return all the data for a specified region.

    :param api_key: the secret api key
    :type api_key: str

    :param spatial_resolution: the required spatial resolution
    :type spatial_resolution: str, one of {'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    :param region_code: the code of the region to filter on
    :type region_code: str

    :param country_code: the code of the country to which `region_code` belongs.
    :type region_code: str

    **Default arguments:**

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
    :rtype: dict/pd.DataFrame
    """
    # request
    base_url = "http://data.localised-project.eu/api/v1/"
    request_url = f"{base_url}region_data/?api_key={api_key}&resolution={spatial_resolution}&region={region_code}&country={country_code}"
    response = requests.get(request_url, stream=True, timeout=1200)

    # required format
    if result_format == "json":
        result = response.json()
    elif result_format == "df":
        response_data = response.json().get("region_data")
        result = pd.json_normalize(response_data)
        result["region_code"] = region_code
        result["country_code"] = country_code
    else:
        raise ValueError("Unrecognised result_format. Available options: json and df")

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(data=result, save_path=save_path, save_name=f"{save_name}.json")
        else:
            save_df(data_df=result, save_path=save_path, save_name=f"{save_name}.csv")

    return result


def get_variable_data(
    api_key: str,
    variable_name: str,
    region_code: str,
    country_code: str,
    result_format: Optional[str] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "variable_data",
) -> Union[dict, pd.DataFrame]:
    """
    Return data for a specified variable at LAU level.

    :param api_key: the secret api key
    :type api_key: str

    :param variable_name: the required variable
    :type variable_name: str

    :param region_code: the code of the region to filter on
    :type region_code: str

    :param country_code: the code of the country for which data should be returned
    :type region_code: str

    **Default arguments:**

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
    :rtype: dict/pd.DataFrame
    """
    # request
    base_url = "http://data.localised-project.eu/api/v1/"
    request_url = f"{base_url}variable_data/?api_key={api_key}&region={region_code}&country={country_code}&variable={variable_name}"
    response = requests.get(request_url, stream=True, timeout=240)

    # required format
    if result_format == "json":
        result = response.json()[0]
    elif result_format == "df":
        response_data = response.json()[0]

        result = pd.json_normalize(response_data.get("region_data"))

        field_list = [
            "var_name",
            "var_description",
            "var_unit",
            "var_aggregation_method",
            "proxy_metrics",
        ]
        for field in field_list:
            if field == "proxy_metrics":
                result[field] = ", ".join(field)
            else:
                result[field] = response_data.get(field)
    else:
        raise ValueError("Unrecognised result_format. Available options: json and df")

    # save
    if save_result:
        if save_path is None:
            save_path = os.path.dirname(__file__)

        if result_format == "json":
            save_json(data=result, save_path=save_path, save_name=f"{save_name}.json")
        else:
            save_df(data_df=result, save_path=save_path, save_name=f"{save_name}.csv")

    return result
