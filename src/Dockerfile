# Stage 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# Stage 2: Production
FROM python:3.12-slim AS production

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy the application code
COPY . .

# Set environment variable
ENV ENVIRONMENT=production

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app from main/src.py where `app = FastAPI()`
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
