
from bs4 import BeautifulSoup
import re

from parser.models.ExtractionResult import ExtractionResult
from parser.models.Book import Book
from parser.website_parsers.Utilities import NumberExtractor, TableExtractor


class BooksToScrapeParser:
    """Parses book product pages from books.toscrape.com."""

    def __init__(self):
        """Initialize parser with extraction utilities."""

        self.number_extractor = NumberExtractor()
        self.table_extractor = TableExtractor()
    
    def parse(self, html_content) -> ExtractionResult:
        """Parse HTML content and extract book data."""

        soup = BeautifulSoup(html_content, 'html.parser')
        product_article = soup.find('article', class_='product_page')
        
        if not product_article:
            return ExtractionResult(success=False, error='Not a product page')
        
        try:
            table = soup.find('table', class_='table')
            if not table:
                return ExtractionResult(success=False, error='Product details table not found')
            
            result = ExtractionResult(
                success=True,
                data=Book(
                    name=self.extract_title(soup),
                    upc=self.table_extractor.extract_from_table(table, 'UPC'),
                    price_pre_tax=self.number_extractor.float_from_text(
                        self.table_extractor.extract_from_table(table, 'Price (excl. tax)')),
                    tax=self.number_extractor.float_from_text(
                        self.table_extractor.extract_from_table(table, 'Tax')),
                    available_amount=self.number_extractor.int_from_text(
                        self.table_extractor.extract_from_table(table, 'Availability')) or 0
                ))
            
            return result
            
        except Exception as e:
            return ExtractionResult(success=False, error=f'Failed to parse product page: {str(e)}')
    
    def extract_title(self, soup) -> str:
        """Extract title from product page."""

        product_main = soup.find('div', class_='product_main')
        return product_main.h1.string.strip() if product_main else None
    
    def extract_availability(self, soup) -> int:
        """Extract available stock amount."""

        availability_text = self.table_extractor.extract_from_table(soup, 'Availability')
        match = re.search(r'In stock \((\d+) available\)', availability_text)
        return int(match.group(1)) if match else 0