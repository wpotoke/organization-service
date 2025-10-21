# ruff:noqa:E712
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Activity as ActivityModel,
)
from app.schemas import ActivityCreate


class ActivityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[ActivityModel]:
        result = await self.db.scalars(select(ActivityModel).where(ActivityModel.is_active == True))
        return result.all()

    async def get_by_id(self, activity_id: int) -> ActivityModel | None:
        result = await self.db.scalars(
            select(ActivityModel).where(ActivityModel.id == activity_id, ActivityModel.is_active == True)
        )
        return result.first()

    async def get_by_name(self, name: str) -> ActivityModel | None:
        result = await self.db.scalars(
            select(ActivityModel).where(ActivityModel.name == name, ActivityModel.is_active == True)
        )
        return result.first()

    async def create(self, activity_create: ActivityCreate) -> ActivityModel:
        activity_db = ActivityModel(**activity_create.model_dump())
        self.db.add(activity_db)
        await self.db.commit()
        await self.db.refresh(activity_db)
        return activity_db

    async def update(self, activity_id: int, activity_update: ActivityCreate) -> ActivityModel:
        result = await self.db.execute(
            update(ActivityModel)
            .where(ActivityModel.id == activity_id)
            .values(**activity_update.model_dump())
        )
        await self.db.commit()
        if result.rowcount > 0:
            return await self.get_by_id(activity_id)
        return None

    async def delete(self, activity_id: int) -> bool:
        result = await self.db.execute(
            update(ActivityModel).where(ActivityModel.id == activity_id).values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
