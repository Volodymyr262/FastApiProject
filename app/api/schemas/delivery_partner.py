from pydantic import BaseModel, EmailStr, Field


class BaseDeliveryPartner(BaseModel):
    name: str
    email: EmailStr
    servicable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseDeliveryPartner):
    pass


class DeliveryPartnerUpdate(BaseModel):
    servicable_zip_codes: list[int]
    max_handling_capacity: int


class DeliveryPartnerCreate(BaseDeliveryPartner):
    password: str = Field(max_length=72)
