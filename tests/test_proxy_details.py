import os
import pytest
import pandas as pd
from zoomin_client import client


def test_get_proxy_details(api_key):
    result = client.get_proxy_details(
        api_key, "de", "cproj_annual_mean_temperature_cooling_degree_days"
    )

    assert len(result) == 80
