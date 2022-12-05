import json
from falcon.testing import TestClient

new_driver = {
    'name': 'Adamastor',
    'age': 38,
    'gender': 'male',
    'has_vehicle': False,
    'license_type': 'E',
    'is_loaded': True,
    'vehicle_type': 2
}


def test_index(client):
    resp = client.simulate_get('/drivers')

    assert resp.status_code == 200
    assert len(resp.json) == 6


def test_show(client, mongodb):
    assert 'drivers' in mongodb.list_collection_names()
    driver = mongodb.drivers.find_one({ 'name': 'Fulano' })

    resp = client.simulate_get('/drivers/1')

    assert resp.status_code == 200
    assert resp.json == driver


def test_create(client: TestClient, mongodb):
    resp = client.simulate_post('/drivers/1', body=json.dumps(new_driver))
    driver = mongodb.drivers.find_one({ 'name': new_driver['name'] })

    assert resp.status_code == 204
    assert driver == new_driver


def test_update(client: TestClient, mongodb):
    new_data = {
        'has_vehicle': True,
        'vehicle_type': 3
    }

    updated_driver = new_driver | new_data

    resp = client.simulate_patch('/drivers/1', body=json.dumps(new_data))

    assert resp.status_code == 200
    assert resp.json == updated_driver


def test_list_with_truck(client):
    resp = client.simulate_get('/drivers/truck')

    assert resp.status_code == 200
    assert len(resp.json) == 3


def test_list_unloaded(client):
    resp = client.simulate_get('/drivers/unloaded')

    assert resp.status_code == 200
    assert len(resp.json) == 2
