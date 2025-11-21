from decimal import Decimal
from sqlmodel import Session, select

from app.models.order_model import Order
from app.models.order_item_model import OrderItem
from app.models.product_model import Product
from app.models.user_model import User


# ==========================
# Tạo đơn hàng (User)
# ==========================
def create_order(session: Session, user, order_data) -> Order:
    total = Decimal(0)
    items_data: list[dict] = []

    # Support both dict-based and object-based order_data
    if isinstance(order_data, dict):
        cart_items = order_data.get("cart_items", [])
        address = order_data.get("address")
        phone_number = order_data.get("phone_number")
    else:
        cart_items = getattr(order_data, "cart_items", [])
        address = getattr(order_data, "address", None)
        phone_number = getattr(order_data, "phone_number", None)

    # 1. Kiểm tra sản phẩm + tính tiền
    for item in cart_items:
        # item may be a dict or an object
        if isinstance(item, dict):
            product_id = item.get("product_id")
            quantity = item.get("quantity")
        else:
            product_id = getattr(item, "product_id", None)
            quantity = getattr(item, "quantity", None)

        if product_id is None or quantity is None:
            raise Exception("Invalid cart item format")

        product = session.get(Product, product_id)
        if not product:
            raise Exception(f"Sản phẩm ID {product_id} không tồn tại")

        if product.stock < quantity:
            raise Exception(f"Tồn kho không đủ cho sản phẩm: {product.name}")

        price = product.price
        total += price * quantity

        items_data.append({
            "product": product,
            "quantity": quantity,
            "price": price,
        })

    # 2. Tạo order
    order = Order(
        user_id=user.id,
        total_amount=total,
        address=address,
        phone_number=phone_number,
        payment_status="Pending",
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    # 3. Tạo order items + trừ kho
    for i in items_data:
        order_item = OrderItem(
            order_id=order.id,
            product_id=i["product"].id,
            product_name=i["product"].name,
            quantity=i["quantity"],
            price_at_order=i["price"],
        )
        session.add(order_item)

        i["product"].stock -= i["quantity"]
        session.add(i["product"])

    session.commit()

    # Attach created items and user to returned order for convenience
    items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
    object.__setattr__(order, 'items', items)
    object.__setattr__(order, 'user', session.exec(select(User).where(User.id == order.user_id)).first())

    return order


# ==========================
# Lấy danh sách đơn của user
# ==========================
def get_user_orders(session: Session, user_id: int) -> list[Order]:
    return session.exec(
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    ).all()


# ==========================
# Lấy 1 order kèm items (+optional check user)
# ==========================
def get_order_with_items(
    session: Session,
    order_id: int,
    admin: bool = False,
    user_id: int | None = None,
) -> Order | None:
    order = session.exec(select(Order).where(Order.id == order_id)).first()
    if not order:
        return None

    if not admin and user_id is not None:
        if order.user_id != user_id:
            return None

    # attach items and user manually to avoid SQLModel Relationship dependencies
    items = session.exec(select(OrderItem).where(OrderItem.order_id == order.id)).all()
    # set attributes bypassing pydantic/SQLModel validation
    object.__setattr__(order, 'items', items)
    object.__setattr__(order, 'user', session.exec(select(User).where(User.id == order.user_id)).first())
    return order


# ==========================
# Admin: lấy tất cả orders
# ==========================
def admin_get_all_orders(session: Session) -> list[Order]:
    orders = session.exec(select(Order).order_by(Order.created_at.desc())).all()
    # attach user and items for each order
    for o in orders:
        object.__setattr__(o, 'user', session.exec(select(User).where(User.id == o.user_id)).first())
        object.__setattr__(o, 'items', session.exec(select(OrderItem).where(OrderItem.order_id == o.id)).all())
    return orders


# ==========================
# Admin: xác nhận đơn
# ==========================
def confirm_order(session: Session, order: Order) -> Order:
    order.payment_status = "Confirmed"
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
