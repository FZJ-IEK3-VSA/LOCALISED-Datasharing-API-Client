#load required libraries 
from typing import Any, Dict, Optional, List
import json
import requests
from pandas import json_normalize

def get_regions(api_key: str, spatial_resolution: Optional[str] = "NUTS3", region_code: Optional[str] = None) -> List[dict]:
    """Return list of regions or one particular region."""
    request_url = f"http://data.localised-project.eu/api/v1/{spatial_resolution}/?api_key={api_key}"

    if region_code is not None:
        request_url = f"{request_url}&region={region_code}"

    response = requests.get(request_url)

    #get the json response 
    response_json = response.json()

    return response_json


def get_region_data(api_key: str, spatial_resolution: Optional[str] = "NUTS3", region_code: str = "DEA23") -> Dict[str, Any]:
    """Return data for a specified region."""
    base_url = "http://data.localised-project.eu/api/v1/"
    request_url = f"{base_url}{spatial_resolution}/?api_key={api_key}&region={region_code}&type=data"
    response = requests.get(request_url)

    #get the json response 
    response_json = response.json()

    return response_json

    # #save the entire json response in a json file 
    # with open('data.json', 'w') as f:
    #     json.dump(response_json, f)

    # #alternatively, save only the regional data (region_data) as a .csv file 
    # data_df = json_normalize(response_json.get('regions')[0].get('region_data'))
    # data_df.to_csv('region_data.csv')