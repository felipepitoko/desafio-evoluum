# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files and to run in unbuffered mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Create a non-root user to run the application
RUN addgroup --system app && adduser --system --group app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Convert line endings, make the entrypoint script executable, and change ownership
RUN sed -i 's/\r$//' ./entrypoint.sh \
    && chmod +x ./entrypoint.sh && chown -R app:app .

# Switch to the non-root user
USER app

# Set the entrypoint script to be executed when the container starts
ENTRYPOINT ["./entrypoint.sh"]
