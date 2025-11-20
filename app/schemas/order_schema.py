from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.schemas.user_schema import UserRead


# ====== ITEM TRONG ĐƠN HÀNG (READ) ======
class OrderItemRead(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price_at_order: float

    class Config:
        from_attributes = True


# ====== INPUT KHI TẠO ĐƠN ======
class CartItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    address: str
    phone_number: str
    cart_items: List[CartItem]


# ====== ĐƠN HÀNG CHO USER XEM ======
class OrderReadUser(BaseModel):
    id: int
    total_amount: float
    address: str
    phone_number: str
    created_at: datetime
    payment_status: str

    class Config:
        from_attributes = True


# ====== ĐƠN HÀNG CHO ADMIN XEM ======
class OrderReadAdmin(BaseModel):
    id: int
    total_amount: float
    address: str
    phone_number: str
    created_at: datetime
    payment_status: str

    user: UserRead
    items: List[OrderItemRead]

    class Config:
        from_attributes = True
