# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p chroma_db logs data

# Expose port
EXPOSE 5000

# Create startup script
RUN echo '#!/bin/bash\n\
# Start Ollama in background\n\
ollama serve &\n\
\n\
# Wait for Ollama to start\n\
sleep 10\n\
\n\
# Download model if not exists\n\
ollama list | grep -q llama2 || ollama pull llama2\n\
\n\
# Start Flask application\n\
python app.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Set the startup command
CMD ["/app/start.sh"]