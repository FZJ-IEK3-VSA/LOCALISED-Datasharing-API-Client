import pytest
from zoomin_client import client


@pytest.mark.parametrize(
    ("variable", "output"),
    [
        (
            "cproj_annual_mean_temperature_cooling_degree_days",
            9,
        ),  # one for each year. cproj_years = [2020, 2025, 2030, 2035, 2040, 2045, 2050, 2075, 2099]
        ("population", 1),
        (
            "eucalc_ind_emissions_co2e_textiles",
            7,
        ),  # one for each year. eucalc_years = [2020, 2025, 2030, 2035, 2040, 2045, 2050]
    ],
)
def test_get_proxy_details(variable, output):
    result = client.get_proxy_details(
        version="v4",
        country_code="lv",
        variable=variable,
    )

    assert len(result) == output
