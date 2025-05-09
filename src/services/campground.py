from sqlalchemy.orm import Session
from src.models.campground import Campground
from src.schemas.campground import CampgroundRequest


def create_campground(db: Session, campground: CampgroundRequest):
    db_campground = Campground(**campground.dict())
    db.add(db_campground)
    db.commit()
    db.refresh(db_campground)
    return db_campground


def get_campground(db: Session, campground_id: str):
    return db.query(Campground).filter(Campground.id == campground_id).first()
