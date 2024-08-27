from zoomin_client import client


def test_get_proxy_details():
    result = client.get_proxy_details(
        "de", "cproj_annual_mean_temperature_cooling_degree_days"
    )

    assert len(result) == 80
