FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TRANSFORMERS_CACHE=/app/cache \
    # Ensure the local bin is in the path just in case
    PATH="/home/appuser/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and set up permissions
RUN useradd -m appuser
RUN mkdir -p /app/cache && chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Copy requirements and install
# Added --user to ensure it goes into /home/appuser/.local
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy the rest of the application code
COPY --chown=appuser:appuser . .

# Expose the port
EXPOSE 8000

# PATCH: Use 'python -m uvicorn' to avoid "executable not found" errors
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
