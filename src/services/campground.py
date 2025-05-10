from sqlalchemy.orm import Session
from src.models.campground import DBCampground
from src.schemas.campground import CampgroundRequest, Campground, PaginationParams
from fastapi import Depends


def create_campground(db: Session, campground: Campground):
    db_campground = DBCampground(
        id=campground.id,
        type=campground.type,
        name=campground.name,
        latitude=campground.latitude,
        longitude=campground.longitude,
        region_name=campground.region_name,
        administrative_area=campground.administrative_area,
        nearest_city_name=campground.nearest_city_name,
        accommodation_type_names=campground.accommodation_type_names,
        bookable=campground.bookable,
        camper_types=campground.camper_types,
        operator=campground.operator,
        photo_url=campground.photo_url,
        photo_urls=campground.photo_urls,
        photos_count=campground.photos_count,
        rating=campground.rating,
        reviews_count=campground.reviews_count,
        slug=campground.slug,
        price_low=campground.price_low,
        price_high=campground.price_high,
        availability_updated_at=campground.availability_updated_at,
    )

    db.add(db_campground)
    db.commit()
    db.refresh(db_campground)
    return db_campground


def get_campground(db: Session, campground_id: str):
    return db.query(DBCampground).filter(DBCampground.id == campground_id).first()


def get_pagination_params(pagination: PaginationParams = Depends()):
    return pagination
