from pydantic import BaseModel, Field


class HasId(BaseModel):
    """
    A base class for models that have an ID field.
    It is designed to work with mongoDB because it uses the `_id` field.

    Args:
        BaseModel (_type_): _description_
    """
    id: str = Field(alias='_id', description='The unique identifier for the record.')
