import falcon.asgi
import falcon.testing
import pytest

from truckpad.app import create_app

@pytest.fixture
def client():
    app = create_app()
    return falcon.testing.TestClient(app)
