# This ETL Pipeline gets info from the GTFS, then sends to the Kafka. After streaming it to Kafka, it is
# pushed to MongoDB and Twilio to send SMS alerts. 

from kafka import KafkaConsumer, KafkaProducer
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
import requests
from pymongo import MongoClient
import os 
from dotenv import load_dotenv
import certifi
import time
import datetime 
from twilio.rest import Client
from kafka.errors import KafkaError

# Retry logic for connecting to Kafka
def wait_for_kafka():
    while True:
        try:
            print("🔌 Trying to connect to Kafka...")
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            print("Connected to Kafka.")
            return producer
        except Exception as e:
            print(f"Kafka not ready: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def run_alert_ingestion():
    print("Starting ETL pipeline")
    load_dotenv()
    print("Environment variables loaded.")

    mongoDB = os.getenv("MONGODB")

    # Twilio Info 
    twilio_sid = os.getenv("TWILIO_SID")
    twilio_token = os.getenv("TWILIO_TOKEN")
    twilio_number = os.getenv("TWILIO_NUMBER")
    target_phone = os.getenv("TARGET_PHONE")
    twilio_client = Client(twilio_sid, twilio_token)

    # 1. Connection to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient(mongoDB, tlsCAFile=certifi.where())
    db = client["ttc"]
    alerts = db["alerts"]
    print("Connected to MongoDB.")

    # 2. Delete alerts older than 10 minutes
    cutoff_time = datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10)
    delete_result = alerts.delete_many({"timestamp": {"$lt": cutoff_time}})
    print(f"Deleted {delete_result.deleted_count} old alerts")

    # 3. Fetch data and push to Kafka
    producer = wait_for_kafka()
    print("Fetching GTFS-RT alert feed...")
    response_alert = requests.get("https://bustime.ttc.ca/gtfsrt/alerts")

    if response_alert.status_code == 200:
        future = producer.send("alerts", value=response_alert.content)
        result = future.get(timeout=10)  # wait for Kafka ack
        print("Streamed to Kafka topic: alerts")
    else:
        print(f"Failed to fetch GTFS feed: {response_alert.status_code}")

    producer.flush()
    producer.close()

    # 4. Creating Kafka consumer for alerts
    print("Starting Kafka consumer for alerts...")
    consumer = KafkaConsumer(
        'alerts', 
        bootstrap_servers = "kafka:9092",
        group_id = "alert-group",
        auto_offset_reset = "earliest"
    ) 
    print("Kafka consumer ready and listening...")

    # 5. Pushing Alerts to MongoDB and messaging to phone number
    records = consumer.poll(timeout_ms=10000)  # wait up to 10s

    if not records:
        print("No alerts received in 10 seconds, exiting...")
        return  # Exit this run of run_alert_ingestion()

    for tp, messages in records.items():
        for msg in messages:
            try:
                # Making the feed readable 
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(msg.value)

                for entity in feed.entity:
                    if entity.HasField("alert"):
                        alert_obj = entity.alert

                        alert_doc = {
                            "header": alert_obj.header_text.translation[0].text if alert_obj.header_text.translation else "",
                            "description": alert_obj.description_text.translation[0].text if alert_obj.description_text.translation else "",
                            "timestamp": datetime.datetime.now(datetime.UTC)
                        }

                        # Insert into MongoDB
                        alerts.insert_one(alert_doc)
                        print(f"Alert saved: {alert_doc['header']}")

            except DecodeError:
                print("Could not decode GTFS alert message.")
            except Exception as e:
                print(f"Error saving alert: {e}")

# Run every 10 min
if __name__ == "__main__":
    while True:
        print("\n[RUNNING ALERT INGESTION]")
        run_alert_ingestion()
        print("[SLEEPING FOR 10 MINS...]\n")
        time.sleep(600)
