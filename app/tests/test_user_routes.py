from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token(username="userroute1", password="123456"):
    # Register
    client.post("/auth/register", json={
        "username": username,
        "password": password,
        "full_name": "User Route"
    })

    # Login
    res = client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )

    return res.json()["access_token"]


def test_get_me():
    token = get_token()

    res = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    data = res.json()

    assert data["username"] == "userroute1"
    assert "full_name" in data


def test_get_me_unauthorized():
    res = client.get("/users/me")  # no token
    # depending on dependency/header validation this may be 401 or 422
    assert res.status_code in (401, 422)
