from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.schemas import Building


class OrganizationCreate(BaseModel):
    name: Annotated[str, Field(..., min_length=5, max_length=155)]
    building_id: Annotated[int, Field(..., ge=1)]


class Organization(BaseModel):
    id: Annotated[int, Field(...)]
    name: str
    building: Building
    is_active: Annotated[bool, Field(default=True)]

    model_config = ConfigDict(from_attributes=True)
