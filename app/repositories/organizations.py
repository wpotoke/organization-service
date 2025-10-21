# ruff:noqa:E712
from sqlalchemy import select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    Activity as ActivityModel,
)
from app.models import (
    Building as BuildingModel,
)
from app.models import (
    Organization as OrganizationModel,
)
from app.models import (
    organization_activities,
)
from app.schemas import OrganizationCreate


class OrganizationRepository:
    COMMON_OPTIONS = [
        selectinload(OrganizationModel.activities),
        selectinload(OrganizationModel.building),
        selectinload(OrganizationModel.phones),
    ]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.scalars(
            select(OrganizationModel).where(OrganizationModel.is_active == True).options(*self.COMMON_OPTIONS)
        )
        organizations = result.all()
        return organizations

    async def get_by_building(self, building_id: int) -> list[OrganizationModel]:
        result = await self.db.scalars(
            select(OrganizationModel)
            .where(
                OrganizationModel.building_id == building_id,
                OrganizationModel.is_active == True,
            )
            .options(*self.COMMON_OPTIONS)
        )
        organizations = result.all()
        return organizations

    async def get_by_activity(self, activity_id: int) -> list[OrganizationModel]:
        result = await self.db.scalars(
            select(OrganizationModel)
            .join(
                organization_activities,
                OrganizationModel.id == organization_activities.c.organization_id,
            )
            .join(ActivityModel, organization_activities.c.activity_id == ActivityModel.id)
            .where(
                ActivityModel.id == activity_id,
                OrganizationModel.is_active == True,
                ActivityModel.is_active == True,
            )
            .options(*self.COMMON_OPTIONS)
        )
        organizations = result.all()
        return organizations

    async def get_by_radius(self, lat: float, lon: float, radius_km: float | int) -> list[OrganizationModel]:
        table_name = BuildingModel.__tablename__  # "buildings"
        result = await self.db.scalars(
            select(OrganizationModel)
            .join(BuildingModel)
            .where(
                OrganizationModel.is_active == True,
                BuildingModel.is_active == True,
                text(
                    f"""
                    6371 * acos(
                        cos(radians(:lat)) * cos(radians({table_name}.latitude)) *
                        cos(radians({table_name}.longitude) - radians(:lon)) +
                        sin(radians(:lat)) * sin(radians({table_name}.latitude))
                    ) <= :radius
                """
                ),
            )
            .params(lat=lat, lon=lon, radius=radius_km)
            .options(*self.COMMON_OPTIONS)
        )
        return result.all()

    async def get_by_rectangle(
        self,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ) -> list[OrganizationModel]:
        result = await self.db.scalars(
            select(OrganizationModel)
            .join(BuildingModel, BuildingModel.id == OrganizationModel.building_id)
            .where(
                BuildingModel.latitude.between(lat_min, lat_max),
                BuildingModel.longitude.between(lon_min, lon_max),
                OrganizationModel.is_active == True,
                BuildingModel.is_active == True,
            )
            .options(*self.COMMON_OPTIONS)
        )
        organizations = result.all()
        return organizations

    async def get_by_id(self, organization_id: int) -> OrganizationModel | None:
        result = await self.db.scalars(
            select(OrganizationModel)
            .where(
                OrganizationModel.id == organization_id,
                OrganizationModel.is_active == True,
            )
            .options(*self.COMMON_OPTIONS)
        )
        organization = result.first()
        return organization

    async def get_by_name(self, name: str) -> OrganizationModel | None:
        result = await self.db.scalars(
            select(OrganizationModel)
            .where(OrganizationModel.name == name, OrganizationModel.is_active == True)
            .options(*self.COMMON_OPTIONS)
        )
        organization = result.first()
        return organization

    async def get_by_name_activity_with_children(self, activity: ActivityModel) -> list[OrganizationModel]:
        cte = (
            select(ActivityModel)
            .where(ActivityModel.id == activity.id, ActivityModel.is_active == True)
            .cte(name="activity_tree", recursive=True)
        )
        children = select(ActivityModel).join(cte, ActivityModel.parent_id == cte.c.id)
        cte = cte.union_all(children)
        query = select(cte.c.id)
        result_activity_ids = await self.db.execute(query)
        activity_ids = [row[0] for row in result_activity_ids.fetchall()]

        organizations = await self.db.scalars(
            select(OrganizationModel)
            .join(
                organization_activities,
                OrganizationModel.id == organization_activities.c.organization_id,
            )
            .where(
                organization_activities.c.activity_id.in_(activity_ids),
                OrganizationModel.is_active == True,
            )
            .options(*self.COMMON_OPTIONS)
        )

        return organizations.all()

    async def create(self, organization_create: OrganizationCreate):
        organization_db = OrganizationModel(
            name=organization_create.name, building_id=organization_create.building_id
        )
        self.db.add(organization_db)
        await self.db.commit()
        await self.db.refresh(organization_db)

        for activity_id in organization_create.activity_ids:
            await self.db.execute(
                organization_activities.insert().values(
                    organization_id=organization_db.id,
                    activity_id=activity_id,
                )
            )
        await self.db.commit()
        return await self.get_by_id(organization_db.id)

    async def update(
        self, organization_id: int, organization_update: OrganizationCreate
    ) -> OrganizationModel:
        result = await self.db.execute(
            update(OrganizationModel)
            .where(OrganizationModel.id == organization_id)
            .values(
                name=organization_update.name,
                building_id=organization_update.building_id,
            )
        )
        await self.db.commit()

        await self.db.execute(
            organization_activities.delete().where(
                organization_activities.c.organization_id == organization_id
            )
        )

        for activity_id in organization_update.activity_ids:
            await self.db.execute(
                organization_activities.insert().values(
                    organization_id=organization_id,
                    activity_id=activity_id,
                )
            )

        await self.db.commit()

        if result.rowcount > 0:
            return await self.get_by_id(organization_id)
        return None

    async def delete(self, organization_id: int) -> bool:
        result = await self.db.execute(
            update(OrganizationModel).where(OrganizationModel.id == organization_id).values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
