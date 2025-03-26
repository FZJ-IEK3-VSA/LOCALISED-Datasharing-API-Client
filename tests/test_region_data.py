import os
import pytest
from zoomin_client import client


def test_get_region_data():
    """Check if region data is returned."""
    lau_output = client.get_region_data(
        version="v4",
        country_code="lv",
        region_code="LV007_0661000",
        result_format="df",
        mini_version=True,
    )

    nuts3_output = client.get_region_data(
        version="v4",
        country_code="lv",
        region_code="LV007",
        result_format="df",
        mini_version=True,
    )

    nuts2_output = client.get_region_data(
        version="v4",
        country_code="lv",
        region_code="LV00",
        result_format="df",
        mini_version=True,
    )

    nuts0_output = client.get_region_data(
        version="v4",
        country_code="lv",
        region_code="LV",
        result_format="df",
        mini_version=True,
    )

    # check if output is present
    assert len(lau_output) > 0
    assert len(nuts3_output) > 0
    assert len(nuts2_output) > 0
    assert len(nuts0_output) > 0

    # check if the number of variables are the same at all levels
    lau_n_vars = len(lau_output["var_name"].unique())
    nuts3_n_vars = len(nuts3_output["var_name"].unique())
    nuts2_n_vars = len(nuts2_output["var_name"].unique())
    nuts0_n_vars = len(nuts0_output["var_name"].unique())

    assert lau_n_vars == nuts3_n_vars == nuts2_n_vars == nuts0_n_vars

    # Climate Projection
    cproj_var = nuts3_output[
        nuts3_output["var_name"]
        == "cproj_annual_maximum_temperature_cooling_degree_days"
    ]
    assert len(cproj_var) == 9 * 3  # year * RCPs

    # Climate impact, non time series
    cimp_non_ts_var = nuts3_output[
        nuts3_output["var_name"] == "cimp_historical_probability_of_heatwaves_mean"
    ]
    assert (
        len(cimp_non_ts_var) == 1
    )  # year (["2020", "2025", "2030", "2035", "2040", "2045", "2050", "2075", "2099"]) * RCPs

    # Climate impact, time series
    cimp_ts_var = nuts3_output[
        nuts3_output["var_name"] == "cimp_ts_heatwaves_intensity_mean"
    ]
    assert (
        len(cimp_ts_var) == 8 * 3
    )  # year ("2025", "2030", "2035", "2040", "2045", "2050", "2075", "2100",) * RCPs

    # Collected var
    coll_var = nuts3_output[nuts3_output["var_name"] == "population"]
    assert len(coll_var) == 1

    # Collected var
    eucalc_var = nuts3_output[
        nuts3_output["var_name"] == "eucalc_agr_emissions_n2o_crop_fertilizer"
    ]
    assert len(eucalc_var) == 7 * 2  # years * pathways
