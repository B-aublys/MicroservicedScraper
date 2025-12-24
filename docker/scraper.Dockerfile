FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY scraper/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy scraper module
COPY scraper/ ./scraper/

EXPOSE 8080

# Run the scraper
CMD ["python", "-m", "scraper"]
