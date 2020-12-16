"""
Base route file.

This script is used to call the application.
"""
from fastapi import FastAPI

from server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, tags=["User"], prefix="/User")


@app.get("/", tags=["Root"])
async def read_root():
    """Return a defaul message."""
    return {"message": "Welcome to this fantastic app!"}
