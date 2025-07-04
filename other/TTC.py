import requests
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

response_alert = requests.get("https://bustime.ttc.ca/gtfsrt/alerts")
if response_alert.status_code == 200:
    future = producer.send("alerts", value=response_alert.content)
    result = future.get(timeout=10)  # wait for Kafka ack
    print(" Streamed to Kafka topic: alerts")
else:
    print(f" Failed to fetch: {response_alert.status_code}")

response_vehicle = requests.get("https://bustime.ttc.ca/gtfsrt/vehicle")
if response_vehicle.status_code == 200:
    future = producer.send("vehicle", value=response_vehicle.content)
    result = future.get(timeout=10)  # wait for Kafka ack
    print(" Streamed to Kafka topic: vehicle")
else:
    print(f" Failed to fetch: {response_vehicle.status_code}")

response_trips = requests.get("https://bustime.ttc.ca/gtfsrt/trips")
if response_trips.status_code == 200:
    future = producer.send("trips", value=response_trips.content)
    result = future.get(timeout=10)  # wait for Kafka ack
    print(" Streamed to Kafka topic: trips")
else:
    print(f" Failed to fetch: {response_trips.status_code}")

producer.flush()
producer.close()


