from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.security import create_access_token
from app.crud.user_crud import authenticate_user


def login_user(session: Session, username: str, password: str) -> dict:
    user = authenticate_user(session, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tên đăng nhập hoặc mật khẩu!",
        )

    token = create_access_token({"sub": user.username})
    return {
        "access_token": token,
        "token_type": "bearer",
    }
