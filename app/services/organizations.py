# ruff:noqa:E712
from app.core import BusinessException, NotFoundException
from app.models import Organization as OrganizationModel
from app.repositories import (
    ActivityRepository,
    BuildingRepository,
    OrganizationRepository,
)
from app.schemas import CoordinateRadius, CoordinateRectangle, OrganizationCreate


class OrganizationService:
    def __init__(
        self,
        organization_repo: OrganizationRepository,
        building_repo: BuildingRepository,
        activity_repo: ActivityRepository,
    ):
        self.organization_repo = organization_repo
        self.building_repo = building_repo
        self.activity_repo = activity_repo

    async def get_all_organizations(self) -> list[OrganizationModel]:
        return await self.organization_repo.get_all()

    async def get_organization_by_id(self, organization_id: int) -> OrganizationModel | None:
        return await self.organization_repo.get_by_id(organization_id)

    async def get_organization_by_name(self, name: str) -> OrganizationModel | None:
        return await self.organization_repo.get_by_name(name)

    async def get_organization_by_building(self, building_id: int) -> list[OrganizationModel]:
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise NotFoundException(f"Organization with building id {building_id} not found")
        return await self.organization_repo.get_by_building(building_id)

    async def get_organization_by_activity(self, activity_id: int) -> list[OrganizationModel]:
        activity = await self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise NotFoundException(f"Organization with activity id {activity_id} not found")
        organization = await self.organization_repo.get_by_activity(activity_id)
        if not organization:
            raise NotFoundException(401, f"Organization with activity id {activity_id} not found")
        return organization

    async def get_organizations_by_name_activity_with_children(self, name: str) -> list[OrganizationModel]:
        activity = await self.activity_repo.get_by_name(name)
        if not activity:
            raise NotFoundException(f"Organization with activity name {name} not found")
        return await self.organization_repo.get_by_name_activity_with_children(name)

    async def get_organization_by_rectangle(
        self, coordinates: CoordinateRectangle
    ) -> list[OrganizationModel]:
        return await self.organization_repo.get_by_rectangle(**coordinates.model_dump())

    async def get_organization_by_radius(self, coordinates: CoordinateRadius) -> list[OrganizationModel]:
        return await self.organization_repo.get_by_radius(**coordinates.model_dump())

    async def create_organization(self, organization_create: OrganizationCreate):
        building = await self.building_repo.get_by_id(organization_create.building_id)
        if not building:
            raise NotFoundException(
                status_code=401,
                detail=f"Organization with building id {organization_create.building_id} not found",
            )
        return await self.organization_repo.create(organization_create)

    async def update_organization(
        self, organization_id: int, organization_update: OrganizationCreate
    ) -> OrganizationModel:
        organization = await self.organization_repo.get_by_id(organization_id)
        if not organization:
            raise NotFoundException(f"Organization with id {organization_id} not found")
        building = await self.building_repo.get_by_id(organization_update.building_id)
        if not building:
            raise NotFoundException(
                status_code=401,
                detail=f"Organization with building id {organization_update.building_id} not found",
            )
        organization_db = await self.organization_repo.update(organization_update)
        if not organization_db:
            raise BusinessException(detail=f"Failed to update activity with id {organization_id}")

    async def delete_organization(self, organization_id: int) -> bool:
        organization = await self.organization_repo.get_by_id(organization_id)
        if not organization:
            raise NotFoundException(f"Organization with id {organization_id} not found")
        await self.organization_repo.delete(organization_id)
