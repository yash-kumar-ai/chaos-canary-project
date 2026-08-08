from fastapi import FastAPI
import socket
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
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
    "Total HTTP requests"
)

SUCCESS_COUNTER = Counter(
    "http_requests_success_total",
    "successful HTTP requests"
)

ERROR_COUNTER = Counter(
    "http_requests_error_total",
    "Failed HTTP requests"
)


@app.get("/")
def home():
    REQUEST_COUNTER.inc()
    SUCCESS_COUNTER.inc()

    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": HOSTNAME
    }
@app.get("/fail")
def fail():
    REQUEST_COUNTER.inc()
    ERROR_COUNTER.inc()
    
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