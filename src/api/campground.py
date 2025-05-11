from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.campground import PaginationParams
from src.models.campground import DBCampground, Campground
from src.services.campground import get_campground, get_pagination_params
from src.core.logging import logger
from src.services.campground import create_campground
from geopy.geocoders import Nominatim

router = APIRouter()


@router.get('/', response_model=List[Campground])
async def list_campgrounds(
        db: Session = Depends(get_db),
        pagination: PaginationParams = Depends(get_pagination_params)):
    '''List all campgrounds in DB with pagination'''
    total_count = db.query(DBCampground).count()
    logger.info(f"Total campgrounds: {total_count}")
    campgrounds = db.query(DBCampground).offset(
        pagination.page_number).limit(pagination.page_size).all()
    logger.info(
        f"Campground count: {len(campgrounds)} (limit={pagination.page_size}, offset={pagination.page_number})")
    if not campgrounds:
        raise HTTPException(status_code=404, detail="No campgrounds found")

    return campgrounds


@router.get("/{campground_id}", response_model=Campground)
def get_campground(campground_id: str, db: Session = Depends(get_db)):
    '''Get a campground by ID in DB'''
    db_campground = get_campground(db, campground_id)
    if not db_campground:
        raise HTTPException(status_code=404, detail="Campground not found")

    return db_campground


@router.post("/", response_model=Campground)
def create_new_campground(campground: Campground,
                          db: Session = Depends(get_db)):
    '''Create a new campground in DB'''
    db_campground = campground.to_db_model()  #  pydantic to sqlalchemy

    campground_in_db = db.query(DBCampground).filter(
        DBCampground.id == db_campground.id).first()
    if campground_in_db:
        raise HTTPException(
            status_code=400, detail="Campground with this ID already exists")

    new_campground = create_campground(db, db_campground)
    #  sqlalchemy to dict to json to pydantic
    return Campground.model_validate(jsonable_encoder(new_campground))


@router.patch('/{campground_id}', response_model=Campground)
async def update_campground(
        campground_id: str,
        updated_data: dict = Body({"name": "New Campground Name"}),
        db: Session = Depends(get_db)):
    '''Partially update a campground by ID'''
    db_campground = get_campground(db, campground_id)
    if not db_campground:
        raise HTTPException(status_code=404, detail="Campground not found")

    for key, value in updated_data.items():
        if hasattr(db_campground, key):
            setattr(db_campground, key, value)
        else:
            raise HTTPException(
                status_code=400, detail=f"Invalid field: {key}")

    try:
        db.commit()
        db.refresh(db_campground)
        logger.info(f"Campground '{campground_id}' updated successfully.")
        return jsonable_encoder(db_campground)

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update campground '{campground_id}': {e}")
        raise HTTPException(
            status_code=500, detail="Failed to update campground")


@router.get('/{campground_id}/address')
async def find_adress(campground_id: str, db: Session = Depends(get_db)):
    '''Get adress of a campground by ID'''
    db_campground = get_campground(db, campground_id)
    if not db_campground:
        raise HTTPException(status_code=404, detail="Campground not found")
    geolocator = Nominatim(user_agent="campground_locator")
    location = geolocator.reverse(
        f"{db_campground.latitude}, {db_campground.longitude}", exactly_one=True)
    adress = location.address
    if not adress:
        raise HTTPException(status_code=404, detail="Adress not found")
    return adress
