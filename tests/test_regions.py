import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize(
    "spatial_resolution", ["Europe", "NUTS0", "NUTS1", "NUTS2", "NUTS3", "LAU"]
)
def test_get_regions(api_key, spatial_resolution):
    """Check if region list is returned."""
    output = client.get_regions(api_key, spatial_resolution)
    assert output.get("resolution") == spatial_resolution

@pytest.mark.parametrize(
    "result_format", ["json", "df"]
)
def test_save_regions(api_key, result_format):
    """Check if the results of get_regions() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__), "..", "data")
    output = client.get_regions(api_key, spatial_resolution="NUTS0", result_format=result_format, save_result=True, save_path=save_path)

    if result_format == "json":
        assert isinstance(output, dict)
        assert len(output.get("regions")) == 27
        assert os.path.exists(os.path.join(save_path, "regions.json"))
    else:
        assert isinstance(output, pd.DataFrame)
        assert len(output) == 27
        assert os.path.exists(os.path.join(save_path, "regions.csv"))
    
    
def test_get_single_region(api_key):
    """Check if filtering on a region works."""
    region_code="DEA23"
    output = client.get_regions(api_key, spatial_resolution="NUTS3", region_code=region_code)
    assert output.get("regions")[0].get("region_code") == region_code  
