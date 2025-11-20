# Dockerfile
# Sử dụng base image Python 3.13-slim
FROM python:3.13-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /usr/src/app

# Sao chép và cài đặt các dependencies (requirements.txt vẫn ở ngoài)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code dự án vào thư mục làm việc
# Giả sử thư mục PHARMACY chứa thư mục app/ và file requirements.txt
COPY . .

# Mở cổng 8000
EXPOSE 8000

# Lệnh mặc định để chạy ứng dụng:
# CHÚ Ý: Cần chỉ định main:app nằm trong thư mục con 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]