from app.core import BusinessException, NotFoundException
from app.models import Building as BuildingModel
from app.repositories import BuildingRepository
from app.schemas import BuildingCreate


class BuildingService:
    def __init__(self, building_repo: BuildingRepository):
        self.building_repo = building_repo

    async def get_all_buildings(self) -> list[BuildingModel]:
        return await self.building_repo.get_all()

    async def get_building(self, building_id: int) -> BuildingModel | None:
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise NotFoundException(detail=f"Building with id {building_id} not found")
        return building

    async def create_building(self, building_create: BuildingCreate) -> BuildingModel:
        return await self.building_repo.create(building_create)

    async def update_building(self, building_id: int, building_update: BuildingCreate) -> BuildingModel:
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise NotFoundException(detail=f"building with id {building_id} not found")
        building_db = await self.building_repo.update(building_id, building_update)
        if not building_db:
            raise BusinessException(detail=f"Failed to update building with id {building_id}")

        return building_db

    async def delete_building(self, building_id: int) -> bool:
        building = await self.building_repo.get_by_id(building_id)
        if not building:
            raise NotFoundException(detail=f"building with id {building_id} not found")
        return await self.building_repo.delete(building_id)
