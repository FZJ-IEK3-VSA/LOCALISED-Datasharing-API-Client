import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize(
    "spatial_resolution, region_code", [ ("NUTS3", "DEA23"), ("LAU", "05315000")]  # ("NUTS0", "DE"), #TODO: check why error is returned for this case 
)
def test_get_region_data(api_key, spatial_resolution, region_code):
    """Check if region data is returned."""
    output = client.get_region_data(api_key, 
                                    spatial_resolution=spatial_resolution, 
                                    region_code=region_code)
    assert output.get("resolution") == spatial_resolution
    
#TODO: add data value asserts here 
@pytest.mark.parametrize(
    "result_format", ["json", "df"]
)
def test_save_region_data(api_key, result_format):
    """Check if the results of get_region_data() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__), "..", "data")
    output = client.get_region_data(api_key, spatial_resolution="NUTS3", result_format=result_format, save_result=True, save_path=save_path)

    if result_format == "json":
        assert isinstance(output, dict)
        assert os.path.exists(os.path.join(save_path, "region_data.json"))
    else:
        assert isinstance(output, pd.DataFrame)
        assert os.path.exists(os.path.join(save_path, "region_data.csv"))
    
