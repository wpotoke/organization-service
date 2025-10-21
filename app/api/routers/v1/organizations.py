# ruff:noqa:UP045,B008
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from pydantic import Field

from app.core import BusinessException, NotFoundException
from app.core.dependencies.services import OrganizationService, get_organization_service
from app.schemas import (
    CoordinateRadius,
    CoordinateRectangle,
    Organization,
    OrganizationCreate,
)

router = APIRouter(prefix="/organization", tags=["organization"])


@router.get("/radius", response_model=list[Organization])
async def get_organizations_by_radius(
    lat: Annotated[float, Query(..., description="Latitude")],
    lon: Annotated[float, Query(..., description="Longitude")],
    radius_km: Annotated[float | int, Query(..., description="Radius in km")],
    organization_service: OrganizationService = Depends(get_organization_service),
) -> list[Organization]:
    try:
        coordinates = CoordinateRadius(lat=lat, lon=lon, radius_km=radius_km)
        return await organization_service.get_organization_by_radius(coordinates)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get("/area/", response_model=list[Organization])
async def get_organizations_by_rectangle(
    lat_min: Annotated[float, Query(..., description="Min latitude")],
    lat_max: Annotated[float, Query(..., description="Max latitude")],
    lon_min: Annotated[float, Query(..., description="Min longitude")],
    lon_max: Annotated[float, Query(..., description="Max longitude")],
    organization_service: OrganizationService = Depends(get_organization_service),
) -> list[Organization]:
    try:
        coordinates = CoordinateRectangle(lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)
        return await organization_service.get_organization_by_rectangle(coordinates)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get("/", response_model=list[Organization], status_code=status.HTTP_200_OK)
async def get_organizations(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    return await organization_service.get_all_organizations()


@router.get(
    "/{organization_id}",
    response_model=Optional[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    try:
        return await organization_service.get_organization_by_id(organization_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/buildings/{building_id}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_building(
    building_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    try:
        return await organization_service.get_organization_by_building(building_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/activities/{activity_id}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_activity(
    activity_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    try:
        return await organization_service.get_organization_by_activity(activity_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.get(
    "/activity/{activity_name}",
    response_model=list[Organization],
    status_code=status.HTTP_200_OK,
)
async def get_organizations_by_activity_with_children(
    activity_name: str,
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[Organization]:
    try:
        return await organization_service.get_organizations_by_name_activity_with_children(activity_name)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.post("/", response_model=Optional[Organization], status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_create: Annotated[OrganizationCreate, Field(description="Organization create data")],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    try:
        return await organization_service.create_organization(organization_create)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.put(
    "/{organization_id}",
    response_model=Optional[Organization],
    status_code=status.HTTP_200_OK,
)
async def update_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_update: Annotated[OrganizationCreate, Field(description="Building update data")],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> Organization | None:
    try:
        return await organization_service.update_organization(organization_id, organization_update)
    except (BusinessException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.delete("/{organization_id}")
async def delete_organization(
    organization_id: Annotated[int, Path(ge=1)],
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> dict:
    try:
        res = await organization_service.delete_organization(organization_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    if res:
        return {"success": "Organization success deleted"}
    return {"success": "Organization not exists"}
