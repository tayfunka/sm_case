from fastapi import APIRouter, Depends, HTTPException
from typing import List
import httpx
from sqlalchemy.orm import Session
from src.schemas.dyrt import FetchCampgroundsRequest, FetchCampgroundsResponse
from src.schemas.campground import Campground
from src.models.campground import DBCampground
from src.services.dyrt import get_campgrounds_from_fetch_campground_response
from src.services.campground import create_campground
from src.core.db import get_db
from src.core.logging import logger
import json
router = APIRouter()


@router.get('/fetch_campgrounds')
async def fetch_campgrounds(request: FetchCampgroundsRequest = Depends(), db: Session = Depends(get_db)):
    '''Fetch campgrounds from Dyrt API, if insert_db is True, save to database'''
    base_url = "https://thedyrt.com/api/v6/locations/search-results"
    params = request.to_params()
    try:
        async with httpx.AsyncClient() as client:

            response = await client.get(base_url, params=params)
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code,
                                    detail="Error fetching data from Dyrt API")

            if request.insert_db:
                response_data = response.json()
                with open("response_debug.json", "w") as json_file:
                    json.dump(response_data, json_file, indent=4)
                    logger.info(
                        "Response written to response_debug.json for debugging.")
                campgrounds = await get_campgrounds_from_fetch_campground_response(response)

                for campground in campgrounds:
                    existing_campground = db.query(DBCampground).filter(
                        DBCampground.id == campground.id).first()
                    if existing_campground:
                        logger.info(
                            f"'{existing_campground.id}' already exists in db.")
                        continue

                    db_campground = create_campground(db, campground)
                    logger.info(
                        f"'{db_campground.id}' created in db.")
                    db_campground = db.query(DBCampground).filter(
                        DBCampground.id == campground.id).first()

                    if not db_campground:
                        raise HTTPException(
                            status_code=500, detail=f"Failed to save campground to the database"
                        )
                return campgrounds
            return FetchCampgroundsResponse(**response.json())
    except Exception as e:
        logger.error(
            f"An error occurred while fetching data from Dyrt API: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching data from Dyrt API")
