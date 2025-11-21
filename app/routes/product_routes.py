from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.crud.product_crud import (
    get_all_products,
    get_product,
    create_product,
    update_product,
    delete_product,
)
from app.schemas.product_schema import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
)
from app.routes.user_routes import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


# ============= PUBLIC ================
@router.get("/", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)):
    return get_all_products(session)


# ============= ADMIN CHECK ===========
def admin_required(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(403, "Bạn không có quyền admin")
    return user


# ============= ADMIN CRUD =============
@router.get("/admin", response_model=list[ProductRead])
def admin_list_products(
    session: Session = Depends(get_session),
    admin=Depends(admin_required)
):
    return get_all_products(session)


@router.get("/admin/{product_id}", response_model=ProductRead)
def admin_get_product(
    product_id: int,
    session: Session = Depends(get_session),
    admin=Depends(admin_required)
):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(404, "Không tìm thấy sản phẩm")
    return product


# ============= PUBLIC: get single product =============
@router.get("/{product_id}", response_model=ProductRead)
def get_single_product(
    product_id: int,
    session: Session = Depends(get_session),
):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(404, "Không tìm thấy sản phẩm")
    return product


@router.post("/admin", response_model=ProductRead)
def admin_create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    admin=Depends(admin_required),
):
    return create_product(session, data.dict())


@router.put("/admin/{product_id}", response_model=ProductRead)
def admin_update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
    admin=Depends(admin_required),
):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(404, "Không tìm thấy sản phẩm")

    return update_product(session, product, data.dict(exclude_unset=True))


@router.delete("/admin/{product_id}")
def admin_delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    admin=Depends(admin_required)
):
    product = get_product(session, product_id)
    if not product:
        raise HTTPException(404, "Không tìm thấy sản phẩm")

    delete_product(session, product)
    return {"message": "Đã xóa sản phẩm"}
