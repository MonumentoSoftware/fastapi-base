from fastapi.routing import APIRouter
from app.utils.logging import setup_logger


class BaseRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Basic Logger
        self.logger = setup_logger(__class__.__name__)
