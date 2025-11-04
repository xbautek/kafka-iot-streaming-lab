import json, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9094"
TOPIC = "iot_demo"
EVENTS = 20
DELAY_S = 0.5

def make_event(machine_id: int) -> dict:
    return {
        "machine_id": machine_id,
        "temperature": round(random.normalvariate(70, 5), 2),
        "vibration": round(abs(random.normalvariate(3, 1)), 2),
        "rpm": int(random.normalvariate(1500, 80)),
        "power": round(random.uniform(0.6, 1.4), 2),
        "ts": datetime.now(timezone.utc).isoformat(),
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: str(k).encode("utf-8"),
    )
    print(f"[producer] topic={TOPIC} bootstrap={BOOTSTRAP_SERVERS}")
    try:
        for i in range(EVENTS):
            key = random.randint(1, 5)
            event = make_event(key)
            producer.send(TOPIC, key=key, value=event)
            producer.flush()
            print(f"→ sent #{i+1:02d} key={key}: {event}")
            time.sleep(DELAY_S)
    finally:
        producer.close()

if __name__ == "__main__":
    main()
