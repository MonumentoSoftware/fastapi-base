
from contextlib import asynccontextmanager
import os
from fastcore.client_handler import ClientHandler
from fastcore.abstract.abstract_app import AbstractApp


class CustomClientApp(AbstractApp):
    """
    A custom App class to better handle the database connections.
    It has a client, that is a ClientHandler class, with a singleton pattern.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger.debug('App Started')

    async def set_client(self, client_debug):
        """Set up custom settings, like database connections."""
        try:
            self.client = ClientHandler(client_debug).client
        except Exception as e:
            self.logger.error(e)

    async def shutdown(self):
        """Close any open resources (e.g., database connections)."""
        self.client.close()


@asynccontextmanager
async def ClientLifespan(app: AbstractApp):
    """
    Custom lifespan to init the app.client
    """
    DEBUG = os.getenv('DEBUG')

    await app.set_client(DEBUG)

    yield
    await app.shutdown()
