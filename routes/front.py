from fastapi import APIRouter, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/", response_class=FileResponse, include_in_schema=False)
async def read_root():
    """Serves the main HTML file for the frontend."""
    return "static/index.html"