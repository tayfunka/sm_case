from src.schemas.dyrt import FetchCampgroundsResponse
from src.services.campground import create_campground
from src.models.campground import DBCampground
from src.core.logging import logger


db_fields = [
    "name", "latitude", "longitude", "region-name", "administrative-area",
    "nearest-city-name", "operator", "photo-url", "photo-urls", "photos-count",
    "rating", "reviews-count", "slug", "price-low", "price-high",
    "accommodation-type-names", "camper-types", "bookable"
]


async def get_campgrounds_from_fetch_campground_response(response: FetchCampgroundsResponse) -> list:
    '''Get required fields from Dyrt response'''
    try:
        campgrounds_data = response.json().get("data", [])
        if not campgrounds_data:
            logger.error("No 'data' key found in response or 'data' is empty")
            raise ValueError(
                "Invalid response format: 'data' key is missing or empty")

        campgrounds = []
        for campground_data in campgrounds_data:
            campground_attributes = campground_data.get("attributes", {})
            if not campground_attributes:
                logger.error(
                    f"No 'attributes' key found in campground data: {campground_data}")
                raise ValueError(
                    "Invalid response format: 'attributes' key is missing")

            campground = DBCampground(
                id=campground_data.get("id"),
                type=campground_data.get("type", "campground"),
                name=campground_attributes.get("name", "Unknown Campground"),
                latitude=campground_attributes.get("latitude", 0.0),
                longitude=campground_attributes.get("longitude", 0.0),
                region_name=campground_attributes.get(
                    "region-name", "Unknown Region"),
                administrative_area=campground_attributes.get(
                    "administrative-area", "Unknown Area"),
                nearest_city_name=campground_attributes.get(
                    "nearest-city-name", "Unknown City"),
                accommodation_type_names=campground_attributes.get(
                    "accommodation-type-names", []),
                bookable=campground_attributes.get("bookable", False),
                camper_types=campground_attributes.get("camper-types", []),
                operator=campground_attributes.get(
                    "operator", "Unknown Operator"),
                photo_url=campground_attributes.get("photo-url", ""),
                photo_urls=campground_attributes.get("photo-urls", []),
                photos_count=campground_attributes.get("photos-count", 0),
                rating=campground_attributes.get("rating", 0.0),
                reviews_count=campground_attributes.get("reviews-count", 0),
                slug=campground_attributes.get("slug", ""),
                price_low=campground_attributes.get("price-low", "0.00"),
                price_high=campground_attributes.get("price-high", "0.00"),
            )
            campgrounds.append(campground)
        logger.info(f"{len(campgrounds)} campgrounds fetched from Dyrt API")
        return campgrounds
    except Exception as e:
        logger.error(f"Error processing response: {e}")
        raise
