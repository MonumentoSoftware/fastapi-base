from fastapi import APIRouter

from dotenv import load_dotenv

from fastcore.client_handler import get_settings
from .logger import setup_logger


class AbstractRouter(APIRouter):
    client_debug: bool = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = setup_logger(self._type())

        # NOTE Assures that, we load envs and sets the client
        self.__assert_client_debug()
        self.db = get_settings(self.client_debug)

    def _type(self):
        return self.__class__.__name__

    def __assert_client_debug(self):
        load_dotenv()
        assert self.client_debug is not None, 'Please subscribe the client sebug'
