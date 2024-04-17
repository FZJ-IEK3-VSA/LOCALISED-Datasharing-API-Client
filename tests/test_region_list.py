import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize("spatial_resolution", ["NUTS1", "NUTS2", "NUTS3"])
def test_get_region_list(api_key, spatial_resolution):
    """Check if region list is returned."""
    output = client.get_region_metadata(api_key, spatial_resolution, country_code="DE")
    assert output[0].get("resolution") == spatial_resolution



def test_save_regions(api_key):
    """Check if the results of get_regions() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__))
    output = client.get_region_metadata(
        api_key,
        spatial_resolution="NUTS3",
        country_code="DE",
        save_result=True,
        save_path=save_path,
    )

    assert isinstance(output, list)
    assert len(output) == 401

    file_name = os.path.join(save_path, "region_metadata.json")
    assert os.path.exists(file_name)
    os.remove(file_name)
