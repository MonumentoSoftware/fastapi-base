from functools import partial
from datetime import datetime, timezone

utc_now = partial(datetime.now, timezone.utc)


def slugify(text: str) -> str:
    """
    This function will convert the text into a slug.
    """
    return text.lower().replace(' ', '_')
