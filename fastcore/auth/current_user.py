import os
from typing import Type
from fastapi import HTTPException
import jwt

from starlette.authentication import AuthCredentials
from fastcore.request import UserRequest
from fastcore.abstract.abstract_user import TUser, AbstractUser
from fastcore.client_handler import get_settings

import logging

SECRET_KEY = os.getenv('SECRET_KEY', 'change_me')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

logger = logging.getLogger('get_user')


async def get_token_user(token: str, user_model: Type[TUser] = AbstractUser):
    if not token:
        return None, None
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None, None

        user = await get_settings().client.get_database('users').get_collection('users').find_one({"username": username})
        if user is None:
            return None, None

        return AuthCredentials(["authenticated"]), user_model(**user)  # Return the user if everything is valid

    except jwt.ExpiredSignatureError:
        # Return None if the token has expired
        return None, None
    except jwt.PyJWTError:
        # Return None if there is any issue with the token
        return None, None


async def get_current_user(request: UserRequest, user_model: Type[TUser]):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        user = await request.app.client.get_database('users').get_collection('users').find_one({"username": username})
        if user is None:
            return None
        return user_model(**user)
    except jwt.ExpiredSignatureError:
        logger.error('Expired Token')
        return None
    except jwt.PyJWTError:
        return None


async def get_current_user_enforce(request: UserRequest):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Not authenticated")
        user = request.app.client.get_database('users').get_collection('users').find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=403, detail="Not authenticated")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Token invalid")
