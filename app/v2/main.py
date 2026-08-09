from fastapi import FastAPI
import socket
import time
import random 
import os
from prometheus_client import (Counter,Histogram , generate_latest, CONTENT_TYPE_LATEST)
from fastapi.responses import Response
from fastapi import HTTPException, status

app = FastAPI(
    title="Chaos Canary Deployer",
    description="Production-inspired DevOps platform demonstrationg canary deployments, observability, and chaos engineering.",
    version="1.0.0"
)

HOSTNAME = socket.gethostname()

APP_NAME =os.getenv("APP_NAME", "Chaos Canary API")
APP_VERSION = os.getenv("APP_VERSION", "v2")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status", "version"]
)

SUCCESS_COUNTER = Counter(
    "http_requests_success_total",
    "Successful HTTP requests",
    ["method", "endpoint", "status", "version"]
)

ERROR_COUNTER = Counter(
    "http_requests_error_total",
    "Failed HTTP requests",
    ["method", "endpoint", "status", "version"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint", "version"]
)
@app.get("/")
def home():

    if APP_VERSION == "v2":
        if random.random() < 0.30:
            raise HTTPException(
                status_code=500,
                detail="Simulated v2 failure"
            )
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": HOSTNAME
    }
@app.get("/fail")
def fail():
    raise HTTPException(
        status_code=500,
        detail="Simulated application failure"
    )   
@app.get("/version")
def version():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "hostname": HOSTNAME
    }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
@app.middleware("http")
async def prometheus_middleware(request, call_next):

    # Don't count Prometheus scraping itself
    if request.url.path == "/metrics":
        return await call_next(request)

    # Don't count Kubernetes health checks as application traffic
    if request.url.path == "/health":
        return await call_next(request)

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    method = request.method
    endpoint = request.url.path
    status = str(response.status_code)

    REQUEST_COUNTER.labels(
        method=method,
        endpoint=endpoint,
        status=status,
        version=APP_VERSION
    ).inc()

    REQUEST_LATENCY.labels(
        method=method,
        endpoint=endpoint,
        version=APP_VERSION
    ).observe(duration)

    if response.status_code >= 400:
        ERROR_COUNTER.labels(
            method=method,
            endpoint=endpoint,
            status=status,
            version=APP_VERSION
        ).inc()
    else:
        SUCCESS_COUNTER.labels(
            method=method,
            endpoint=endpoint,
            status=status,
            version=APP_VERSION
        ).inc()

    return response
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )