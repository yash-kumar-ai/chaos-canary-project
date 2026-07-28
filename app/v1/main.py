from fastapi import FastAPI
import socket
import os

app = FastAPI(
    title="Chaos Canary Deployer",
    description="Production-inspired DevOps platform demonstrationg canary deployments, observability, and chaos engineering.",
    version="1.0.0"
)

HOSTNAME = socket.gethostname()

APP_NAME =os.getenv("APP_NAME", "Chaos Canary API")
APP_VERSION = os.getenv("APP_VERSION", "v1")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

@app.get("/")
def home():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": HOSTNAME
    }
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
