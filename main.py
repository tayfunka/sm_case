import os
from fastapi import FastAPI
from src.api.router import router
from src.core.db import Base, engine
from src.core.logging import logger
from src.core.scheduler import start_scheduler


app = FastAPI(
    title="Hello, Smart Maple!",
    description="This is a case for Smart Maple.",
    version="1.0.0",
    docs_url="/docs",
    debug=True,
)


start_scheduler()

Base.metadata.create_all(bind=engine)

app.include_router(router, prefix='/api')
