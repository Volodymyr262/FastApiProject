from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from app.database.models import ShipmentStatus


# Base model with shared fields
class ShipmentBase(SQLModel):
    destination: int
    content: str
    weight: float

class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(SQLModel):
    content: Optional[str] = None
    destination: Optional[int] = None
    weight: Optional[float] = None
    estimated_delivery: Optional[datetime] = None
    status: Optional[str] = None