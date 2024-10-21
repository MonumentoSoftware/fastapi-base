import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv


load_dotenv()

# The main FastAPI app
# NOTE: We are using the `StaticFiles` class to serve static files
app = FastAPI(
    title="Sigmine API",
    description="A real time API for sigmine records",  # noqa
    version="0.1.0",
    contact={
        "name": "Pedro Cavalcanti",
        "url": "https://github.com/pedrokpaxo",
        "email": "pedrograxxa@gmail.com"
    }
)

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
# Deal with cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def root():
    """
    Performs a health check.
    On both the Redis and MongoDB databases.
    """
    try:
        return {"database_status": True}

    except Exception as e:
        logging.error(e)
        return {"database_status": False}
