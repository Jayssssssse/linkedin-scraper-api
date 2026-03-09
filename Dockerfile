FROM python:3.11-slim

RUN apt-get update && apt-get install -y chromium chromium-driver && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY linkedin_api.py .

CMD ["uvicorn", "linkedin_api:app", "--host", "0.0.0.0", "--port", "8000"]
