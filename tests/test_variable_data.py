import pytest
import pandas as pd
from zoomin_client import client


@pytest.mark.parametrize("result_format", ["json", "df"])
def test_get_region_data(api_key, result_format):
    """Check if variable data is returned."""
    output = client.get_variable_data(
        api_key,
        region_code="08126",
        country_code="ES",
        variable_name="population",
        result_format=result_format,
    )

    if result_format == "json":
        assert isinstance(output, dict)

    else:
        assert isinstance(output, pd.DataFrame)
