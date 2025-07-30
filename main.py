import logging
from fastapi import FastAPI
from routes import users, notes

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