FROM python:3.10-slim

WORKDIR /app

# Cài dependency hệ thống cho OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code sau
COPY . .

CMD ["python", "run.py"]