import os
from fastapi import FastAPI
from src.api.router import router
from src.core.db import Base, engine

app = FastAPI(
    title="Hello Smart Maple!",
    description="This is a simple FastAPI application.",
    version="1.0.0",
    docs_url="/docs",
    debug=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix='/api')
