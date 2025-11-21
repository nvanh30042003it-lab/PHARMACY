from sqlmodel import Session
from app.core.database import engine
from app.crud.order_crud import create_order, get_user_orders, get_order_with_items
from app.crud.product_crud import create_product
from app.crud.user_crud import create_user


def test_order_crud_basic():
    with Session(engine) as session:
        # create a test user
        user = create_user(session, username="order_tester", password="pwd", full_name="Order Tester")

        # 1. create product
        product = create_product(session, {"name": "OrderProd", "description": "Test", "price": 20, "stock": 10, "category": "Test"})

        # 2. create order via create_order (expects cart_items)
        order_data = {"cart_items": [{"product_id": product.id, "quantity": 2}], "address": "a", "phone_number": "p"}
        order = create_order(session, user, order_data)
        assert order.id is not None

        # verify stock decreased
        session.refresh(product)
        assert product.stock == 8

        # fetch order with items
        fetched = get_order_with_items(session, order.id, admin=True)
        assert fetched is not None
        assert hasattr(fetched, "items")

        # user orders
        orders = get_user_orders(session, user.id)
        assert any(o.id == order.id for o in orders)
