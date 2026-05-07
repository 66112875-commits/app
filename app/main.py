from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

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

from fastapi.staticfiles import StaticFiles

app.mount("/qrcodes", StaticFiles(directory="qrcodes"), name="qrcodes")
app.mount("/static", StaticFiles(directory="static"), name="static")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


@app.get("/login")
def login_page():
    return FileResponse(BASE_DIR / "frontend" / "login.html")


@app.get("/admin")
def admin_page():
    return FileResponse(BASE_DIR / "frontend" / "admin.html")

@app.get("/")
def login_page():
    return FileResponse("app/frontend/login.html")

@app.get("/dashboard")
def dashboard():
    return FileResponse("app/frontend/index.html")

##python -m uvicorn app.main:app --reload
##http://127.0.0.1:8000/login
##http://127.0.0.1:8000/admin
## eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3NzgzMDQzNX0.SfFVXHHLu7F47baHvQnoDr4PaCvASLSvmYchFdQac0I
##ขึ้น git
## git push
##git push -u origin main
##ขึ้นคราว https://dashboard.render.com/web/srv-d7t43fegvqtc73a98bog/deploys/dep-d7t43fmgvqtc73a98c90
## ขึ้นคลาว https://dashboard.render.com/web/srv-d7t43fegvqtc73a98bog/logs
## https://app-utgg.onrender.com/