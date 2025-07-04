from kafka import KafkaConsumer
from google.transit import gtfs_realtime_pb2
from google.protobuf.message import DecodeError
from datetime import datetime
import requests
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

response_trips = requests.get("https://bustime.ttc.ca/gtfsrt/trips")
if response_trips.status_code == 200:
    future = producer.send("trips", value=response_trips.content)
    result = future.get(timeout=10)  # wait for Kafka ack
    print(" Streamed to Kafka topic: trips")
else:
    print(f" Failed to fetch: {response_trips.status_code}")

producer.flush()
producer.close()

def unix_to_readable(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %I:%M:%S %p')

consumer = KafkaConsumer(
    'trips',
    bootstrap_servers="localhost:9092",
    group_id="trips-group",
    auto_offset_reset="latest"
)

print("Listening to Trips...\n")

# CHATGPT MADE THIS
try:
    for msg in consumer:
        try:
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(msg.value)

            for entity in feed.entity:
                if entity.HasField("trip_update"):
                    trip = entity.trip_update.trip
                    print(f"🚌 Trip Update:")
                    print(f"  • Trip ID: {trip.trip_id}")
                    print(f"  • Route ID: {trip.route_id}")
                    print(f"  • Direction ID: {trip.direction_id}")
                    print(f"  • Start Time: {trip.start_time}")
                    print(f"  • Start Date: {trip.start_date}")
                    if trip.HasField("schedule_relationship"):
                        print(f"  • Schedule Relationship: {trip.schedule_relationship}")

                    # Go through stop time updates
                    for stop_update in entity.trip_update.stop_time_update:
                        print(f"\n  🛑 Stop Sequence: {stop_update.stop_sequence}")
                        print(f"  • Stop ID: {stop_update.stop_id}")
                        if stop_update.HasField("arrival"):
                            arrival = stop_update.arrival
                            print(f"  • Arrival Time: {unix_to_readable(arrival.time)}")
                            print(f"  • Arrival Delay: {arrival.delay} seconds")
                        if stop_update.HasField("departure"):
                            departure = stop_update.departure
                            print(f"  • Departure Time: {unix_to_readable(departure.time)}")
                            print(f"  • Departure Delay: {departure.delay} seconds")

                        if stop_update.HasField("schedule_relationship"):
                            print(f"  • Stop Schedule Relationship: {stop_update.schedule_relationship}")
                    print("\n" + "-" * 60)

        except DecodeError:
            print("⚠️ Could not decode trip update.\n")

except KeyboardInterrupt:
    print("\nStopping consumer...")

finally:
    consumer.close()
    print("Consumer closed.")
