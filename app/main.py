from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.core.database import create_db_and_tables, engine
from app.models.user_model import User
from app.crud.user_crud import create_user

# ROUTES
from app.routes.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.product_routes import router as product_router
from app.routes.order_routes import router as order_router
from app.routes.admin_routes import router as admin_router

# AI
from app.routes.ai_chat_routes import router as ai_chat_router


app = FastAPI(title="Pharmacy Backend ", version="1.0.0")
app.include_router(ai_chat_router)

# ==========================
# CORS CONFIG (FIXED)
# ==========================

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://pharmacy3004.onrender.com",
    "https://pharmacy-frontend-z60m.onrender.com",  # FRONTEND RENDER
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# CREATE DEFAULT ADMIN
# ==========================

def create_default_admin():
    with Session(engine) as session:
        admin = session.exec(
            select(User).where(User.username == "adminpharmacy")
        ).first()

        if not admin:
            print("⚡ Tạo tài khoản admin mặc định...")
            create_user(
                session,
                username="adminpharmacy",
                password="admin2003",
                full_name="Admin Nhà Thuốc ",
                is_admin=True,
            )
        else:
            print("✔ Admin đã tồn tại.")

# ==========================
# STARTUP EVENT
# ==========================

@app.on_event("startup")
def startup_event():
    print("🔧 Khởi tạo database & bảng...")
    create_db_and_tables()

    print("🔐 Khởi tạo admin mặc định...")
    create_default_admin()

    print("🚀 Hệ thống backend đã sẵn sàng!")

# ==========================
# ROUTES
# ==========================

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(admin_router)

# ==========================
# ROOT
# ==========================

@app.get("/")
def root():
    return {
        "message": "Pharmacy Backend is running!",
        "status": "OK",
        "version": "1.0.0",
    }
