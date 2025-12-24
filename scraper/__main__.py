import asyncio
import logging
import os
from .scraper import Scraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

index_url = os.getenv("SCRAPER_URL", "https://books.toscrape.com/index.html")
max_retries = int(os.getenv("SCRAPER_MAX_RETRIES", "3"))
num_workers = int(os.getenv("SCRAPER_NUM_WORKERS", "30"))
parser_server = os.getenv("GRPC_PARSER_SERVER", "localhost:50051")


async def main():
    scraper = Scraper(
        url=index_url,
        max_tries=max_retries,
        num_workers=num_workers,
        parser_server=parser_server
    )

    try:
        await scraper.run()
    except Exception as e:
        logger.error(f"Scraper failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())