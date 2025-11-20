from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List




class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    full_name: str
    is_admin: bool = Field(default=False)

