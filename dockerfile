# Use a slim Python image (adjust tag if you need a specific Python version)
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable stdout/stderr streaming
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps required for building some Python wheels (removed afterwards)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask default port
EXPOSE 5000

# Configure Flask runtime env; pass SECRET_KEY or other env vars at runtime
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# If you want debug, set FLASK_DEBUG=1 at runtime (not recommended in production)

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]