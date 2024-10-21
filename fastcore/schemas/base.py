from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from bson import ObjectId
from typing import Optional
from .utils import utc_now


class HasId(BaseModel):
    """
    A abstract model to handle MongoDB responses
    """
    id: Optional[ObjectId] = Field(alias='_id')

    model_config = {
        'arbitrary_types_allowed': True
    }

    @field_serializer('id', when_used='json')
    def serialize_object_id(self, value: ObjectId) -> str:
        return str(value)


class BaseGeometricModel(BaseModel):
    """
    A base Abstract model to use with geometric models
    """
    geometry: dict


class TimeStampedModel(HasId):
    """
    Model with id field and created_at, and updated at.
    """
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    model_config = {
        'from_attributes': True
    }

    def save(self):
        """
        Updates the updated_at field.
        """
        self.updated_at = utc_now()
