from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.campground import CampgroundRequest, PaginationParams
from src.models.campground import DBCampground
from src.services.campground import create_campground, get_campground, get_pagination_params
from src.core.logging import logger


router = APIRouter()


@router.get("/{campground_id}")
def read_campground(campground_id: str, db: Session = Depends(get_db)):
    db_campground = get_campground(db, campground_id)
    if not db_campground:
        raise HTTPException(status_code=404, detail="Campground not found")

    return db_campground


@router.get('/')
def list_campgrounds(
        db: Session = Depends(get_db),
        pagination: PaginationParams = Depends(get_pagination_params)):

    campgrounds = db.query(DBCampground).offset(
        pagination.offset).limit(pagination.limit).all()
    logger.info(
        f"Campground count: {len(campgrounds)} (limit={pagination.limit}, offset={pagination.offset})")
    if not campgrounds:
        raise HTTPException(status_code=404, detail="No campgrounds found")

    return campgrounds


@router.post("/")
def create_new_campground(campground: CampgroundRequest,
                          db: Session = Depends(get_db)):

    return create_campground(db, campground)
