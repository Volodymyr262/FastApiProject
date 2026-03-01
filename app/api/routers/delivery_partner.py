from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..dependencies import get_partner_access_token, DeliveryPartnerDep, DeliveryPartnerServiceDep
from ..schemas.delivery_partner import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from ...database.redis import add_jti_to_blacklist

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(
        seller: DeliveryPartnerCreate,
        service: DeliveryPartnerServiceDep
):
    return await service.add(seller)


@router.post("/token")
async def login_delivery_partner(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: DeliveryPartnerServiceDep
):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "bearer",
    }


@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(
    partner_update: DeliveryPartnerUpdate,
    partner: DeliveryPartnerDep,
    service: DeliveryPartnerServiceDep,
):
    return await service.update(
        partner.sqlmodel_update(partner_update)
    )


@router.get("/logout")
async def logout_delivery_partner(
    token_data: Annotated[dict, Depends(get_partner_access_token)],
):
    await add_jti_to_blacklist(token_data["jti"])
    return {"Successfully logged out"}
