# Kubernetes Deployment Guide

## Prerequisites
- Have a running kubernetes instance like Docker Desktop (untested with other implementations, but should work :))
- kubectl installed

## Setup Steps

### 1. Build Docker Images

```bash
# Build parser image
docker build -f docker/parser.Dockerfile -t parser:latest .

# Build scraper image
docker build -f docker/scraper.Dockerfile -t scraper:latest .
```

### 2. Deploy to Kubernetes

```bash
# Deploy parser
kubectl apply -f k8s/parser-deployment.yaml
kubectl apply -f k8s/parser-service.yaml

# Deploy scraper
kubectl apply -f k8s/scraper-deployment.yaml
kubectl apply -f k8s/scraper-service.yaml
```
