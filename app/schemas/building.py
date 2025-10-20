from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BuildingCreate(BaseModel):
    address: Annotated[str, Field(..., min_length=5, max_length=155)]
    latitude: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[55.7558])]
    longitude: Annotated[float, Field(..., ge=-180.0, le=180.0, examples=[37.6173])]


class Building(BaseModel):
    id: Annotated[int, Field(...)]
    address: str
    latitude: float
    longitude: float
    is_active: Annotated[bool, Field(default=True)]

    model_config = ConfigDict(from_attributes=True)
