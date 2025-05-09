import os
from fastapi import FastAPI

app = FastAPI(
    title="Hello Smart Maple!",
    description="This is a simple FastAPI application.",
    version="1.0.0",
    docs_url="/docs",
    debug=True)
