FROM python:3.11-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache netcat-openbsd

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (if needed for health checks)
EXPOSE 3001

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "main.py"]
