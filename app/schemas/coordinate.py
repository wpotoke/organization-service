from typing import Annotated

from pydantic import BaseModel, Field


class CoordinateRectangle(BaseModel):
    lat_min: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[55.7558])]
    lat_max: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[12.28518])]
    lon_min: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[-36.2358])]
    lon_max: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[88.8128])]


class CoordinateRadius(BaseModel):
    lat: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[55.7558])]
    lon: Annotated[float, Field(..., ge=-90.0, le=90.0, examples=[-36.2358])]
    radius_km: Annotated[float | int, Field(..., ge=1, le=6371)]
