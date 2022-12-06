import falcon.asgi
import falcon.testing
import pytest

from truckpad.app import create_app
from truckpad.config import Config

@pytest.fixture
def client(mongodb):
    config = Config()
    app = create_app(config, mongodb)
    return falcon.testing.TestClient(app)
