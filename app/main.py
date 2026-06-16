import asyncio
import random

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="FastAPI Monitoring Scaffold", version="0.1.0")


@app.get("/", tags=["meta"])
async def root() -> JSONResponse:
    await asyncio.sleep(max(0.0, random.gauss(0.05, 0.05)))
    return JSONResponse({"service": "fastapi-monitoring-scaffold", "status": "ok"})


@app.get("/healthz", tags=["health"])
async def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/readyz", tags=["health"])
async def readyz() -> JSONResponse:
    return JSONResponse({"status": "ready"})


Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
).instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
