from bson.json_util import dumps, loads

new_driver = {
    'age': 38,
    'gender': 'male',
    'has_vehicle': False,
    'is_loaded': True,
    'license_type': 'E',
    'name': 'Adamastor',
    'vehicle_type': 2
}

def test_show(client, mongodb):
    driver = mongodb.drivers.find_one()

    resp = client.simulate_get(f'/drivers/{driver["_id"]}')

    assert resp.status_code == 200
    assert loads(dumps(resp.json)) == loads(dumps(driver))


def test_update(client, mongodb):
    driver = mongodb.drivers.find_one({ 'has_vehicle': False })

    new_data = {
        'has_vehicle': True,
        'vehicle_type': 3
    }

    resp = client.simulate_patch(f'/drivers/{driver["_id"]}', body=dumps(new_data))

    assert resp.status_code == 200
    assert new_data.items() <= resp.json.items()
