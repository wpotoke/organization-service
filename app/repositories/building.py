from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Building as BuildingModel,
)
from app.schemas.building import BuildingCreate


class BuildingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[BuildingModel]:
        result = await self.db.scalars(select(BuildingModel))
        return result.all()

    async def get_by_id(self, building_id: int) -> BuildingModel | None:
        result = await self.db.scalars(select(BuildingModel).where(BuildingModel.id == building_id))
        return result.first()

    async def create(self, bulding_create: BuildingCreate) -> BuildingModel:
        building_db = BuildingModel(**bulding_create.model_dump())
        self.db.add(building_db)
        await self.db.commit()
        await self.db.refresh(building_db)
        return building_db

    async def update(self, building_id: int, building_update: BuildingCreate) -> BuildingModel:
        result = await self.db.execute(
            update(BuildingModel)
            .where(BuildingModel.id == building_id)
            .values(**building_update.model_dump())
        )
        await self.db.commit()
        if result.rowcount > 0:
            return await self.get_by_id(building_id)
        return None

    async def delete(self, building_id: int) -> bool:
        result = self.db.execute(
            update(BuildingModel).where(BuildingModel.id == building_id).values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
