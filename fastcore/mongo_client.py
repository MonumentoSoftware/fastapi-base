from functools import lru_cache
import os

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


def get_sync_mongo_client(debug=True) -> MongoClient:
    """
    This function returns a handle to the MongoDB database.
    Make sure to set the environment variables `MONGO_INITDB_ROOT_USERNAME` and
    `MONGO_INITDB_ROOT_PASSWORD` to the username and password of the MongoDB
    database.
    """
    # NOTE make sure to set the environment variables
    if debug is True:
        user = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
        password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'root')
        client = MongoClient(f'mongodb://{user}:{password}@localhost:27017')
    else:
        KEY = os.environ.get('MONGODB_API', '')
        client = MongoClient(KEY)
    return client


def get_async_mongo_client(debug=True) -> AsyncIOMotorClient:
    """
    This function returns a handle to the MongoDB database.
    Make sure to set the environment variables `MONGO_INITDB_ROOT_USERNAME` and
    `MONGO_INITDB_ROOT_PASSWORD` to the username and password of the MongoDB
    database.
    """
    # NOTE make sure to set the environment variables
    if debug is True:
        user = os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'root')
        password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'root')
        client = AsyncIOMotorClient(f'mongodb://{user}:{password}@localhost:27017')
    else:
        KEY = os.environ.get('MONGODB_API', '')
        client = AsyncIOMotorClient(KEY)
    return client


@lru_cache
def get_app_client(debug: bool):
    return get_async_mongo_client(debug=debug)
