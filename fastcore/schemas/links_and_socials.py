
from typing import List
from pydantic import BaseModel, Field, field_validator, HttpUrl
from enum import Enum


class LinkCategory(str, Enum):
    social = "Social"
    video = "Video"
    image = "Image"
    document = "Document"
    other = "Other"


class Link(BaseModel):
    url: HttpUrl = Field(..., description='Link to a website or asset.')
    category: LinkCategory = Field(..., description='Category of the link')


class SocialLink(Link):
    category: LinkCategory = LinkCategory.social  # Override to enforce 'Social' as category

    @field_validator('category')
    def ensure_social_category(cls, v):
        if v != LinkCategory.social:
            raise ValueError('Category must be "Social" for a SocialLink')
        return v


class SocialProfiles(BaseModel):
    links: List[Link] = Field(..., description='List of social profile links')
