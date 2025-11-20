from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.schemas.order_schema import (
    OrderCreate,
    OrderReadUser,
    OrderItemRead,
)
from app.crud.order_crud import (
    create_order,
    get_user_orders,
    get_order_with_items,
)
from app.routes.user_routes import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderReadUser)
def user_create_order(
    order_data: OrderCreate,
    user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:
        return create_order(session, user, order_data)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/", response_model=list[OrderReadUser])
def user_list_orders(
    user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return get_user_orders(session, user.id)


@router.get("/{order_id}/items", response_model=list[OrderItemRead])
def user_order_items(
    order_id: int,
    user=Depends(get_current_user),
    session: Session = Depends(get_session),
):
    order = get_order_with_items(session, order_id, user_id=user.id)
    if not order:
        raise HTTPException(404, "Không tìm thấy đơn hàng")
    return order.items
