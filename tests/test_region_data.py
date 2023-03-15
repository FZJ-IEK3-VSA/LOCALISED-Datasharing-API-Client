import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize(
    "spatial_resolution, region_code, country_code",
    [
        # ("NUTS3", "DEA23", "DE"),#TODO: uncomment other resolutions later
        # ("NUTS0", "DE"),
        ("LAU", "05315000", "DE"),
    ],
)
def test_get_region_data(api_key, spatial_resolution, region_code, country_code):
    """Check if region data is returned."""
    output = client.get_region_data(
        api_key,
        spatial_resolution=spatial_resolution,
        region_code=region_code,
        country_code=country_code,
    )
    assert len(output) > 0


# TODO: add data value asserts here
@pytest.mark.parametrize("result_format", ["json", "df"])
def test_save_region_data(api_key, result_format):
    """Check if the results of get_region_data() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__))
    output = client.get_region_data(
        api_key,
        spatial_resolution="LAU",
        region_code="11000000",
        country_code="DE",
        result_format=result_format,
        save_result=True,
        save_path=save_path,
    )

    if result_format == "json":
        assert isinstance(output, list)

        file_name = os.path.join(save_path, "region_data.json")
        assert os.path.exists(file_name)
        os.remove(file_name)
    else:
        assert isinstance(output, pd.DataFrame)

        file_name = os.path.join(save_path, "region_data.csv")
        assert os.path.exists(file_name)
        os.remove(file_name)
