from abc import ABC, abstractmethod
from pydantic import BaseModel
from pymongo.errors import PyMongoError
from pymongo.results import InsertOneResult
from typing import TypeVar, Generic, List, Optional

from .logger import setup_logger
from .types import CLIENTS, DATABASES, COLLECTIONS

_T = TypeVar('_T', bound=BaseModel)


class AbstractRepository(ABC, Generic[_T]):
    """
    Abstract base class for repository pattern. Defines the standard CRUD operations.
    """

    @abstractmethod
    def create(self, data: dict) -> Optional[str]:
        """
        Create a new document in the collection.

        Args:
            data (dict): Data for the new document.

        Returns:
            Optional[str]: The ID of the created document, or None if creation failed.
        """
        pass

    @abstractmethod
    def read(self, query: dict) -> Optional[_T]:
        """
        Read a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            Optional[_T]: The document if found, or None if not found.
        """
        pass

    @abstractmethod
    def update(self, query: dict, data: dict) -> bool:
        """
        Update a document in the collection.

        Args:
            query (dict): Query to find the document.
            data (dict): Data to update the document.

        Returns:
            bool: True if the document was updated, False otherwise.
        """
        pass

    @abstractmethod
    def delete(self, query: dict) -> bool:
        """
        Delete a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        pass

    @abstractmethod
    def list(self, filter: dict = {}) -> List[_T]:
        """
        List documents in the collection.

        Args:
            filter (dict, optional): Filter to apply to the documents. Defaults to {}.

        Returns:
            List[_T]: List of documents matching the filter.
        """
        pass


class BaseRepository(AbstractRepository, Generic[_T]):
    """
    Base synchronous repository implementing common CRUD operations using PyMongo.
    """

    def __init__(self, client: CLIENTS, database_name: str, collection_name: str):
        """
        Initialize the repository.

        Args:
            client (CLIENTS): MongoDB client instance.
            database_name (str): Name of the database.
            collection_name (str): Name of the collection.
        """
        self.client = client
        self.database: DATABASES = client[database_name]
        self.collection: COLLECTIONS = self.database[collection_name]
        self.logger = setup_logger(self.__class__.__name__)

    def create(self, data: dict) -> Optional[str]:
        """
        Create a new document in the collection.

        Args:
            data (dict): Data for the new document.

        Returns:
            Optional[str]: The ID of the created document, or None if creation failed.
        """
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except PyMongoError as e:
            self.logger.error(f"Failed to insert document: {e}")
            return None

    def read(self, query: dict) -> Optional[_T]:
        """
        Read a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            Optional[_T]: The document if found, or None if not found.
        """
        try:
            document = self.collection.find_one(query)
            if document:
                return self.model(**document)
        except PyMongoError as e:
            self.logger.error(f"Failed to find document: {e}")
        return None

    def update(self, query: dict, data: dict) -> bool:
        """
        Update a document in the collection.

        Args:
            query (dict): Query to find the document.
            data (dict): Data to update the document.

        Returns:
            bool: True if the document was updated, False otherwise.
        """
        try:
            updated_data = {"$set": data}
            result = self.collection.update_one(query, updated_data)
            return result.modified_count > 0
        except PyMongoError as e:
            self.logger.error(f"Failed to update document: {e}")
            return False

    def delete(self, query: dict) -> bool:
        """
        Delete a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except PyMongoError as e:
            self.logger.error(f"Failed to delete document: {e}")
            return False

    def list(self, filter: dict = {}) -> List[_T]:
        """
        List documents in the collection.

        Args:
            filter (dict, optional): Filter to apply to the documents. Defaults to {}.

        Returns:
            List[_T]: List of documents matching the filter.
        """
        try:
            documents = self.collection.find(filter)
            return [self.model(**doc) for doc in documents]
        except PyMongoError as e:
            self.logger.error(f"Failed to retrieve documents: {e}")
            return []


class AsyncBaseRepository(AbstractRepository, Generic[_T]):
    """
    Base asynchronous repository implementing common CRUD operations using Motor.
    """

    def __init__(self, client: CLIENTS, database_name: str, collection_name: str, model: _T):
        """
        Initialize the repository.

        Args:
            client (CLIENTS): MongoDB client instance.
            database_name (str): Name of the database.
            collection_name (str): Name of the collection.
        """
        self.client = client
        self.database: DATABASES = client[database_name]
        self.collection: COLLECTIONS = self.database[collection_name]
        self.logger = setup_logger(f'{self.__class__.__name__}({database_name}.{collection_name})')
        self.model = model
        self.logger.info(f"Initialized repository for {database_name}.{collection_name}")

    async def create(self, data: dict) -> Optional[str]:
        """
        Create a new document in the collection.

        Args:
            data (dict): Data for the new document.

        Returns:
            Optional[str]: The ID of the created document, or None if creation failed.
        """
        try:
            result: InsertOneResult = await self.collection.insert_one(data)
            return str(result.inserted_id)
        except PyMongoError as e:
            self.logger.error(f"Failed to insert document: {e}")
            return None

    async def read(self, query: dict) -> Optional[_T]:
        """
        Read a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            Optional[_T]: The document if found, or None if not found.
        """
        try:
            document = await self.collection.find_one(query)
            if document is not None:
                return self.model(**document)
        except PyMongoError as e:
            self.logger.error(f"Failed to find document: {e}")
        return None

    async def update(self, query: dict, data: dict) -> bool:
        """
        Update a document in the collection.

        Args:
            query (dict): Query to find the document.
            data (dict): Data to update the document.

        Returns:
            bool: True if the document was updated, False otherwise.
        """
        try:
            updated_data = {"$set": data}
            result = await self.collection.update_one(query, updated_data)
            self.logger.info('Document Updated')
            return result.modified_count > 0
        except PyMongoError as e:
            self.logger.error(f"Failed to update document: {e}")
            return False

    async def delete(self, query: dict) -> bool:
        """
        Delete a document from the collection.

        Args:
            query (dict): Query to find the document.

        Returns:
            bool: True if the document was deleted, False otherwise.
        """
        try:
            result = await self.collection.delete_one(query)
            return result.deleted_count > 0
        except PyMongoError as e:
            self.logger.error(f"Failed to delete document: {e}")
            return False

    async def list(self, filter: dict = {}) -> List[_T]:
        """
        List documents in the collection.

        Args:
            filter (dict, optional): Filter to apply to the documents. Defaults to {}.

        Returns:
            List[_T]: List of documents matching the filter.
        """
        try:
            cursor = self.collection.find(filter)
            documents = await cursor.to_list(length=None)
            return [self.model(**doc) for doc in documents]
        except PyMongoError as e:
            self.logger.error(f"Failed to retrieve documents: {e}")
            return []

    async def insert_many(self, data: List[dict]) -> bool:
        """
        Insert many documents in the collection.

        Args:
            data (List[dict]): List of data for the new documents.

        Returns:
            bool: True if the documents were inserted, False otherwise.
        """
        try:
            result = await self.collection.insert_many(data)
            return len(result.inserted_ids) == len(data)
        except PyMongoError as e:
            self.logger.error(f"Failed to insert documents: {e}")
            return False
