from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"


def login(data, db):
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
    if not pwd_context.verify(
        data.password,
        user.password
    ):
        return {
            "success": False,
            "message": "Email hoặc mật khẩu không chính xác"
        }

    expire = datetime.utcnow() + timedelta(minutes=30)
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {
        "success": True,
        "message": "Đăng nhập thành công",
        "access_token": token
    }