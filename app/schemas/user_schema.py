from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    is_admin: bool

    class Config:
        from_attributes = True  # Cho phép map từ SQLModel
