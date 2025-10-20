from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Activity as AcitivityModel,
)
from app.schemas import ActivityCreate


class BuildingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[AcitivityModel]:
        result = await self.db.scalars(select(AcitivityModel))
        return result.all()

    async def get_by_id(self, activity_id: int) -> AcitivityModel | None:
        result = await self.db.scalars(select(AcitivityModel).where(AcitivityModel.id == activity_id))
        return result.first()

    async def create(self, activity_create: ActivityCreate) -> AcitivityModel:
        activity_db = AcitivityModel(**activity_create.model_dump())
        self.db.add(activity_db)
        await self.db.commit()
        await self.db.refresh(activity_db)
        return activity_db

    async def update(self, activity_id: int, activity_update: ActivityCreate) -> AcitivityModel:
        result = await self.db.execute(
            update(AcitivityModel)
            .where(AcitivityModel.id == activity_id)
            .values(**activity_update.model_dump())
        )
        await self.db.commit()
        if result.rowcount > 0:
            return await self.get_by_id(activity_id)
        return None

    async def delete(self, activity_id: int) -> bool:
        result = self.db.execute(
            update(AcitivityModel).where(AcitivityModel.id == activity_id).values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
