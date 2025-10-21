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


def get_activity_repository(
    db: AsyncSession = Depends(get_async_db),
) -> ActivityRepository:
    return ActivityRepository(db=db)


def get_building_repository(
    db: AsyncSession = Depends(get_async_db),
) -> BuildingRepository:
    return BuildingRepository(db=db)


def get_phone_repository(db: AsyncSession = Depends(get_async_db)) -> PhoneRepository:
    return PhoneRepository(db=db)


def get_organization_repository(
    db: AsyncSession = Depends(get_async_db),
) -> OrganizationRepository:
    return OrganizationRepository(db=db)
