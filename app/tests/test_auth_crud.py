from app.core.security import hash_password, verify_password, create_access_token
from app.crud.user_crud import create_user, authenticate_user
from app.core.database import engine
from sqlmodel import Session

def test_hash_and_verify_password():
    password = "123456"
    hashed = hash_password(password)

    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)


def test_authenticate_user():
    with Session(engine) as session:
        # Create test user
        user = create_user(session, username="testuser1", password="123456", full_name="Test User")

        # Correct login
        login_user = authenticate_user(session, "testuser1", "123456")
        assert login_user is not None
        assert login_user.username == "testuser1"

        # Wrong password
        wrong = authenticate_user(session, "testuser1", "wrong")
        assert wrong is None


def test_jwt_token_creation():
    token = create_access_token({"sub": "testuser1"})
    assert isinstance(token, str)
    assert len(token) > 10
