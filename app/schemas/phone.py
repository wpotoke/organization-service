from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class PhoneCreate(BaseModel):
    phone_number: Annotated[
        str,
        Field(
            ...,
            pattern=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
        ),
    ]
    organization_id: Annotated[int | None, Field()] = None


class Phone(BaseModel):
    id: Annotated[int, Field(...)]
    phone_number: str
    organization_id: Annotated[int | None, Field()] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
