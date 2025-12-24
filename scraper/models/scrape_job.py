from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ScrapeJob:
    url: str
    failed: bool = False
    tries: int = 0

    def logError(self, message: str):
        logger.error(f"Error scraping {self.url}, try {self.tries}: {message}")

    def logSuccess(self, action: str):
        logger.info(f"Successfully {action} for {self.url} in {self.tries} try")