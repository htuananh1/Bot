# Multi-stage build for optimized image size
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY bot/ ./bot/
COPY main.py .

# Create data directory
RUN mkdir -p /app/data

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DATA_PATH=/app/data/users.json

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health').read()" || exit 1

# Run the bot
CMD ["python", "-u", "main.py"]
