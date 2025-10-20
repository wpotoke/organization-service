from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class ActivityCreate(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=155)]
    parent_id: int | None = Field(None, description="ID родительской деятельности. None для корневого уровня")


class Acivity(BaseModel):
    id: Annotated[int, Field(...)]
    name: str
    parent_id: int | None = None
    is_active: Annotated[bool, Field(default=True)]
    level: int = Field(..., ge=1, le=3)

    model_config = ConfigDict(from_attributes=True)
