from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import User

from ..auth_core.hashing import verify_password
from .jwt_handler import create_access_token
from ..auth_core.dependencies import get_current_user

router = APIRouter(prefix="/auth")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user:
        return {
            "error": "user not found"
        }

    if not verify_password(
        form_data.password,
        user.password
    ):
        return {
            "error": "wrong password"
        }

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token
    }



@router.get("/me")
def me(
    user = Depends(get_current_user)
):

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }



@router.post("/refresh")
def refresh_token(
    user = Depends(get_current_user)
):

    new_token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": new_token
    }


@router.post("/logout")
def logout():

    return {
        "message": "logout success"
    }