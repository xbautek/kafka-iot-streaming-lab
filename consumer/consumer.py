import json, os, time
from collections import defaultdict
from kafka import KafkaConsumer

BOOTSTRAP = os.getenv("BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC = os.getenv("TOPIC", "iot_demo")
GROUP_ID = os.getenv("GROUP_ID", "lab-consumers-1")
WINDOW_SEC = float(os.getenv("WINDOW_SEC", "5"))

def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    print(f"[consumer] <- topic={TOPIC} bootstrap={BOOTSTRAP} group={GROUP_ID}")

    bucket_start = time.time()
    agg = defaultdict(float)
    count = 0

    def emit_avg():
        nonlocal agg, count, bucket_start
        if count == 0:
            return
        avg_temp = agg["temperature"] / count
        avg_vib  = agg["vibration"] / count
        avg_rpm  = agg["rpm"] / count
        avg_pow  = agg["power"] / count
        print(
            f"[avg {WINDOW_SEC:.0f}s] n={count} "
            f"temp={avg_temp:.2f}°C vib={avg_vib:.2f} rpm={avg_rpm:.0f} power={avg_pow:.2f}"
        )
        agg = defaultdict(float)
        count = 0
        bucket_start = time.time()

    try:
        for msg in consumer:
            data = msg.value
            temp = float(data.get("temperature", 0.0))
            if temp > 80.0:
                print(f"!!! ALERT temp>{80}: {temp:.2f}°C @ machine={data.get('machine_id')} ts={data.get('ts')}")

            agg["temperature"] += temp
            agg["vibration"] += float(data.get("vibration", 0.0))
            agg["rpm"] += float(data.get("rpm", 0.0))
            agg["power"] += float(data.get("power", 0.0))
            count += 1

            now = time.time()
            if now - bucket_start >= WINDOW_SEC:
                emit_avg()
    except KeyboardInterrupt:
        print("[consumer] stopping...")
    finally:
        if count > 0:
            emit_avg()
        consumer.close()

if __name__ == "__main__":
    main()
