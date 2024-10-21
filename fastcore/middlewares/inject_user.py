from typing import Type
from fastapi.requests import HTTPConnection
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import AuthenticationBackend

from fastcore.auth.current_user import get_current_user, get_token_user
from fastcore.abstract.abstract_user import TUser
from fastcore.request import UserRequest
from fastcore.logger import setup_logger

from logging import Logger


async def authenticate(self, conn: HTTPConnection):
    self.logger.info('Getting conn')
    if "Authorization" not in conn.headers:
        return

    auth = conn.headers["Authorization"]
    scheme, token = auth.split()
    # Only process Bearer tokens
    if scheme.lower() != "bearer":
        return

    return await get_token_user(token)


class AuthJwt(AuthenticationBackend):
    logger: Logger = None

    async def authenticate(self, conn: HTTPConnection):
        token = conn.cookies.get("access_token")
        if not token:
            return None, None

        return await get_token_user(token)


class AuthInjectUserMiddleware(AuthenticationMiddleware):
    backend: AuthJwt

    def __init__(self, app, user_model: Type[TUser], *args, **kwargs):
        super().__init__(app, backend=AuthJwt(), *args, **kwargs)
        self.user_model = user_model
        self.logger = setup_logger(__class__.__name__)
        self.logger.debug('Middleware started')
        self.backend.logger = self.logger


class BaseInjectUserMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

    async def dispatch(self, request: UserRequest, call_next):
        # Pass the specific user model to the generic `get_current_user` function
        user = await get_current_user(request, self.user_model)
        request.state.user = user
        response = await call_next(request)
        self.logger.info('Dispatching')
        return response
