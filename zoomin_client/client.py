import os
from typing import Any, Dict, Optional, List
import json
import requests
import pandas as pd


def save_json(data, save_path: str, save_name: str) -> None:
    """Save the response in a json file."""
    file_name = os.path.join(save_path, save_name)

    with open(file_name, "w") as f:
        json.dump(data, f)


def save_df(data_df: pd.DataFrame, save_path: str, save_name: str) -> None:
    """Save the data in a csv file."""

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
) -> List[dict]:
    """Return list of regions or one particular region."""
    # request
    request_url = f"http://data.localised-project.eu/api/v1/{spatial_resolution}/?api_key={api_key}"

    if region_code is not None:
        request_url = f"{request_url}&region={region_code}"

    response = requests.get(request_url)

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
) -> Dict[str, Any]:
    """Return data for a specified region."""
    # request
    base_url = "http://data.localised-project.eu/api/v1/"
    request_url = f"{base_url}{spatial_resolution}/?api_key={api_key}&region={region_code}&type=data"
    response = requests.get(request_url)

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
