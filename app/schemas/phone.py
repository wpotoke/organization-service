from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PhoneCreate(BaseModel):
    phone_number: Annotated[str, Field(..., pattern=r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")]
    organization_id: Annotated[int | None, Field()] = None


class Phone(BaseModel):
    id: Annotated[int, Field(...)]
    phone_number: str
    organization_id: Annotated[int | None, Field()] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
