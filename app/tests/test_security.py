from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token,
)
import time


def test_password_hashing():
    pwd = "mytestpassword"

    hashed = hash_password(pwd)
    assert hashed != pwd

    assert verify_password(pwd, hashed)
    assert not verify_password("wrongpass", hashed)


def test_jwt_token_creation_and_decoding():
    data = {"sub": "user123"}
    token = create_access_token(data, expires_minutes=5)

    assert isinstance(token, str)
    assert len(token) > 20

    decoded = decode_token(token)
    assert decoded and decoded.get("sub") == "user123"


def test_jwt_expired_token():
    # Create token already expired by using negative expiry
    short_token = create_access_token({"sub": "user123"}, expires_minutes=-1)
    decoded = decode_token(short_token)
    assert decoded is None
