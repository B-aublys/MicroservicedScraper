import logging
import os
from pathlib import Path
from parser.models.Book import Book

logger = logging.getLogger(__name__)

class BookDataSaver:
    """Saves book data to JSON files."""

    def __init__(self, output_dir: str = None):
        """Initialize BookDataSaver with output directory."""
     
        if output_dir is None:
            output_dir = os.getenv("BOOKS_DATA_DIR", "books_data")
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"BookDataSaver initialized with output directory: {self.output_dir}")
    
    def save_book(self, book_upc: str, book: Book) -> None:
        """Save a book to JSON file."""
     
        try:
            filename = f"{book_upc}.json"
            filepath = self.output_dir / filename
            json_data = book.model_dump_json(indent=2)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            logger.info(f"Book {book.name} saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save book: {e}")