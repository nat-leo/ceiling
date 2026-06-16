# FastAPI Monitoring Scaffold

This repository contains a small FastAPI service wired into Prometheus and Grafana with Docker Compose.

## What is included

- A FastAPI app with:
  - `/healthz` for liveness
  - `/readyz` for readiness
  - `/metrics` for Prometheus scraping
- A Docker image for the app
- A Compose stack with:
  - FastAPI on `http://localhost:8000`
  - Prometheus on `http://localhost:9090`
  - Grafana on `http://localhost:3000`
- Grafana datasource provisioning so Prometheus is available immediately

## Start the stack

```bash
docker compose up --build
```

## Endpoints

- App root: `http://localhost:8000/`
- Health: `http://localhost:8000/healthz`
- Ready: `http://localhost:8000/readyz`
- Metrics: `http://localhost:8000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Grafana login

- Username: `admin`
- Password: `admin`

## Load testing

This scaffold includes a `k6` load test that ramps concurrent virtual users until the app starts failing or latency degrades.

Start the app stack first:

```bash
docker compose up --build
```

Run the breakpoint test in another terminal:

```bash
docker compose --profile loadtest run --rm k6
```

Useful overrides:

```bash
docker compose --profile loadtest run --rm \
  -e TARGET_PATH=/healthz \
  -e WAIT_SECONDS=0 \
  k6
```

The default script:

- ramps from 10 to 300 concurrent virtual users
- treats more than 5% failed requests as a failure
- treats p95 latency above 750ms as a failure

If you want a true breaking-point run, raise the stages and lower `WAIT_SECONDS` in [loadtest/breakpoint.js](/Users/natleo/Desktop/ceiling/loadtest/breakpoint.js).

For fixed concurrency testing, use [loadtest/constant.js](/Users/natleo/Desktop/ceiling/loadtest/constant.js):

```bash
docker compose --profile loadtest run --rm k6 \
  run --vus 100 --duration 30s /scripts/constant.js
```
