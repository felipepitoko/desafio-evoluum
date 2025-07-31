import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes import users, notes, auth

# Configure logging (can be moved to a central config file later)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create FastAPI app instance
app = FastAPI(
    title="Notes API",
    description="A simple API to manage users and their notes.",
    version="1.0.0"
)

# Include routers from other files
app.include_router(users.router)
app.include_router(notes.router)
app.include_router(auth.router)

# Mount the static directory to serve frontend files (HTML, JS, CSS).
# The `html=True` argument makes it serve `index.html` for the root path.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
