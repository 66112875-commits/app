from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import User

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# ================= DB =================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ================= CURRENT USER =================

def get_current_user(

    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)

):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token"
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.username == username
    ).first()

    if user is None:
        raise credentials_exception

    return user

# ================= ADMIN =================

def get_current_admin(

    user: User = Depends(get_current_user)

):

    if user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return user