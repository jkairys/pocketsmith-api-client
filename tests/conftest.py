import pytest
from pocketsmith.client import Client
import os


@pytest.fixture(scope="session")
def client():
    """
    Configures client for testing
    """
    developer_key = os.getenv("DEVELOPER_KEY")
    if developer_key is None:
        raise RuntimeError("DEVELOPER_KEY is required env var")
    return Client(developer_key=developer_key)


@pytest.fixture(scope="session")
def user_id(client: Client) -> int:
    """
    User ID associated with developer key
    """
    return client.get_me().id
