from app.api.routers.v1.activities import router as activity_router
from app.api.routers.v1.buildings import router as building_router
from app.api.routers.v1.organizations import router as orginazation_router
from app.api.routers.v1.phones import router as phone_router

__all__ = ["activity_router", "orginazation_router", "building_router", "phone_router"]
