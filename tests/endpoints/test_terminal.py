from bson.json_util import dumps
from bson.json_util import dumps, loads

def test_index(client):
    resp = client.simulate_get('/terminal')

    assert resp.status_code == 200
    assert len(resp.json) == 7


def test_create(client, mongodb):
    driver = mongodb.drivers.find_one()
    checkin = {
        "arrived_at": {
            "$date": '2022-12-07T15:06:23Z'
        },
        "origin": {
            "latitude": -23.550520,
            "longitude": -46.633308
        },
        "destination": {
            "latitude": -23.689842,
            "longitude": -46.564850
        },
        "driver": driver['_id']
    }

    resp = client.simulate_post('/terminal', body=dumps(checkin))

    checkin['driver'] = driver
    json = resp.json.copy()
    json.pop('_id')

    assert resp.status_code == 201
    assert loads(dumps(json)) == loads(dumps(checkin))


def test_stats(client):
    resp = client.simulate_get('/terminal/stats')

    assert resp.status_code == 200
    assert resp.json == {
        'days': [
            { '_id': '2022-11-25', 'total': 1 },
            { '_id': '2022-11-30', 'total': 1 },
            { '_id': '2022-12-6', 'total': 5 }
        ],
        'months': [
            { '_id': '2022-11', 'total': 2 },
            { '_id': '2022-12', 'total': 5 }
        ],
        'weeks': [
            { '_id': '2022-47', 'total': 1 },
            { '_id': '2022-48', 'total': 1 },
            { '_id': '2022-49', 'total': 5 }
        ]
    }


def test_trucklist(client):
    resp = client.simulate_get('/terminal/trucklist')

    assert resp.status_code == 200
    assert len(resp.json) == 2



