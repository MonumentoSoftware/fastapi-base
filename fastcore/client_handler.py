from functools import lru_cache

from fastcore.mongo_client import get_async_mongo_client
from fastcore.singleton import SingletonMeta
from fastcore.logger import setup_logger


class ClientHandler(metaclass=SingletonMeta):
    """
    A class to hold a mongodb client connection.
    It follows a singleton pattern, to avoid multiple clients.
    """

    def __init__(self, debug) -> None:
        self.debug = debug
        self.client = get_async_mongo_client(debug=self.debug)
        self.logger = setup_logger(__class__.__name__)
        self.logger.info('Client Started')


@lru_cache
def get_settings(debug: bool = True) -> 'ClientHandler':
    try:
        return ClientHandler(debug)
    finally:
        # You can handle connection closing here if needed per request,
        # otherwise manage it at the application lifecycle
        pass
