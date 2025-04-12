FROM python:3.13-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 6000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=6000"] 