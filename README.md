# Pharmacy ANHDUONG

Hệ thống **Pharmacy Backend + Frontend** 

* Backend: FastAPI + SQLModel
* Frontend: HTML/Tailwind + JS
* JWT Auth, Products CRUD, Orders
* Docker deploy, Unit testing

## 🚀 Công Nghệ

**Backend:** FastAPI, SQLModel, SQLite, JWT, bcrypt
**Frontend:** TailwindCSS, HTML, Lucide Icons
**DevOps:** Dockerfile, docker-compose, pytest

## 📁 Cấu Trúc Thư Mục

```
PHARMACY/
│
├── .pytest_cache/        # Cache sinh ra khi chạy pytest
├── .ruff_cache/          # Cache của Ruff linter
├── .venv/                # Virtual environment (Python)
│
├── app/                  # Toàn bộ source backend FastAPI
│   ├── core/
│   ├── crud/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── main.py
│
├── fontend/              # Frontend (index.html, admin-dashboard.html)
│
├── tests/                # Thư mục test chính chạy pytest
│
├── uploads/              # Ảnh sản phẩm upload
│
├── .env                  # File môi trường
├── docker-compose        
├── Dockerfile            # File docker build backend
│
├── pharmacy              # File SQLite database (pharmacy.db)
├── README.md             # File README
├── requirements.txt      # Thư viện Python
```

## ⚙️ Chạy Backend

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docs API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Admin mặc định:

```
adminpharmacy / admin2003
```

## 🔐 Auth

* POST /auth/register
* POST /auth/login
* GET /users/me

## 🛍 Products API

* Public: /products
* Admin CRUD: /products/admin
* Upload ảnh: /upload/product-image

## 📦 Orders API

* User: tạo đơn, xem đơn
* Admin: xem & xác nhận đơn

## 🎨 Frontend

* index.html: giao diện khách
* admin-dashboard.html: quản trị SP & ĐH

## 🧪 Code Style & Linting

Dự án sử dụng **ruff** để format code và lint:

```
pip install ruff
ruff check .
ruff format .
```

## 🧪 Test

```
py -m pytest -q

## 🐳 Docker

```
docker-compose up --build -d
```

## ⭐ Tác giả

Pharmacy ANHDUONG
