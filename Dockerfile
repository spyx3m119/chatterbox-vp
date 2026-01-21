# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME=0.0.0.0 \
    GRADIO_SERVER_PORT=7860 \
    HF_HOME=/app/cache/huggingface

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    libsndfile1-dev \
    libavcodec-extra \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . /app/

# Install Python dependencies and the project itself
# We use -e . to install in editable mode if the user wants to develop inside the container
RUN pip install --no-cache-dir -e .

# Create cache directory and set permissions for samples
RUN mkdir -p /app/cache/huggingface && chmod -R 777 /app/cache/huggingface
RUN chmod -R 777 /app/samples

# Expose the Gradio port
EXPOSE 7860

# Command to run the unified webui by default
CMD ["python", "unified_webui.py"]
