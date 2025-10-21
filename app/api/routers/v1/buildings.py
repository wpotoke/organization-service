# ruff:noqa:UP045
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import Field

from app.core import BusinessException, NotFoundException
from app.core.dependencies.services import BuildingService, get_building_service
from app.schemas import Building, BuildingCreate

router = APIRouter(prefix="/building", tags=["building"])


@router.get("/", response_model=list[Building], status_code=status.HTTP_200_OK)
async def get_buildings(
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> list[Building]:
    return building_service.get_all_buildings()


@router.get("/{building_id}", response_model=Optional[Building], status_code=status.HTTP_200_OK)
async def get_building(
    building_id: Annotated[int, Path(ge=1)],
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> Building | None:
    try:
        return building_service.get_building(building_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.post("/", response_model=Optional[Building], status_code=status.HTTP_201_CREATED)
async def create_building(
    building_create: Annotated[BuildingCreate, Field(description="Building create data")],
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> Building | None:
    try:
        return building_service.create_building(building_create)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.put("/{building_id}", response_model=Optional[Building], status_code=status.HTTP_200_OK)
async def update_building(
    building_id: Annotated[int, Path(ge=1)],
    building_update: Annotated[BuildingCreate, Field(description="Building update data")],
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> Building | None:
    try:
        return building_service.update_building(building_id, building_update)
    except (BusinessException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.delete("/{building_id}", status_code=status.HTTP_200_OK)
async def delete_building(
    building_id: Annotated[int, Path(ge=1)],
    building_service: Annotated[BuildingService, Depends(get_building_service)],
) -> Building | None:
    try:
        res = building_service.delete_building(building_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    if res:
        return {"success": "Building success deleted"}
    return {"success": "Building not exists"}
