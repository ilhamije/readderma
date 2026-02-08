FROM python:3.11-slim

WORKDIR /app

# Environment settings
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/cache

# (Optional) install system deps only if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create cache directory for Hugging Face models
RUN mkdir -p /app/cache

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
