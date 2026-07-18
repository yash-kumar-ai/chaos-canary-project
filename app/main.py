from fastapi import FastAPI
import socket

app = FastAPI(
    title="Chaos Canary Deployer",
    description="Production-inspired DevOps platform demonstrationg canary deployments, observability, and chaos engineering.",
    version="1.0.0"
)

HOSTNAME = socket.gethostname()

@app.get("/")
def home():
    return {
        "message": "Welcome to Chaos Canary API",
        "version": "v1",
        "hostname": "HOSTNAME"
    }
@app.get("/version")
def version():
    return {
        "version": "v1",
        "hostname": "HOSTNAME"
    }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
