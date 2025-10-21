# ruff:noqa:UP045
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import Field

from app.core import BusinessException, NotFoundException
from app.core.dependencies.services import ActivityService, get_activity_service
from app.schemas import Acivity, ActivityCreate

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/", response_model=list[Acivity], status_code=status.HTTP_200_OK)
async def get_activities(
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> list[Acivity]:
    return await activity_service.get_all_activities()


@router.get("/{activity_id}", response_model=Optional[Acivity], status_code=status.HTTP_200_OK)
async def get_activity(
    activity_id: Annotated[int, Path(ge=1)],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> Acivity | None:
    return await activity_service.get_activity(activity_id)


@router.post("/", response_model=Optional[Acivity], status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_create: Annotated[ActivityCreate, Field(description="Activity create data")],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> Acivity | None:
    try:
        return await activity_service.create_activity(activity_create)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.put("/{phone_id}", response_model=Optional[Acivity], status_code=status.HTTP_200_OK)
async def update_activity(
    activity_id: Annotated[int, Path(ge=1)],
    activity_update: Annotated[ActivityCreate, Field(description="Activity update data")],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> Acivity | None:
    try:
        return await activity_service.update_activity(activity_id, activity_update)
    except (BusinessException, NotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@router.delete("/{phone_id}", status_code=status.HTTP_200_OK)
async def delete_activity(
    activity_id: Annotated[int, Path(ge=1)],
    activity_service: Annotated[ActivityService, Depends(get_activity_service)],
) -> Acivity | None:
    try:
        res = await activity_service.delete_activity(activity_id)
    except NotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    if res:
        return {"success": "Activity success deleted"}
    return {"success": "Activity not exists"}
