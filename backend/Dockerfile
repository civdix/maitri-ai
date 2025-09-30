FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y \
    ffmpeg libsndfile1 git build-essential \
    libgl1 libglib2.0-0 cmake g++ make \
    libopenblas-dev liblapack-dev libx11-dev curl unzip \
  && rm -rf /var/lib/apt/lists/*

# Install Piper CLI binary
RUN curl -L -o /usr/local/bin/piper https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_amd64 && \
    chmod +x /usr/local/bin/piper

COPY requirements.txt .
# For GPU builds, switch to requirements-gpu.txt and ensure CUDA libs are available
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p models data

EXPOSE 8000
CMD ["python", "main.py"]