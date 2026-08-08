from fastapi import FastAPI
import socket
import os
from prometheus_client import Counter,Histogram , generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from fastapi import HTTPException, status

app = FastAPI(
    title="Chaos Canary Deployer",
    description="Production-inspired DevOps platform demonstrationg canary deployments, observability, and chaos engineering.",
    version="1.0.0"
)

HOSTNAME = socket.gethostname()

APP_NAME =os.getenv("APP_NAME", "Chaos Canary API")
APP_VERSION = os.getenv("APP_VERSION", "v1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status", "version"]
)

SUCCESS_COUNTER = Counter(
    "http_requests_success_total",
    "successful HTTP requests"
    ["method", "endpoint", "status", "version"]
)

ERROR_COUNTER = Counter(
    "http_requests_error_total",
    "Failed HTTP requests"
    ["method", "endpoint", "status", "version"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds"
)
@app.get("/")
def home():
    REQUEST_COUNTER.labels(
        method="GET",
        endpoint="/",
        status="200",
        version=APP_VERSION
    ).inc()

    SUCCESS_COUNTER.labels(
        method="GET",
        endpoints="/",
        status="200",
        version=APP_VERSION
    ).inc()

    with REQUEST_LATENCY.time():
        return {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": HOSTNAME
        }

@app.get("/fail")
def fail():
    REQUEST_COUNTER.labels(
        method="GET",
        endpoint="/fail",
        status="500",
        version=APP_VERSION
    ).inc()
    ERROR_COUNTER.labels(
        method="GET",
        endpoints="/fail",
        status="500",
        version=APP_VERSION
    ).INC()
    with REQUEST_LATENCY.time():
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
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )