FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && apt-get update && apt-get install -y --no-install-recommends netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*
COPY producer.py .
ENV BOOTSTRAP_SERVERS=kafka:9092
ENV TOPIC=iot_demo
ENV RATE_PER_SEC=5
ENV MACHINES=5
CMD ["bash", "-lc", "until nc -z kafka 9092; do echo '[producer] waiting for kafka...'; sleep 0.5; done; python producer.py"]
