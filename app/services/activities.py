from app.core import BusinessException, NotFoundException
from app.models import Activity as ActivityModel
from app.repositories import ActivityRepository
from app.schemas import ActivityCreate


class ActivityService:
    def __init__(self, activity_repo: ActivityRepository):
        self.activity_repo = activity_repo

    async def get_all_activities(self) -> list[ActivityModel]:
        return await self.activity_repo.get_all()

    async def get_activity(self, activity_id: int) -> ActivityModel | None:
        activity = await self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise NotFoundException(f"Activity with id {activity_id} not found")
        return activity

    async def create_activity(self, activity_create: ActivityCreate) -> ActivityModel:
        if activity_create.parent_id:
            activity = await self.activity_repo.get_by_id(activity_create.parent_id)
            if not activity:
                raise NotFoundException(
                    status_code=401,
                    detail=f"Activity with {activity_create.parent_id} not found",
                )
        return await self.activity_repo.create(activity_create)

    async def update_activity(self, activity_id: int, activity_update: ActivityCreate) -> ActivityModel:
        activity = await self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise NotFoundException(f"Activity with id {activity_id} not found")
        if activity_update.parent_id:
            activity = await self.activity_repo.get_by_id(activity_update.parent_id)
            if not activity:
                raise NotFoundException(
                    status_code=401,
                    detail=f"Activity with {activity_update.parent_id} not found",
                )
        activity_db = await self.activity_repo.update(activity_id, activity_update)
        if not activity_db:
            raise BusinessException(detail=f"Failed to update activity with id {activity_id}")

        return activity_db

    async def delete_activity(self, activity_id: int) -> bool:
        activity = await self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise NotFoundException(f"Activity with id {activity_id} not found")
        return await self.activity_repo.delete(activity_id)
