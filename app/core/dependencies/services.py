# ruff:noqa:B008
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies.db import get_async_db
from app.repositories import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
    PhoneRepository,
)
from app.services import (
    ActivityService,
    BuildingService,
    OrganizationService,
    PhoneService,
)


def get_activity_service(db: AsyncSession = Depends(get_async_db)) -> ActivityService:
    return ActivityService(activity_repo=ActivityRepository(db=db))


def get_building_service(db: AsyncSession = Depends(get_async_db)) -> BuildingService:
    return BuildingService(building_repo=BuildingRepository(db=db))


def get_organization_service(db: AsyncSession = Depends(get_async_db)):
    return OrganizationService(
        organization_repo=OrganizationRepository(db=db),
        building_repo=BuildingRepository(db=db),
        activity_repo=ActivityRepository(db=db),
    )


def get_phone_service(db: AsyncSession = Depends(get_async_db)):
    return PhoneService(
        phone_repo=PhoneRepository(db=db),
        organization_repo=OrganizationRepository(db=db),
    )
