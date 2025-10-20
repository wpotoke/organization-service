from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Phone as PhoneModel,
)
from app.schemas import PhoneCreate


class PhoneRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[PhoneModel]:
        result = await self.db.scalars(select(PhoneModel))
        return result.all()

    async def get_by_id(self, phone_id: int) -> PhoneModel | None:
        result = await self.db.scalars(select(PhoneModel).where(PhoneModel.id == phone_id))
        return result.first()

    async def create(self, phone_create: PhoneCreate) -> PhoneModel:
        phone_db = PhoneModel(**phone_create.model_dump())
        self.db.add(phone_db)
        await self.db.commit()
        await self.db.refresh(phone_db)
        return phone_db

    async def update(self, phone_id: int, phone_update: PhoneCreate) -> PhoneModel:
        result = await self.db.execute(
            update(PhoneModel).where(PhoneModel.id == phone_id).values(**phone_update.model_dump())
        )
        await self.db.commit()
        if result.rowcount > 0:
            return await self.get_by_id(phone_id)
        return None

    async def delete(self, phone_id: int) -> bool:
        result = self.db.execute(update(PhoneModel).where(PhoneModel.id == phone_id).values(is_active=False))
        await self.db.commit()
        return result.rowcount > 0
