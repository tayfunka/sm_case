from fastapi import APIRouter
from api.campground import auth, book, categories, user

router = APIRouter()

router.include_router(book.router, prefix='/campground', tags=['campground'])
