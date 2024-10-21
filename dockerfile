# Use an official Python runtime as a parent image
FROM python:3.10-slim as base

LABEL author="Pedro Cavalcanti"

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject.toml and poetry.lock for better caching
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies with Poetry, without dev dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the entire application code into the container
COPY . /app

# Expose the FastAPI port
EXPOSE 8000

# Healthcheck to monitor the application
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Command to run the FastAPI app with Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
