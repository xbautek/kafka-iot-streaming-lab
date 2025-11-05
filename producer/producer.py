import json, os, random, time
from datetime import datetime, timezone
from kafka import KafkaProducer, errors as kerrors

BOOTSTRAP = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("TOPIC", "iot_demo")
RATE = float(os.getenv("RATE_PER_SEC", "5"))
MACHINES = int(os.getenv("MACHINES", "5"))

def make_event(machine_id: int) -> dict:
    return {
        "machine_id": machine_id,
        "temperature": round(random.normalvariate(70, 5), 2),
        "vibration": round(abs(random.normalvariate(3, 1)), 2),
        "rpm": int(random.normalvariate(1500, 80)),
        "power": round(random.uniform(0.6, 1.4), 2),
        "ts": datetime.now(timezone.utc).isoformat(),
    }

def connect_with_retry(max_wait_s=30):
    start = time.time()
    backoff = 0.5
    while True:
        try:
            return KafkaProducer(
                bootstrap_servers=BOOTSTRAP,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: str(k).encode("utf-8"),
                linger_ms=50,
            )
        except (kerrors.NoBrokersAvailable, kerrors.KafkaTimeoutError) as e:
            if time.time() - start > max_wait_s:
                raise
            print(f"[producer] broker not ready ({e}), retrying...")
            time.sleep(backoff)
            backoff = min(backoff * 1.5, 2.0)

def main():
    producer = connect_with_retry()
    print(f"[producer] -> topic={TOPIC} bootstrap={BOOTSTRAP} rate={RATE}/s")
    sleep_step = 1.0 / RATE if RATE > 0 else 0.2
    while True:
        key = random.randint(1, MACHINES)
        event = make_event(key)
        producer.send(TOPIC, key=key, value=event)
        time.sleep(sleep_step)

if __name__ == "__main__":
    main()
