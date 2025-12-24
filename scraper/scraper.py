from . import parser_pb2
from . import parser_pb2_grpc
from bs4 import BeautifulSoup
from scraper.models.scrape_job import ScrapeJob
from urllib.parse import urljoin
import aiohttp
import asyncio
import grpc
import logging

logger = logging.getLogger(__name__)


class Scraper:
    """Async web scraper that recursivelly crawls website urls and sends HTML to a gRPC parsing service."""
    
    def __init__(self, url: str, max_tries: int, num_workers: int, parser_server: str):
        self.max_tries = max_tries
        self.num_workers = num_workers
        self.url = url

        self.session: aiohttp.ClientSession = None
        self.active_workers = 0

        self.discovered_urls: set[str] = set()
        self.job_queue: asyncio.Queue[ScrapeJob] = asyncio.Queue()
        self.job_queue.put_nowait(ScrapeJob(url=url))
        
        self.parser_stub = parser_pb2_grpc.WebsiteParserStub(grpc.aio.insecure_channel(parser_server))


    async def run(self) -> None:
        """Start scraping workers and wait until all jobs complete."""
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            tasks = [asyncio.create_task(self.scrape()) for _ in range(self.num_workers)]

            while not (self.job_queue.empty() and self.active_workers == 0):
                await asyncio.sleep(1)

            for _ in range(self.num_workers):
                await self.job_queue.put(None)

            await asyncio.gather(*tasks)
        
    async def scrape(self) -> None:
        """Worker coroutine that processes jobs from the queue."""

        job = None

        while True:
            try:
                job = await self.job_queue.get()
                if job is None:
                    break

                self.active_workers += 1
                await self.run_job(job)

            except Exception as e:
                if job:
                    job.logError(str(e))
                    job.failed = True
                    if job.tries <= self.max_tries:
                        await self.job_queue.put(job)
                else:
                    logger.error(f"Unexpected error: {e}")
            finally:
                self.active_workers -= 1
                self.job_queue.task_done()

    async def run_job(self, job: ScrapeJob) -> None:
        """Execute a scraping job: fetch webpage, send to parser, extract links."""

        job.tries += 1
        async with self.session.get(job.url) as response:
            response.raise_for_status()
            job.logSuccess("fetched webpage")
            html = await response.text()
            await self.add_new_jobs(job, html)
            await self.send_to_parser(job, html)

    async def send_to_parser(self, job: ScrapeJob, html: str) -> None:
        """Send HTML content to the parser service via gRPC"""

        try:
            request = parser_pb2.ParseRequest(
                url=job.url,
                html_content=html
            )
            parse_response = await self.parser_stub.ParseWebsite(request)
            
            if parse_response.error:
                logger.error(f"Parser error for {job.url}: {parse_response.error}")
            else:
                logger.info(f"Successfully called the parsing service for {job.url}")
                
        except Exception as e:
            logger.error(f"Error occured sending data to parse the GRCP server for {job.url}: {e}")

    async def add_new_jobs(self, job: ScrapeJob, html: str) -> None:
        """Extract links from HTML and add them to the job queue"""

        try:
            soup = BeautifulSoup(html, 'html.parser')

            for link in soup.find_all('a', href=True):
                url = urljoin(job.url, link['href'])
                if url not in self.discovered_urls:
                    self.discovered_urls.add(url)
                    await self.job_queue.put(ScrapeJob(url=url))

            job.logSuccess("extracted urls")

        except Exception as e:
            job.logError(f"Error extracting links: {e}")