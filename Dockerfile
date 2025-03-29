FROM python:3.11-slim

WORKDIR /app

# Install required packages (including fonts)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-noto-cjk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ ./src/
COPY config.yaml .

# Set font path
ENV FONT_PATH=/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["python", "src/main.py"]