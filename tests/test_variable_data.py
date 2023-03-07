import pytest
import pandas as pd
from zoomin_client import client


def test_get_variable_metadata(api_key):
    """Check if variable metadata is returned."""
    output = client.get_variable_metadata(
        api_key, country_code="ES", variable_name="population"
    )

    assert isinstance(output, dict)


@pytest.mark.parametrize("result_format", ["json", "df"])
def test_get_variable_data(api_key, result_format):
    """Check if variable data is returned."""
    output = client.get_variable_data(
        api_key,
        country_code="ES",
        variable_name="population",
        result_format=result_format,
    )

    if result_format == "json":
        assert isinstance(output, list)

    else:
        assert isinstance(output, pd.DataFrame)
