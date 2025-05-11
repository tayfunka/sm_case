from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.inspection import inspect

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from src.core.db import Base


class DBCampground(Base):
    __tablename__ = "campgrounds"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    links = Column(JSON, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region_name = Column(String, nullable=False)
    administrative_area = Column(String, nullable=True)
    nearest_city_name = Column(String, nullable=True)
    accommodation_type_names = Column(ARRAY(String), default=[])
    bookable = Column(Boolean, default=False)
    camper_types = Column(ARRAY(String), default=[])
    operator = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    photo_urls = Column(ARRAY(String), default=[])
    photos_count = Column(Integer, default=0)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    slug = Column(String, nullable=True)
    price_low = Column(Float, nullable=True)
    price_high = Column(Float, nullable=True)
    availability_updated_at = Column(DateTime, nullable=True)

    def get_required_fields(self):
        '''Get required fields from DBCampground model.'''
        mapper = inspect(self.__class__)
        return [
            column.key
            for column in mapper.columns
            if not column.nullable or column.default is None
        ]


class CampgroundLinks(BaseModel):

    self: HttpUrl


class Campground(BaseModel):
    id: str
    type: str
    name: str
    links: CampgroundLinks
    latitude: float
    longitude: float
    region_name: str = Field(None, alias="region-name")
    administrative_area: Optional[str] = Field(
        None, alias="administrative-area")
    nearest_city_name: Optional[str] = Field(None, alias="nearest-city-name")
    accommodation_type_names: List[str] = Field(
        [], alias="accommodation-type-names")
    bookable: bool = False
    camper_types: List[str] = Field([], alias="camper-types")
    operator: Optional[str] = None
    photo_url: Optional[HttpUrl] = Field(None, alias="photo-url")
    photo_urls: List[HttpUrl] = Field([], alias="photo-urls")
    photos_count: int = Field(0, alias="photos-count")
    rating: Optional[float] = None
    reviews_count: int = Field(0, alias="reviews-count")
    slug: Optional[str] = None
    price_low: Optional[float] = Field(None, alias="price-low")
    price_high: Optional[float] = Field(None, alias="price-high")
    availability_updated_at: Optional[datetime] = Field(
        None, alias="availability-updated-at"
    )
    # address: Optinal[str] = "" For bonus point

    def to_db_model(self) -> DBCampground:
        return DBCampground(**self.model_dump(mode="json"))
