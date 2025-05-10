from fastapi import APIRouter
from src.api import campground
from src.api import dyrt

router = APIRouter()

router.include_router(
    campground.router,
    prefix="/campground",
    tags=["campground"],
)

router.include_router(
    dyrt.router,
    prefix='/dyrt',
    tags=['dyrt'],
)
