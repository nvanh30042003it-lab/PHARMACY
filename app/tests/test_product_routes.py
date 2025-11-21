from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_admin_token():
    # login bằng tài khoản admin mặc định
    res = client.post(
        "/auth/login",
        data={"username": "adminpharmacy", "password": "admin2003"}
    )
    assert res.status_code == 200
    return res.json()["access_token"]


def test_create_product_admin():
    token = get_admin_token()

    res = client.post(
        "/products/admin",
        json={
            "name": "PRoute1",
            "description": "Desc",
            "price": 50,
            "stock": 20,
            "category": "Test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "PRoute1"
    product_id = data["id"]

    # test get product
    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == product_id

    # test update
    update_res = client.put(
        f"/products/admin/{product_id}",
        json={"name": "PRoute1 Updated"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "PRoute1 Updated"

    # test delete
    delete_res = client.delete(
        f"/products/admin/{product_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_res.status_code == 200

    # test get deleted product
    get_res2 = client.get(f"/products/{product_id}")
    assert get_res2.status_code == 404


def test_get_all_products_public():
    res = client.get("/products")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
