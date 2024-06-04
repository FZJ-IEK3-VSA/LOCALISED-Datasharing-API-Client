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
    save_path = os.path.join(os.path.dirname(__file__))
    output_df = client.get_region_data(
        api_key,
        country_code="de",
        region_code=region_code,
        result_format="df",
        save_result=True,
        save_path=save_path,
    )

    # Climate Projection  #TODO

    # Collected var
    collected_df = output_df[
        (output_df["var_name"] == "relative_gross_value_added_nace_sector_l")
    ].copy()
    assert len(collected_df) == 1

    # EUCalc
    for year in [2020, 2025, 2030, 2035, 2040, 2045, 2050]:
        for pathway in ["de-lts-st-2050-05062023.json", "de-lts-bc-2050-05062023.json"]:
            eucalc_df = output_df[
                (output_df["var_name"].str.startswith("eucalc_"))
                & (output_df["year"] == year)
                & (output_df["pathway_file_name"] == pathway)
            ].copy()
            assert len(eucalc_df) == 926

    # EUCalc vars assert
    for var_name in [
        "eucalc_elc_capex_nuclear",
        "eucalc_elc_capex_res_solar_pv_utility",
        "eucalc_bld_capex_reno_off_other",
        "eucalc_elc_capex_res_other_hydroelectric",
    ]:
        eucalc_df = output_df[(output_df["var_name"] == var_name)].copy()
        assert len(eucalc_df) == 14

    # assert save
    file_name = os.path.join(save_path, "region_data.csv")
    assert os.path.exists(file_name)
    os.remove(file_name)
