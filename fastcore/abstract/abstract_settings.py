from abc import ABC, abstractmethod

from dotenv import load_dotenv


class AbstractSettings(ABC):

    def __init__(self) -> None:
        super().__init__()
        load_dotenv()

    @abstractmethod
    def load_settings(self):
        """Method to initialize settings such as database connections."""
        pass
