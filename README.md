# FastAPI Monitoring Scaffold

This repository contains a small FastAPI service wired into Prometheus, Grafana, and k6 with Docker Compose.

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
- Grafana provisioning so Prometheus and a k6 dashboard are available immediately

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

## Provisioned Grafana

Grafana starts with:

- a preconfigured Prometheus datasource
- a provisioned `Load Testing/k6 Overview` dashboard from files in `telemetry/grafana`

No Grafana UI setup is required.

## Load testing

This scaffold includes a `k6` load test that ramps concurrent virtual users until the app starts failing or latency degrades. The `k6` container streams metrics to Prometheus with the official remote-write output, and Grafana reads those metrics live from Prometheus.

Start the app stack first:

```bash
docker compose up --build
```

Run the breakpoint test in another terminal:

```bash
docker compose --profile loadtest run --rm k6
```

Then open Grafana at `http://localhost:3000` and view `Load Testing / k6 Overview`.

Useful overrides:

```bash
docker compose --profile loadtest run --rm \
  -e TARGET_PATH=/healthz \
  -e WAIT_SECONDS=0 \
  k6
```

The k6 service is preconfigured with:

- `K6_PROMETHEUS_RW_SERVER_URL=http://prometheus:9090/api/v1/write`
- `K6_PROMETHEUS_RW_TREND_AS_NATIVE_HISTOGRAM=true`
- `K6_PROMETHEUS_RW_STALE_MARKERS=false`

If you run `k6` on the host instead of through Compose, use:

```bash
K6_PROMETHEUS_RW_SERVER_URL=http://localhost:9090/api/v1/write \
K6_PROMETHEUS_RW_TREND_AS_NATIVE_HISTOGRAM=true \
K6_PROMETHEUS_RW_STALE_MARKERS=false \
k6 run -o experimental-prometheus-rw loadtest/breakpoint.js
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
