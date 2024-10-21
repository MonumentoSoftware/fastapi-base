from pydantic import BaseModel
from typing import TypeVar


# NOTE It is also ok to get the starlette SimpleUser

class AbstractUser(BaseModel):
    username: str
    password: str


TUser = TypeVar('TUser', bound=AbstractUser)
