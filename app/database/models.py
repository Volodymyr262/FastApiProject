from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum
from pydantic import EmailStr

from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str, Enum):
    placed = 'placed'
    in_transit = "in_transit"
    out_for_delivery = 'out_for_delivery'
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    __tablename__ = 'shipment'

    # Move primary_key=True inside sa_column and use default_factory
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key='seller.id')

    # Define relationship to Seller
    seller: 'Seller' = Relationship(
        back_populates='shipments',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )


class Seller(SQLModel, table=True):
    __tablename__ = 'seller'

    # Move primary_key=True inside sa_column and use default_factory
    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )
    name: str
    email: EmailStr
    password_hash: str

    # Define relationship to Shipment
    shipments: list[Shipment] = Relationship(
        back_populates='seller',
        sa_relationship_kwargs={'lazy': 'selectin'},
    )