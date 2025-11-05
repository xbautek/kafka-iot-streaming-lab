FROM python:3.11-slim
WORKDIR /consumer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer.py .
ENV BOOTSTRAP_SERVERS=kafka:9092
ENV TOPIC=iot_demo
ENV GROUP_ID=lab-consumers-1
ENV WINDOW_SEC=1
CMD ["python", "consumer.py"]