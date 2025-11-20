from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.user_model import User
from app.core.security import decode_token
from app.schemas.user_schema import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


def get_current_user(
    authorization: str = Header(...),
    session: Session = Depends(get_session),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Token không hợp lệ")

    token = authorization.replace("Bearer ", "")
    data = decode_token(token)
    if not data:
        raise HTTPException(401, "Token hết hạn hoặc không hợp lệ")

    user = session.exec(
        select(User).where(User.username == data["sub"])
    ).first()

    if not user:
        raise HTTPException(404, "Không tìm thấy user")

    return user


@router.get("/me", response_model=UserRead)
def read_current_user(user=Depends(get_current_user)):
    return user
