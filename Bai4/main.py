from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, User
from schema import LoginRequest, LoginResponse
from auth import verify_password, create_access_token

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if user is None:
        return {
            "success": False,
            "message": "Email hoặc mật khẩu không chính xác"
        }

    if not user.is_active:
        return {
            "success": False,
            "message": "Tài khoản đã bị vô hiệu hóa"
        }

    password_correct = verify_password(
        data.password,
        user.password_hash
    )

    if not password_correct:
        return {
            "success": False,
            "message": "Email hoặc mật khẩu không chính xác"
        }

    token = create_access_token(user)

    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "access_token": token,
        "token_type": "bearer"
    }