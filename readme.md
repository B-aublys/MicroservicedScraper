# books.toscrape.com microserviced scraper

## Local launch guide:

### Create virtual environments and install all needed packages:
```bash
# Create 2 different virtual environments for both the scraper and parser:
python -m venv parser/venv
python -m venv scraper/venv

# In two different shells enter the parsers and the scrapers virtual environments
venv\scripts\activate.ps1 # Chose the active script based on the shell that you are running on

# In the two different virtual environments install needed python libraries
pip install -r requirements.txt

```

### Start the parse and scraper
```bash
# From the root folder of the repository
# From the parser env
python -m parser

# From the scraper env
python -m scraper

```

## Kubernetes launch:

### Prerequisites
- Docker installed
- Have a running kubernetes instance like Docker Desktop (untested with other implementations, but should work :))
- kubectl installed


### 1. Build Docker Images

```bash
# Build parser image
docker build -f docker/parser.Dockerfile -t parser:latest .

# Build scraper image
docker build -f docker/scraper.Dockerfile -t scraper:latest .
```

### 2. Deploy ConfigMaps

```bash
# Deploy parser config
kubectl apply -f k8s/parser-config.yaml

# Deploy scraper config
kubectl apply -f k8s/scraper-config.yaml
```

### 3. Deploy to Kubernetes

```bash
# Deploy parser
kubectl apply -f k8s/parser-deployment.yaml
kubectl apply -f k8s/parser-service.yaml

# Deploy scraper
kubectl apply -f k8s/scraper-deployment.yaml
kubectl apply -f k8s/scraper-service.yaml
```

### 4. Check books data
All the scraped books can be found my opening the shell to the pod:
```bash
kubectl get pods
kubectl exec -it <POD-NAME> -- /bin/bash

> ls # should reveal the books_data/ folder 
```

## Structure:
Currently the scraper is divided into a different 2 projects:

- Generic scraper
    - Async crawler with configurable amount of workers.
    - Crawls recursively through all the links in the website.
    - Sends all web pages it fetches to the parsing service.

- Parsing service
    - Non-blocking parsing service, that queues parsing jobs to be done asynchronously.
    - Currently only supports books.toscrape.com, but different parsers can be plugged in to support more websites.
    - Validates the data's correctness using pydantic.
    - Writes the book's information in a folder /books_data, each book gets it's own file named after their upc. This is quite an amusing way to avoid duplicates :D as it will just write over the same file.

These services communicate through GRPC. Furthermore the concern separation is as follows:
- The Scraper is website agnostic and just crawls it.
- The Parsing service contains website knowledge and extracts data if it sees any data needing to be extracted.

Moreover on the interplay between the crawler and the parser. These two services really don't communicate much by design, the scraper just sends jobs to the parser. It is up to the parser to handle all the errors, parse data and save it, this frees up the crawler to not have to wait for parsing and fully separates their concerns.


## Kubernetes
Currently the kubernetes configuration is as follows:
- both the crawler and parser get their own deployment
    - The crawler is a CronJob that runs every 5 mins.
    - The parser is a standard service with healthches that checks the grcp service is still running.
- config maps are created for both services for their settings.

## Future improvements:
Scraper:
- Waiting for the GRPC service to be available and retrying jobs that it could not send. (Although I would probably just run a kafka, that would handle all of that.)
- Detection avoidance:
    - proxy usage
    - time delays
    - changing requests headers to seem like browser traffic

Parser:
- Adding support for more websites