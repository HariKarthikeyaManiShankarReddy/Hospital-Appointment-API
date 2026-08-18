# Multi-stage Dockerfile optimized for smaller final image and fewer vulnerabilities

FROM python:3.11-slim AS builder

WORKDIR /app

# Install build-time dependencies only in the builder stage
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry in the builder to export a requirements file
RUN pip install --no-cache-dir "poetry>=1.2"

# Copy dependency manifests first to leverage layer caching
COPY pyproject.toml poetry.lock* /app/

# Export runtime dependencies (exclude dev) and build wheels for faster/clean installs
RUN poetry export -f requirements.txt --without-hashes --without dev -o requirements.txt
RUN pip wheel --wheel-dir /wheels -r requirements.txt

# Final image: keep it slim and free of build tools
FROM python:3.11-slim

WORKDIR /app

# Install any minimal runtime packages (e.g. libpq for Postgres). Remove if not required.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd --create-home appuser

# Copy built wheels and requirements from builder and install without network access
COPY --from=builder /wheels /wheels
COPY --from=builder /app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r /app/requirements.txt

# Copy application code and set ownership
COPY . /app
RUN chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Run the app, binding to 0.0.0.0 so port mappings from the host work
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
