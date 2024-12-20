# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies and diagnostic tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    net-tools \
    curl \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Make entrypoint script executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["./entrypoint.sh"]