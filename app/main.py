from fastapi import FastAPI

from app.api.routers import (
    activity_router,
    building_router,
    orginazation_router,
    phone_router,
)

app = FastAPI(title="Oragization API", version="0.1.0")

app.include_router(building_router)
app.include_router(phone_router)
app.include_router(activity_router)
app.include_router(orginazation_router)


@app.get("/")
async def greet():
    return {"Reponse": "Hello this organization app, add /docs to you url for view docs"}
