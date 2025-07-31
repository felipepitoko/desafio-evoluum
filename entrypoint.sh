#!/bin/bash

# The docker-compose depends_on with healthcheck ensures the DB is ready.
# So we can directly run our setup script.

echo "Running database migrations..."
python db_config.py

echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000
