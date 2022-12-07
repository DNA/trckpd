import falcon.asgi
import falcon.testing
import pytest

from truckpad.server import Server

@pytest.fixture
def client(mongodb):
    app = Server(mongodb).create()
    return falcon.testing.TestClient(app)
