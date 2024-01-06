from fastapi import FastAPI

from app.core.settings import Settings
from app.v1 import v1_router


app = FastAPI(
    title=Settings.PROJECT_NAME,
    version=Settings.VERSION
)
app.include_router(v1_router)
