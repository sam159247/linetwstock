from fastapi import FastAPI
from mangum import Mangum

from app.api.api import api_router
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root() -> dict:
    return {
        "message": "OK",
        "env": settings.ENV,
    }


app.include_router(api_router)

handler = Mangum(app)
