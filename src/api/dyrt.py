import asyncio
import httpx
from httpx import HTTPStatusError

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from src.schemas.campground import FetchCampgroundsRequest, FetchCampgroundsResponse
from src.services.campground import parse_campgrounds_from_response, create_campground

from src.core.db import get_db
from src.core.logging import logger

router = APIRouter()


@router.get('/fetch_campgrounds')
async def fetch_campgrounds(request: FetchCampgroundsRequest = Depends(), db: Session = Depends(get_db)):
    '''Fetch campgrounds from Dyrt API, if insert_db is True, save to database'''
    base_url = "https://thedyrt.com/api/v6/locations/search-results"
    params = request.to_params()
    max_retries = 3
    retry_delay = 2

    try:
        async with httpx.AsyncClient() as client:
            for attempt in range(max_retries):
                try:
                    response = await client.get(base_url, params=params)
                    response.raise_for_status()
                    break
                except HTTPStatusError as e:
                    logger.warning(
                        f'Attept {attempt + 1} failed with status code {response.status_code}: {e}.'
                    )
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay * (attempt + 1))
                    else:
                        logger.error(
                            f"Max retries reached. Failed to fetch data from Dyrt API: {e}")
                        raise HTTPException(response.status_code,
                                            detail="Max retries reached. Failed to fetch data from Dyrt API")

            if request.insert_db:
                campgrounds = await parse_campgrounds_from_response(response)

                for campground in campgrounds:
                    #  from campground (pydantic) to dbcampground (sqlalchemy)
                    db_campground = campground.to_db_model()

                    #  it's now dbcampground object (sqlalchemy) not campground (pydantic)
                    new_campground = create_campground(db, db_campground)

                    logger.info(
                        f"'{new_campground.id}' created in db.")

                return {"message": "Campgrounds created in db."}
            return {"count": len(response.json().get("data", []))}
    except Exception as e:
        logger.error(
            f"An error occurred while fetching data from Dyrt API: {e}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred while fetching data from Dyrt API")
