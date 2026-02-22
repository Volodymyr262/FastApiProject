from fastapi import APIRouter
from fastapi import HTTPException, status
from app.api.schemas.shipment import ShipmentUpdate, ShipmentCreate
from app.database.models import Shipment

from app.api.dependencies import ShipmentServiceDep, SellerDep

router = APIRouter(prefix='/shipment', tags=['Shipment'])



@router.get("/", response_model=Shipment)
async def get_shipment(
        id: int,
        service: ShipmentServiceDep,
        _: SellerDep,
):
    # Check for shipment with given id
    shipment = await service.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment

@router.post("/")
async def submit_shipment(
        seller: SellerDep,
        shipment: ShipmentCreate,
        service: ShipmentServiceDep
) -> Shipment:
    return await service.add(shipment)


@router.patch("/", response_model=Shipment)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, service: ShipmentServiceDep):
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No data provided',
        )

    shipment = await service.update(id, update)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {id} not found"
        )

    return shipment

@router.delete("/")
async def delete_shipment(id: int, service: ShipmentServiceDep) -> dict[str, str]:
    # Remove from database
    await service.delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}

