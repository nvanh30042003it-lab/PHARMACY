from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user_model import User
from .order_item_model import OrderItem


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    total_amount: Decimal
    address: str
    phone_number: str
    payment_status: str = Field(default="Pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)

