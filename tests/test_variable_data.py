import pytest
import pandas as pd
from zoomin_client import client


def test_get_variable_metadata():
    """Check if variable metadata is returned."""
    output = client.get_variable_metadata(variable="population", country_code="de")

    assert isinstance(output, dict)


@pytest.mark.parametrize("result_format", ["json", "df"])
def test_get_variable_data(result_format):
    """Check if variable data is returned."""
    output = client.get_variable_data(
        variable="population",
        spatial_resolution="LAU",
        country_code="es",
        result_format=result_format,
    )

    if result_format == "json":
        assert isinstance(output, list)

    else:
        assert isinstance(output, pd.DataFrame)
