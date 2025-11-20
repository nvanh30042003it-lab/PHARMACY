from fastapi import APIRouter, Depends, Form, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.schemas.token_schema import Token
from app.schemas.user_schema import UserCreate, UserRead
from app.crud.auth_crud import login_user
from app.crud.user_crud import create_user
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại")

    user = create_user(
        session,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name
    )
    return user


@router.post("/login", response_model=Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    return login_user(session, username, password)
