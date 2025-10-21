# ruff:noqa:B008
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.repositories import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
    PhoneRepository,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as db:
        yield db


def get_activity_repository(db: AsyncSession = Depends(get_async_db)):
    return ActivityRepository(db=db)


def get_building_repository(db: AsyncSession = Depends(get_async_db)):
    return BuildingRepository(db=db)


def get_phone_repository(db: AsyncSession = Depends(get_async_db)):
    return PhoneRepository(db=db)


def get_organization_repository(db: AsyncSession = Depends(get_async_db)):
    return OrganizationRepository(db=db)
