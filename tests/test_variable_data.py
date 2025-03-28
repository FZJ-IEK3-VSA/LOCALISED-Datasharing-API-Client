import pytest
import pandas as pd
from zoomin_client import client


def test_get_variable_metadata():
    """Check if variable metadata is returned."""
    output = client.get_variable_metadata(
        version="v4",
        country_code="lv",
        variable="residential_final_energy_consumption_from_ethane",
    )

    assert isinstance(output, list)


@pytest.mark.parametrize("result_format", ["json", "df"])
def test_get_variable_data(result_format):
    """Check if variable data is returned."""
    output = client.get_variable_data(
        version="v4",
        variable="tenancy_renters",
        spatial_resolution="LAU",
        country_code="lv",
        result_format=result_format,
    )

    if result_format == "json":
        assert isinstance(output, list)

    else:
        assert isinstance(output, pd.DataFrame)
