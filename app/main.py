from fastapi import FastAPI
from app.routes import router  # Import router từ routes.py

# Khởi tạo ứng dụng FastAPI ở đây, không được khởi tạo trong routes.py
app = FastAPI()

# Thêm route gốc để tránh lỗi 404 khi truy cập vào "/"
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

# Đăng ký router với ứng dụng
app.include_router(router)
