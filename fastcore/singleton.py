from threading import Lock


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                try:
                    # Attempt to create the singleton instance
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
                except Exception as e:
                    # Handle the exception gracefully if instance creation fails
                    # Optionally re-raise or log the error
                    raise e
        return cls._instances[cls]
