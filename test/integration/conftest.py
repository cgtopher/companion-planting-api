import pytest
from app import create_app


@pytest.fixture(autouse=True, scope="session")
def test_app():
    test_app = create_app()
    test_app.config.update({"TESTING": True})
    yield test_app


@pytest.fixture(autouse=True, scope="session")
def client(test_app):
    return test_app.test_client()
