# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy requirements and install dependencies
COPY requirements.txt .

# Install dependencies using legacy resolver to avoid marshmallow loop
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install --use-deprecated=legacy-resolver -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim AS production

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy the application code
COPY . .

ENV ENVIRONMENT=production

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
