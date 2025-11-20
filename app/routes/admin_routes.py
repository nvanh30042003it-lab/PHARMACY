from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.core.database import get_session
from app.crud.order_crud import (
    admin_get_all_orders,
    get_order_with_items,
    confirm_order,
)
from app.schemas.order_schema import (
    OrderReadAdmin,
    OrderItemRead,
)
from app.routes.user_routes import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


def admin_required(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Chỉ admin mới được truy cập")
    return user


@router.get("/orders", response_model=list[OrderReadAdmin])
def admin_list_orders(
    session: Session = Depends(get_session),
    admin=Depends(admin_required)
):
    return admin_get_all_orders(session)


@router.get("/orders/{order_id}/items", response_model=list[OrderItemRead])
def admin_order_items(
    order_id: int,
    session: Session = Depends(get_session),
    admin=Depends(admin_required),
):
    order = get_order_with_items(session, order_id, admin=True)
    if not order:
        raise HTTPException(404, "Không tìm thấy đơn hàng")
    return order.items


@router.post("/orders/{order_id}/confirm")
def admin_confirm_order(
    order_id: int,
    session: Session = Depends(get_session),
    admin=Depends(admin_required)
):
    order = get_order_with_items(session, order_id, admin=True)
    if not order:
        raise HTTPException(404, "Không tìm thấy đơn hàng")

    confirm_order(session, order)
    order.status = "Đã xác nhận, chờ vận chuyển"  # Thêm dòng này để thay đổi trạng thái đơn hàng
    session.add(order)
    session.commit()

    return {"message": "Đã xác nhận đơn hàng"}


   

