# ruff:noqa:UP045
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import Field

from app.core import BusinessException, NotFoundException
from app.core.dependencies.services import PhoneService, get_phone_service
from app.schemas import Phone, PhoneCreate

router = APIRouter(prefix="/phone", tags=["phone"])


@router.get("/", response_model=list[Phone], status_code=status.HTTP_200_OK)
async def get_phones(
    phone_service: Annotated[PhoneService, Depends(get_phone_service)],
) -> list[Phone]:
    return phone_service.get_all_phones()


@router.get("/{phone_id}", response_model=Optional[Phone], status_code=status.HTTP_200_OK)
async def get_phone(
    phone_id: Annotated[int, Path(ge=1)],
    phone_service: Annotated[PhoneService, Depends(get_phone_service)],
) -> Phone | None:
    try:
        return phone_service.get_phone(phone_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.post("/", response_model=Optional[Phone], status_code=status.HTTP_201_CREATED)
async def create_phone(
    phone_create: Annotated[PhoneCreate, Field(description="Phone create data")],
    phone_service: Annotated[PhoneService, Depends(get_phone_service)],
) -> Phone | None:
    try:
        return phone_service.create_phone(phone_create)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.put("/{phone_id}", response_model=Optional[Phone], status_code=status.HTTP_200_OK)
async def update_phone(
    phone_id: Annotated[int, Path(ge=1)],
    phone_update: Annotated[PhoneCreate, Field(description="Phone update data")],
    phone_service: Annotated[PhoneService, Depends(get_phone_service)],
) -> Phone | None:
    try:
        return phone_service.update_phone(phone_id, phone_update)
    except (BusinessException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.delete("/{phone_id}", status_code=status.HTTP_200_OK)
async def delete_phone(
    phone_id: Annotated[int, Path(ge=1)],
    phone_service: Annotated[PhoneService, Depends(get_phone_service)],
) -> Phone | None:
    try:
        res = phone_service.delete_phone(phone_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    if res:
        return {"success": "Phone success deleted"}
    return {"success": "Phone not exists"}
