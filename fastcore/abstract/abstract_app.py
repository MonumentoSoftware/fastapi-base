from abc import ABC, abstractmethod

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from fastcore.logger import setup_logger


class AbstractApp(FastAPI, ABC):
    """
    An abstract base class for custom FastAPI apps.
    This enforces that derived classes implement specific methods for managing settings and resources.
    """
    client: AsyncIOMotorClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = setup_logger(self._type())

    def _type(self):
        return self.__class__.__name__

    @abstractmethod
    async def set_client(self):
        """Abstract method to set up custom settings, like database connections."""
        pass

    @abstractmethod
    def shutdown(self):
        """Method to close any resources like database connections."""
        pass
