from pymongo import errors, MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from fastcore.logger import setup_logger
from .mongo_client import get_sync_mongo_client, get_async_mongo_client
from dotenv import load_dotenv
from .types import CLIENTS


class MongoClientHandler:
    """
    Base class for MongoDB client. Handles connection to the database.
    """

    client: CLIENTS
    sync: bool

    def __init__(self, debug: bool = True, sync: bool = True):
        load_dotenv()
        self.sync = sync
        self.client = self.__create_client(sync=sync, debug=debug)
        self.logger = setup_logger(self.__class__.__name__)

    def __create_client(self, sync: bool, debug: bool) -> CLIENTS:
        try:
            if sync:
                client: MongoClient = get_sync_mongo_client(debug=debug)
            else:
                client: AsyncIOMotorClient = get_async_mongo_client(debug=debug)
            return client
        except Exception as e:
            raise errors.ConnectionFailure(f"Could not connect to the MongoDB database: {e}")

    def list_databases(self):
        """
        List all databases in the MongoDB client.
        """
        return self.client.list_database_names()

    def get_database(self, db_name: str):
        """
        Get a database from the MongoDB client.
        """
        return self.client[db_name]
