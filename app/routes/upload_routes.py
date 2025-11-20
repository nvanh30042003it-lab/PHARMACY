from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import os
from uuid import uuid4

from app.routes.user_routes import get_current_user

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/product-image")
async def upload_product_image(
    image: UploadFile = File(...),
    user=Depends(get_current_user),
):
    if not user.is_admin:
        raise HTTPException(403, "Chỉ admin mới được upload ảnh")

    ext = image.filename.split(".")[-1].lower()
    if ext not in ["jpg", "jpeg", "png", "webp"]:
        raise HTTPException(400, "Chỉ hỗ trợ ảnh JPG, JPEG, PNG, WEBP")

    filename = f"{uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Ghi file
    with open(file_path, "wb") as f:
        f.write(await image.read())

    return {
        "image_url": f"/static/products/{filename}"
    }
