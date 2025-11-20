from sqlmodel import Session, select
from app.models.user_model import User
from app.core.security import hash_password, verify_password


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.exec(
        select(User).where(User.username == username)
    ).first()


def create_user(
    session: Session,
    username: str,
    password: str,
    full_name: str,
    is_admin: bool = False
) -> User:
    hashed = hash_password(password)

    user = User(
        username=username,
        hashed_password=hashed,
        full_name=full_name,
        is_admin=is_admin,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
