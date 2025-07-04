from kafka import KafkaConsumer
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
import requests
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

response_vehicle = requests.get("https://bustime.ttc.ca/gtfsrt/vehicle")
if response_vehicle.status_code == 200:
    future = producer.send("vehicle", value=response_vehicle.content)
    result = future.get(timeout=10)  # wait for Kafka ack
    print(" Streamed to Kafka topic: vehicle")
else:
    print(f" Failed to fetch: {response_vehicle.status_code}")

producer.flush()
producer.close()

consumer = KafkaConsumer(
    'vehicle', 
    bootstrap_servers = "localhost:9092",
    group_id = "vehicle-group",
    auto_offset_reset = "latest"
) 

print("Listening to Vehicles...")

for msg in consumer:
    try:
        # Decode GTFS-RT Protobuf
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(msg.value)

        for entity in feed.entity:
            if entity.HasField("vehicle"):
                vehicle = entity.vehicle.description_text.translation[0].text
                print(f"📢 {vehicle}\n")

    except DecodeError as e:
        print("Unable to fetch specific vehicle.")

    finally:
        consumer.close()
        print("Consumer closed")