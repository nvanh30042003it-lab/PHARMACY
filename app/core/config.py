import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Pharmacy Backend"
    API_PREFIX: str = "/api"

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_PHARMACY_APP_2025")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 ngày

    # Database URL (SQLite default)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pharmacy.db")


settings = Settings()
