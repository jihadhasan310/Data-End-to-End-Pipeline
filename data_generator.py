import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_sensor_data():
    sensor_data = {
        "device_id": random.randint(1, 100),
        "temperature": round(random.uniform(15, 30), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "energy_usage": round(random.uniform(50, 500), 2),
        "motion": random.choice([0, 1])
    }
    return
