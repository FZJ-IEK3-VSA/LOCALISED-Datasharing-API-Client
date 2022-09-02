import os
import pytest
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope="session")
def api_key():
    # find .env automagically by walking up directories until it's found
    dotenv_path = find_dotenv()
    # load up the entries as environment variables
    load_dotenv(dotenv_path)

    api_key = os.environ.get("SECRET_API_KEY")
    return api_key
