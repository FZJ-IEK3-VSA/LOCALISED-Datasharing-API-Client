"""Data acess functions are present in this module."""
import os
from typing import Optional, Union
import json
import requests
import pandas as pd


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


def get_regions(
    api_key: str,
    spatial_resolution: Optional[str] = "NUTS3",
    region_code: Optional[str] = None,
    result_format: Optional[str] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "regions",
) -> Union[dict, pd.DataFrame]:
    """
    Return list of regions or one particular region.

    :param api_key: the secret api key
    :type api_key: str

    **Default arguments:**

    :param spatial_resolution: the required spatial level
        |br| * the default value is 'NUTS3'
    :type spatial_resolution: str, one of {'Europe', 'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    :param region_code: the code of the region to filter on.
        If None, all regions are returned.
        |br| * the default value is None
    :type region_code: str

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
        |br| * the default value is 'regions'
    :type save_path: str

    :returns: The result
    :rtype: dict/pd.DataFrame
    """
    # request
    request_url = f"http://data.localised-project.eu/api/v1/{spatial_resolution}/?api_key={api_key}"

    if region_code is not None:
        request_url = f"{request_url}&region={region_code}"

    response = requests.get(request_url, timeout=240)

    # required format
    if result_format == "json":
        result = response.json()[0]
    elif result_format == "df":
        response_data = response.json()[0].get("regions")
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
    spatial_resolution: Optional[str] = "NUTS3",
    region_code: str = "DEA23",
    result_format: Optional[str] = "json",
    save_result: Optional[bool] = False,
    save_path: Optional[str] = None,
    save_name: Optional[str] = "region_data",
) -> Union[dict, pd.DataFrame]:
    """
    Return data for a specified region.

    :param api_key: the secret api key
    :type api_key: str

    **Default arguments:**

    :param spatial_resolution: the required spatial level
        |br| * the default value is 'NUTS3'
    :type spatial_resolution: str, one of {'Europe', 'NUTS0', 'NUTS1', 'NUTS2', 'NUTS3', 'LAU'}

    :param region_code: the code of the region to filter on.
        |br| * the default value is 'DEA23'
    :type region_code: str

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
    request_url = f"{base_url}{spatial_resolution}/?api_key={api_key}&region={region_code}&type=data"
    response = requests.get(request_url, timeout=480)

    # required format
    if result_format == "json":
        result = response.json()
    elif result_format == "df":
        response_data = response.json().get("regions")[0].get("region_data")
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
