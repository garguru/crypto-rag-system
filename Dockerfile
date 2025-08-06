# Use Python slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements_docker.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements_docker.txt

# Copy application files
COPY crypto_rag_with_memory.py .
COPY crypto_rag_enhanced.py .

# Expose Streamlit port
EXPOSE 8501

# Health check to ensure app is running
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "crypto_rag_with_memory.py", "--server.address=0.0.0.0"]