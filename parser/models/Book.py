from pydantic import BaseModel, ConfigDict, ConfigDict, Field


class Book(BaseModel):
    """Represents a book extracted from the Books to Scrape website."""

    model_config = ConfigDict(validate_assignment=True)

    name: str = Field(..., min_length=1, description="Book title")
    available_amount: int = Field(..., ge=0, description="Number of copies available")
    price_pre_tax: float = Field(..., ge=0, description="Price before tax")
    tax: float = Field(..., ge=0, description="Tax amount")
    upc: str = Field(..., min_length=1, description="Universal Product Code")