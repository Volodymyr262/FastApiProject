from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Shipment, ShipmentStatus, Seller
from app.api.schemas.shipment import ShipmentCreate
from app.services.base import BaseService
from app.services.delivery_partner import DeliveryPartnerService


class ShipmentService(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService):
        super().__init__(Shipment, session)
        self.partner_service = partner_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self, shipment_create: ShipmentCreate, seller: Seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        await self.partner_service.assign_shipment(new_shipment)

        return await self._add(new_shipment)


    async def update(self, id: int, shipment_update: dict) -> Shipment:
        shipment = await self.get(id)
        if not shipment:
            return None

        shipment.sqlmodel_update(shipment_update)

        return await self._update(shipment)


    async def delete(self, id: int) -> None:
        await self._delete(self.get(id))
