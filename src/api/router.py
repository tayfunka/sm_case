from fastapi import APIRouter
from src.api import campground

router = APIRouter()

router.include_router(
    campground.router,
    prefix="/campground",
    tags=["campground"],
)
