from app.crud.product_crud import (
    create_product,
    get_product,
    update_product,
    delete_product,
    get_all_products,
)
from app.core.database import engine
from sqlmodel import Session
from app.schemas.product_schema import ProductCreate, ProductUpdate


def test_product_crud():
    with Session(engine) as session:
        # 1. Create product
        product_data = {
            "name": "Test Product",
            "description": "Test Desc",
            "price": 100,
            "stock": 10,
            "category": "Test",
        }

        product = create_product(session, product_data)
        assert product.id is not None
        assert product.name == "Test Product"

        # 2. Get product
        fetched = get_product(session, product.id)
        assert fetched is not None
        assert fetched.id == product.id

        # 3. Update product
        changes = {"name": "Updated Product"}
        updated = update_product(session, product, changes)
        assert updated.name == "Updated Product"

        # 4. List all products
        all_products = get_all_products(session)
        assert len(all_products) >= 1

        # 5. Delete product
        delete_product(session, product)

        # 6. Verify deleted
        assert get_product(session, product.id) is None
    