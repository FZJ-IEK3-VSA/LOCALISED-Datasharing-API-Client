import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize("spatial_resolution", ["NUTS0", "NUTS1", "NUTS2", "NUTS3"])
def test_get_regions(api_key, spatial_resolution):
    """Check if region list is returned."""
    output = client.get_regions(api_key, spatial_resolution)
    assert output[0].get("resolution") == spatial_resolution


@pytest.mark.parametrize("result_format", ["json", "df"])
def test_save_regions(api_key, result_format):
    """Check if the results of get_regions() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__))
    output = client.get_regions(
        api_key,
        spatial_resolution="NUTS0",
        result_format=result_format,
        save_result=True,
        save_path=save_path,
    )

    if result_format == "json":
        assert isinstance(output, list)
        assert len(output) == 3

        file_name = os.path.join(save_path, "regions.json")
        assert os.path.exists(file_name)
        os.remove(file_name)
    else:
        assert isinstance(output, pd.DataFrame)
        assert len(output) == 3

        file_name = os.path.join(save_path, "regions.csv")
        assert os.path.exists(file_name)
        os.remove(file_name)


def test_get_single_region(api_key):
    """Check if filtering on a region works."""
    region_code = "05315000"
    country_code = "DE"
    output = client.get_regions(
        api_key,
        spatial_resolution="LAU",
        region_code=region_code,
        country_code=country_code,
    )
    assert output[0].get("region_code") == region_code
