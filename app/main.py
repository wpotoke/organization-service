from fastapi import Depends, FastAPI

from app.api.routers import (
    activity_router,
    building_router,
    orginazation_router,
    phone_router,
)
from app.core.dependencies.auth import verify_apikey

app = FastAPI(title="Organization app - API", version="0.1.0", dependencies=[Depends(verify_apikey)])

app.include_router(building_router)
app.include_router(phone_router)
app.include_router(activity_router)
app.include_router(orginazation_router)


@app.get("/", tags=["greet"])
async def greet():
    return {"Reponse": "Hello this organization app, add /docs to you url for view docs"}
