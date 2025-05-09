from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.campground import CampgroundRequest, CampgroundResponse
from src.services.campground import create_campground, get_campground


router = APIRouter()


@router.get('/hello')
async def hello():
    return {"message": "Hello, World!"}


@router.get("/{campground_id}", response_model=CampgroundResponse)
def read_campground(campground_id: str, db: Session = Depends(get_db)):
    db_campground = get_campground(db, campground_id)
    if not db_campground:
        raise HTTPException(status_code=404, detail="Campground not found")

    return db_campground


@router.post("/", response_model=CampgroundResponse)
def create_new_campground(campground: CampgroundRequest,
                          db: Session = Depends(get_db)):

    return create_campground(db, campground)
