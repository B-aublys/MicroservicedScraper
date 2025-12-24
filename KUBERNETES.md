# Kubernetes Deployment Guide

## Prerequisites
- Docker Desktop with Kubernetes enabled
- kubectl installed

## Setup Steps

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
