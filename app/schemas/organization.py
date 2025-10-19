import re
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.activity import Acivity
from app.schemas.building import Building


class OrganizationCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=5, max_length=155)]
    phones: Annotated[list[str], Field(...)]
    building_id: Annotated[int, Field(..., ge=1, le=15)]
    activity_ids: Annotated[list[int], Field(..., min_length=1)]

    @field_validator("phone_numbers")
    @classmethod
    def validate_phones(cls, value):
        pattern = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
        for phone in value:
            if not re.match(pattern, phone):
                raise ValueError(f"Incorrect format of phone number {phone}")


class Organization(BaseModel):
    id: Annotated[int, Field(...)]
    name: str
    phones: list[str]
    building: Building
    activities: list[Acivity]

    model_config = ConfigDict(from_attributes=True)
