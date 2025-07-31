from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from logging_config import setup_logging
from routes import users, notes, auth

setup_logging()

app = FastAPI(
    title="Notes API",
    description="A simple API to manage users and their notes.",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(notes.router)
app.include_router(auth.router)

app.mount("/", StaticFiles(directory="static", html=True), name="static")
