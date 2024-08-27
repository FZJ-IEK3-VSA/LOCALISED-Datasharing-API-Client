import os
import pytest
from zoomin_client import client


@pytest.mark.parametrize(
    "region_code",
    [
        ("DEA23"),
        ("DE"),
        ("DE600_02000000"),
    ],
)
def test_get_region_data(region_code):
    """Check if region data is returned."""
    save_path = os.path.join(os.path.dirname(__file__))
    output_df = client.get_region_data(
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
        for pathway in ["national", "with_behavioural_changes"]:
            eucalc_df = output_df[
                (output_df["var_name"].str.startswith("eucalc_"))
                & (output_df["year"] == year)
                & (output_df["pathway_description"] == pathway)
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


@pytest.mark.parametrize(
    "climate_experiment,pathway",
    [
        ("RCP4.5", "national"),
        ("RCP2.6", "national"),
        ("RCP4.5", "with_behavioural_changes"),
    ],
)
def test_get_region_data_with_filter(climate_experiment, pathway):
    """Check if filtered region data is returned."""

    output_df = client.get_region_data(
        country_code="de",
        region_code="DE300",
        climate_experiment=climate_experiment,
        pathway=pathway,
        result_format="df",
    )

    # Collected var
    collected_df = output_df[(output_df["var_name"] == "intertidal_flats_cover")].copy()
    assert len(collected_df) == 1
    # TODO: investigate why its not equal to 80 and fix it and then uncomment this
    # # Climate data
    # climate_df = output_df[
    #     (output_df["var_name"] == "cproj_annual_mean_maximum_temperature") # "cproj_annual_mean_minimum_temperature"
    # ].copy()

    # assert len(climate_df) == 80 # 80 years

    # EUCalc
    eucalc_df = output_df[
        (output_df["var_name"].str.startswith("eucalc_"))
        & (output_df["year"] == 2030)
        & (output_df["pathway_description"] == pathway)
    ].copy()
    assert len(eucalc_df) == 926  # 926 variables
