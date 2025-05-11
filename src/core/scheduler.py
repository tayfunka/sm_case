import os
import time
import asyncio
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from src.api.dyrt import fetch_campgrounds
from src.schemas.campground import FetchCampgroundsRequest

from src.core.db import get_db
from src.core.logging import logger


def scheduled_fetch_campgrounds():
    try:
        logger.info("Scheduled task started")
        db = next(get_db())
        request = FetchCampgroundsRequest(
            component='US',
            sort='Recommended',
            page_number=1,
            page_size=1,
            insert_db=False
        )
        fetched_campgrounds = asyncio.run(
            fetch_campgrounds(request=request, db=db))
        logger.info(
            f"{fetched_campgrounds.get('count', 0)} items fetched from Dyrt API with scheduled task.")

    except Exception as e:
        logger.error(f"Error during scheduled fetch_campgrounds: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_fetch_campgrounds,
                      trigger='cron', hour='*/1')
    scheduler.start()
    logger.info("Press Control+C to exit")
