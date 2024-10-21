

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class AbstractBusinessModel(BaseModel):
    """
    A model for handling business information.
    """
    name: str = Field(..., title="Business Name", min_length=2, max_length=100, description="The name of the business.")
    short_description: str = Field(None, title="Business Description", max_length=300, description="A brief description of the business.")
    address: str = Field(None, title="Business Address", max_length=200, description="The address of the business.")
    phone: str = Field(None, title="Business Phone Number", pattern=r'^\+?[1-9]\d{1,14}$', description="A valid international phone number.")
    email: EmailStr = Field(None, title="Business Email Address", description="A valid business email address.")
    website: HttpUrl = Field(None, title="Business Website URL", description="The website of the business.")
    logo: HttpUrl = Field(None, title="Business Logo URL", description="URL to the business logo.")

    model_config = {

        'title': "Abstract Business Model",
        "example": {
            "name": "Example Business",
            "short_description": "A business that does amazing things.",
            "address": "123 Example Street, City, Country",
            "phone": "+1234567890",
            "email": "info@example.com",
            "website": "https://www.example.com",
            "logo": "https://www.example.com/logo.png"
        }
    }
