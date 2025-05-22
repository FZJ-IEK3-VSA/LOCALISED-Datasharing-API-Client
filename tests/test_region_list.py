import os
import pytest
from zoomin_client import client
from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()
# load up the entries as environment variables
load_dotenv(dotenv_path)

dsp_version = os.environ.get("DSP_VERSION")


@pytest.mark.parametrize("spatial_resolution", ["NUTS1", "NUTS2", "NUTS3"])
def test_get_region_list(spatial_resolution):
    """Check if region list is returned."""
    output = client.get_region_metadata(
        version=dsp_version,
        country_code="lv",
        spatial_resolution=spatial_resolution,
    )
    assert output[0].get("resolution") == spatial_resolution


def test_save_regions():
    """Check if the results of get_regions() are saved properly."""
    save_path = os.path.join(os.path.dirname(__file__))
    output = client.get_region_metadata(
        version=dsp_version,
        country_code="lv",
        spatial_resolution="NUTS3",
        save_result=True,
        save_path=save_path,
    )

    assert isinstance(output, list)
    assert len(output) == 6

    file_name = os.path.join(save_path, "region_metadata.json")
    assert os.path.exists(file_name)
    os.remove(file_name)
