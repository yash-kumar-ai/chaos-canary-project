#importing base image using slim to save space 
FROM python:3.12-slim

#set work directory
WORKDIR /app

#copying requirements file
COPY requirements.txt .

#installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the application
COPY . .

# Exposing FastAPI port
EXPOSE 8000

#Running application with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]