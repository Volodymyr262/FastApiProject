from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.security import oauth2_scheme
from ..dependencies import SellerServiceDep, SessionDep
from ..schemas.seller import SellerCreate, SellerRead
from ...database.models import Seller
from ...utils import decode_access_token

router = APIRouter(prefix="/seller", tags=['Seller'])

@router.post("/signup", response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    return await service.add(seller)

@router.post('/token')
async def login_seller(
        request_form: Annotated[OAuth2PasswordRequestForm ,Depends()],
        service: SellerServiceDep
):
    token = await service.token(request_form.username, request_form.password)
    return {
        'access_token': token,
        'type': 'bearer',
    }

