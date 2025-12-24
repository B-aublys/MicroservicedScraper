import logging
from concurrent.futures import ThreadPoolExecutor
import parser.parser_pb2 as parser_pb2
import parser.parser_pb2_grpc as parser_pb2_grpc
from .data_saver import BookDataSaver
from .website_parsers.books_to_scrape_scraper import BooksToScrapeParser

logger = logging.getLogger(__name__)


class WebsiteParserServicer(parser_pb2_grpc.WebsiteParserServicer):
    """gRPC service that parses websites."""
    
    def __init__(self, num_workers: int) -> None:
        """Initialize parser servicer."""

        self.saver = BookDataSaver()
        self.parser = BooksToScrapeParser()
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
    
    def _parse_async(self, url: str, html_content: str) -> None:
        """Parse and save book asynchronously."""

        try:
            parsed_data = self.parser.parse(html_content)
            
            if parsed_data.success:
                self.saver.save_book(parsed_data.data.upc, parsed_data.data)
                logger.info(f"Successfully parsed {url}")

            elif parsed_data.error == "Not a product page":
                logger.info(f"URL {url} is not a product page, skipping.")

            else:
                logger.error(f"Failed to parse {url}: {parsed_data.error}")
        
        except Exception as e:
            logger.error(f"Error parsing {url}: {e}")
    
    def ParseWebsite(self, request, context) -> parser_pb2.ParseResponse:
        """Parse website HTML content asynchronously."""
        try:
            logger.info(f"Queued parsing for {request.url}")
            self.executor.submit(self._parse_async, request.url, request.html_content)
            return parser_pb2.ParseResponse(url=request.url)
        except Exception as e:
            return parser_pb2.ParseResponse(url=request.url, error=str(e))
