from pydantic import BaseModel

class QRCreate(BaseModel):
    url: str
    logo: str | None = None