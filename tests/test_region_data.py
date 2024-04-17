import os
import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize(
    "region_code",
    [
        ("DEA23"),
        ("DE"),
        ("DE600_02000000"),
    ],
)
def test_get_region_data(api_key, region_code):
    """Check if region data is returned."""
    output = client.get_region_data(api_key, region_code=region_code)
    assert len(output) > 0


# TODO: add data value asserts here
@pytest.mark.parametrize("result_format", ["json", "df"])
def test_save_region_data(api_key, result_format):
    """Check if the results of get_region_data() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__))
    output = client.get_region_data(
        api_key,
        region_code="DE600_02000000",
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
