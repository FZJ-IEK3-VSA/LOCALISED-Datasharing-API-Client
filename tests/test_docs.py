import requests


def test_api_documentation():
    """Check if the docs are displayed."""
    request_url = f"http://data.localised-project.eu/api/v1/docs"

    response = requests.get(request_url)
    assert response.ok
