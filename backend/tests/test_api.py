from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json()['status'] == 'E-Setu API running'


def test_citizen_phone_login_and_reward_tracking():
    client = TestClient(app)
    phone = '+919999000111'

    signup_response = client.post('/auth/citizen/signup', json={
        'name': 'Asha',
        'phone': phone,
        'password': 'safe-pass',
    })
    assert signup_response.status_code == 200

    login_response = client.post('/auth/citizen/login', json={
        'phone': phone,
        'password': 'safe-pass',
    })
    assert login_response.status_code == 200

    dropoff_response = client.post('/dropoffs', json={
        'name': 'Demo Point',
        'ward': 'Ward 1',
        'latitude': 17.6868,
        'longitude': 83.2185,
        'qr_code': 'demo-phone-point',
    })
    assert dropoff_response.status_code == 200

    collection_response = client.post('/collections', json={
        'dropoff_point_id': dropoff_response.json()['id'],
        'phone': phone,
        'weight_kg': 2.5,
        'item_type': 'Battery',
    })
    assert collection_response.status_code == 200

    rewards_response = client.get(f'/rewards/phone/{phone}')
    assert rewards_response.status_code == 200
    assert rewards_response.json()['credits'] >= 1
