from typing import Any, Dict, Optional, Generic, TypeVar  # noqa

from fastapi import Request
from pydantic import BaseModel
from starlette.datastructures import State

from fastcore.abstract.abstract_app import AbstractApp


_TApp = TypeVar('T', bound=AbstractApp)


class AbstractUser(BaseModel):
    email: str
    password: str


class UserState(State):
    """
    A custom state class to store user-related state with better typing support.
    This inherits from the original FastAPI `State` class but enforces type safety for `user`.
    """

    def __init__(self, state: Dict[str, Any] | None = None):
        super().__init__(state)

    def set_user(self, user: AbstractUser) -> None:
        """Set the user in the state."""
        self._state['user'] = user

    def get_user(self) -> Optional[AbstractUser]:
        """Get the user from the state."""
        return self._state.get('user')

    def clear_user(self) -> None:
        """Clear the user from the state."""
        self._state.pop('user', None)


class UserRequest(Request, Generic[_TApp]):
    state: UserState
    app: AbstractApp

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state

    @property
    def user(self) -> Optional[AbstractUser]:
        """Convenient access to the current user from the state."""
        return self.state.get_user()

    def set_user(self, user: AbstractUser) -> None:
        """Set the current user into the state."""
        self.state.set_user(user)

    def clear_user(self) -> None:
        """Clear the current user from the state."""
        self.state.clear_user()
