def test_list_images(client):
    resp = client.simulate_get('/')

    assert resp.status_code == 200
    assert resp.json == {'hello': 'world'}
