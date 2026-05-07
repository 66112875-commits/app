from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from pathlib import Path

from .database import Base, engine, SessionLocal
from .models import QRCode

from .routers.auth import router as auth_router
from .routers.qr import router as qr_router
from .routers.admin import router as admin_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(qr_router)
app.include_router(admin_router)

app.mount("/qrcodes", StaticFiles(directory="qrcodes"), name="qrcodes")
app.mount("/static", StaticFiles(directory="static"), name="static")


BASE_DIR = Path(__file__).resolve().parent


@app.get("/r/{code}")
def redirect(code: str):

    db: Session = SessionLocal()

    qr = db.query(QRCode).filter(
        QRCode.short_code == code
    ).first()

    if qr:
        qr.scan_count += 1
        db.commit()

        return RedirectResponse(qr.original_url)

    return {"error": "Not found"}


# หน้าแรก = Login
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "frontend" / "login.html")

# หน้า Login
@app.get("/login")
def login_page():
    return FileResponse(BASE_DIR / "frontend" / "login.html")

# หน้า Generator
@app.get("/dashboard")
def dashboard():
    return FileResponse(BASE_DIR / "frontend" / "index.html")

# หน้า Admin
@app.get("/admin")
def admin_page():
    return FileResponse(BASE_DIR / "frontend" / "admin.html")

##python -m uvicorn app.main:app --reload
##http://127.0.0.1:8000/login
##http://127.0.0.1:8000/admin
## eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3NzgzMDQzNX0.SfFVXHHLu7F47baHvQnoDr4PaCvASLSvmYchFdQac0I

##Push ขึ้น GitHub
##git add .
##git commit -m "add auth frontend",git commit -m "update project"
##git push

##ขึ้น git
## git push
##git push -u origin main

##ขึ้นคราว https://dashboard.render.com/web/srv-d7t43fegvqtc73a98bog/deploys/dep-d7t43fmgvqtc73a98c90
## ขึ้นคลาว https://dashboard.render.com/web/srv-d7t43fegvqtc73a98bog/logs
## https://app-utgg.onrender.com/