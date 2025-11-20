from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from decimal import Decimal

if TYPE_CHECKING:
    from .order_model import Order


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)

    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int

    product_name: str
    quantity: int
    price_at_order: Decimal

