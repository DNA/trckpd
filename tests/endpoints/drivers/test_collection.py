import json

def test_index(client):
    resp = client.simulate_get('/drivers')

    assert resp.status_code == 200
    assert len(resp.json) == 6


def test_create(client):
    driver = {
        'name': 'Adamastor',
        'age': 38,
        'gender': 'male',
        'has_vehicle': False,
        'license_type': 'E',
        'is_loaded': True,
        'vehicle_type': 2
    }

    resp = client.simulate_post('/drivers', body=json.dumps(driver))

    assert resp.status_code == 201
    assert driver.items() <= resp.json.items()

def test_list_truck(client):
    resp = client.simulate_get('/drivers/truck')

    assert resp.status_code == 200
    assert len(resp.json) == 3


def test_list_unloaded(client):
    resp = client.simulate_get('/drivers/unloaded')

    assert resp.status_code == 200
    assert len(resp.json) == 2
