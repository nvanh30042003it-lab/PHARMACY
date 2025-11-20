import hashlib
import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings


# ============================
# PASSWORD HASHING (SECURE)
# ============================

def _sha256_hex(password: str) -> bytes:
    """Pre-hash bằng SHA256 để tránh lỗi unicode của bcrypt."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode()


def hash_password(password: str) -> str:
    sha = _sha256_hex(password)
    hashed = bcrypt.hashpw(sha, bcrypt.gensalt())
    return hashed.decode()


def verify_password(raw_password: str, hashed_password: str) -> bool:
    sha = _sha256_hex(raw_password)
    return bcrypt.checkpw(sha, hashed_password.encode())


# ============================
# JWT TOKEN CREATE
# ============================

def create_access_token(data: dict, expires_minutes: int = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# ============================
# JWT DECODE
# ============================

def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# OAuth2 scheme for dependency injection (used by routes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
