
from dataclasses import dataclass
from parser.models.Book import Book

@dataclass
class ExtractionResult:
    """Represents the result of data extraction from a webpage."""
    success: bool
    data: Book = None
    error: str | None = None
    