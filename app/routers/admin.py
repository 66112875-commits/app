from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import QRCode, User
from ..auth_core.dependencies import get_current_admin

router = APIRouter(prefix="/admin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/qrcodes")
def get_all_qr(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(QRCode).all()

@router.get("/stats")
def stats(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    total_qr = db.query(QRCode).count()
    total_scan = sum([q.scan_count for q in db.query(QRCode).all()])

    return {
        "total_qr": total_qr,
        "total_scan": total_scan
    }

@router.get("/top")
def top_qr(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return db.query(QRCode)\
        .order_by(QRCode.scan_count.desc())\
        .limit(5)\
        .all()

@router.delete("/qrcodes/{qr_id}")
def delete_qr(
    qr_id: int,
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    qr = db.query(QRCode).filter(QRCode.id == qr_id).first()

    if not qr:
        raise HTTPException(status_code=404, detail="QR not found")

    db.delete(qr)
    db.commit()

    return {"msg": "QR deleted"}

