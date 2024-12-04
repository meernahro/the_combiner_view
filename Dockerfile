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

# Command to run Daphne
CMD ["daphne","-b", "0.0.0.0", "-p", "7999", "the_combiner_view.asgi:application"]
