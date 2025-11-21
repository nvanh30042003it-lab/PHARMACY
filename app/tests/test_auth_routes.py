from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    # 1. Register user
    register_res = client.post("/auth/register", json={
        "username": "authroute1",
        "password": "123456",
        "full_name": "Tester Route"
    })

    assert register_res.status_code == 200
    data = register_res.json()
    assert data["username"] == "authroute1"

    # 2. Login user (form-data)
    login_res = client.post(
        "/auth/login",
        data={
            "username": "authroute1",
            "password": "123456"
        }
    )

    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"


def test_login_wrong_password():
    res = client.post(
        "/auth/login",
        data={
            "username": "authroute1",
            "password": "wrongpass"
        }
    )

    assert res.status_code == 401


def test_login_user_not_exist():
    res = client.post(
        "/auth/login",
        data={
            "username": "notexists",
            "password": "123456"
        }
    )

    assert res.status_code == 401
