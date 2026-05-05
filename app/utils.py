import random
import string
import qrcode
from PIL import Image
import os

# ✅ เพิ่มอันนี้ (แก้ error)
def generate_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ QR + LOGO
def generate_qr_with_logo(url: str, filepath: str, logo_path: str = None):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path)

        qr_w, qr_h = img.size
        size = qr_w // 4
        logo = logo.resize((size, size))

        pos = ((qr_w - size) // 2, (qr_h - size) // 2)

        img.paste(logo, pos)

    img.save(filepath)