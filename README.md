# 🧠 Kafka IoT Streaming Lab

A small end-to-end data engineering project that simulates an IoT data pipeline using Apache Kafka. A Python producer sends telemetry events and a Python consumer computes 1-second averages and raises alerts for high temperatures.

---

## 🚀 Features

- Producer (Python) — generates randomized IoT sensor data for multiple machines
- Consumer (Python) — computes 1-second averages and prints alerts when temperature > 80 °C
- Apache Kafka (KRaft mode) as the message broker
- Kafka UI (Provectus) for inspecting topics/messages
- Fully containerized with Docker Compose

---

## 🧩 Architecture

Producer (Python) --> Kafka (broker) --> Consumer (Python)  
Kafka UI connects to the broker for visualization

Each component runs in its own Docker container on an internal Docker network.

---

## 🛠️ Stack

| Component        |                Technology |
| ---------------- | ------------------------: |
| Message broker   | Apache Kafka (KRaft mode) |
| Producer         |     Python + kafka-python |
| Consumer         |     Python + kafka-python |
| Visualization    |      Kafka UI (Provectus) |
| Containerization |            Docker Compose |

---

## 🧰 Project Structure

kafka-iot-streaming-lab/  
├─ docker-compose.yml  
├─ producer/  
│ ├─ Dockerfile  
│ ├─ requirements.txt  
│ └─ producer.py # sends ~5 IoT messages/sec  
├─ consumer/  
│ ├─ Dockerfile  
│ ├─ requirements.txt  
│ └─ consumer.py # prints 1s average + alerts if temp > 80  
└─ README.md

---

## ⚙️ How to run

1. Start the stack:

```bash
docker compose up -d --build
```

This starts:

- kafka — the broker
- kafka-ui — dashboard on port 8080
- producer — continuously sends simulated IoT data
- consumer — reads and aggregates messages

2. Open Kafka UI:

- http://localhost:8080
- Navigate: Topics → iot_demo → Messages
- Set Deserializer: JSON, Offset: Earliest

3. View logs:
   Producer:

```bash
docker compose logs -f producer
```

Consumer:

```bash
docker compose logs -f consumer
```

Expected consumer output (example):

```text
[avg 1s] n=5 temp=72.31 °C vib=3.02 rpm=1490 power=1.01
!!! ALERT temp>80: 81.45 °C @ machine=3 ts=2025-11-05T14:12:34Z
```

Example message (JSON):

```json
{
  "machine_id": 3,
  "temperature": 72.15,
  "vibration": 2.95,
  "rpm": 1495,
  "power": 1.03,
  "ts": "2025-11-05T14:00:33.123Z"
}
```

---

## 🧠 How it works

- Producer publishes JSON messages to topic `iot_demo`.
- Consumer reads the topic, computes 1-second rolling averages, and prints alerts when temperature > 80 °C.
- Kafka UI lets you inspect topics and messages.

---

## 🧪 Useful commands

List running services:

```bash
docker compose ps
```

List topics:

```bash
docker compose exec kafka bash -lc "/opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list"
```

Consume messages from Kafka:

```bash
docker compose exec kafka bash -lc "/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iot_demo --from-beginning --timeout-ms 5000"
```

Stop everything:

```bash
docker compose down
```

---

## 🧱 Next steps (ideas)

- Store processed data in TimescaleDB or PostgreSQL
- Build Grafana dashboards for live monitoring
- Deploy to cloud managed services (MSK, etc.)
- Add ML-based anomaly detection (e.g., Isolation Forest)
- Orchestrate ETL with Airflow

---

Enjoy experimenting with the IoT streaming pipeline! :)
