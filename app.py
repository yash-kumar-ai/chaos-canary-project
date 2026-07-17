from fastapi import FastAPI, Response, status
import os

app = FastAPI()

# Read the application version from an Environment Variable
VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.get("/")
def read_root():
    return {"service": "payment-api", "version": VERSION, "status": "running"}

@app.get("/health")
def health_check(response: Response):
    # This endpoint is crucial! Kubernetes and Prometheus will check this.
    return {"status": "healthy", "version": VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)