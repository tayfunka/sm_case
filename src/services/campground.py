from sqlalchemy.orm import Session
from src.models.campground import DBCampground, Campground
from src.schemas.campground import PaginationParams
from fastapi import Depends
from src.core.logging import logger


async def parse_campgrounds_from_response(response) -> list[Campground]:
    try:
        campgrounds_data = response.json().get("data", [])
        if not campgrounds_data:
            raise ValueError("No 'data' found in response")

        campgrounds = []
        for item in campgrounds_data:
            attributes = item.get("attributes", {})
            attributes.update({
                "id": item.get("id"),
                "type": item.get("type", "campground"),
                "links": item.get("links", {})
            })
            campground = Campground(**attributes)
            campgrounds.append(campground)

        logger.info(f"{len(campgrounds)} campgrounds parsed")
        return campgrounds

    except Exception as e:
        logger.error(f"Failed to parse campgrounds: {e}")
        raise


def create_campground(db: Session, campground: DBCampground):
    try:
        campground_in_db = get_campground(db, campground.id)

        if campground_in_db:
            logger.info(
                f"Campground with id '{campground.id}' already exists in the database.")
            return campground_in_db
        else:
            db.add(campground)
            db.commit()
            db.refresh(campground)
            return campground
    except Exception as e:
        db.rollback()
        raise e


def get_campground(db: Session, campground_id: str):
    return db.query(DBCampground).filter(DBCampground.id == campground_id).first()


def get_pagination_params(pagination: PaginationParams = Depends()):
    return pagination
