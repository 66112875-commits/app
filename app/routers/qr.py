from fastapi import APIRouter, UploadFile, File, Form
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import QRCode
import qrcode
from PIL import Image
import uuid
import os

router = APIRouter()

STATIC_DIR = "static"
QR_DIR = f"{STATIC_DIR}/qrcodes"
LOGO_DIR = f"{STATIC_DIR}/logos"

os.makedirs(QR_DIR, exist_ok=True)
os.makedirs(LOGO_DIR, exist_ok=True)


@router.post("/qr/")
async def create_qr(
    url: str = Form(...),
    logo: UploadFile = File(None)
):

    db: Session = SessionLocal()

    try:

        short_code = str(uuid.uuid4())[:8]


        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGBA")

        qr_w, qr_h = qr_img.size

        if logo and logo.filename:

            logo_path = f"{LOGO_DIR}/{uuid.uuid4()}.png"

            with open(logo_path, "wb") as f:
                f.write(await logo.read())

            logo_img = Image.open(logo_path).convert("RGBA")

            logo_size = qr_w // 4
            logo_img = logo_img.resize((logo_size, logo_size))

            pos = (
                (qr_w - logo_size) // 2,
                (qr_h - logo_size) // 2
            )

            qr_img.paste(logo_img, pos, mask=logo_img)

    
        filename = f"{short_code}.png"
        path = os.path.join(QR_DIR, filename)

        qr_img.save(path)

    
        db_qr = QRCode(
            original_url=url,
            short_code=short_code,
            qr_image=f"/static/qrcodes/{filename}"
        )

        db.add(db_qr)
        db.commit()
        db.refresh(db_qr)

    
        return {
            "short_link": f"http://127.0.0.1:8000/r/{short_code}",
            "qr_image": f"/static/qrcodes/{filename}"
        }

    except Exception as e:
        db.rollback()
        return {"error": str(e)}

    finally:
        db.close()