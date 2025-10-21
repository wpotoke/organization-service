from app.core import BusinessException, NotFoundException
from app.models import Phone as PhoneModel
from app.repositories import OrganizationRepository, PhoneRepository
from app.schemas import PhoneCreate


class PhoneService:
    def __init__(self, phone_repo: PhoneRepository, organization_repo: OrganizationRepository):
        self.phone_repo = phone_repo
        self.organization_repo = organization_repo

    async def get_all_activities(self) -> list[PhoneModel]:
        return await self.phone_repo.get_all()

    async def get_phone(self, phone_id: int) -> PhoneModel | None:
        phone = await self.phone_repo.get_by_id(phone_id)
        if not phone:
            raise NotFoundException(f"phone with id {phone_id} not found")
        return phone

    async def create_phone(self, phone_create: PhoneCreate) -> PhoneModel:
        if phone_create.organization_id:
            organization = self.organization_repo.get_by_id(phone_create.organization_id)
            if not organization:
                raise NotFoundException(
                    status_code=401,
                    detail=f"Organization with {phone_create.organization_id} not found",
                )
        return await self.phone_repo.create(phone_create)

    async def update_phone(self, phone_id: int, phone_update: PhoneCreate) -> PhoneModel:
        phone = await self.phone_repo.get_by_id(phone_id)
        if not phone:
            raise NotFoundException(f"phone with id {phone_id} not found")
        if phone_update.organization_id:
            organization = self.organization_repo.get_by_id(phone_update.organization_id)
            if not organization:
                raise NotFoundException(
                    status_code=401,
                    detail=f"Organization with {phone_update.organization_id} not found",
                )
        phone_db = await self.phone_repo.update(phone_id, phone_update)
        if not phone_db:
            raise BusinessException(detail=f"Failed to update phone with id {phone_id}")

        return phone_db

    async def delete_phone(self, phone_id: int) -> bool:
        phone = await self.phone_repo.get_by_id(phone_id)
        if not phone:
            raise NotFoundException(f"phone with id {phone_id} not found")
        return await self.phone_repo.delete(phone_id)
