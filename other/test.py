# MONGODB TEST
# from pymongo import MongoClient
# import certifi

# uri = "mongodb+srv://17alanhu:9s4jyg8BF0zWGHrr@ttc.uznaw29.mongodb.net/?tls=true"

# client = MongoClient(uri, tlsCAFile=certifi.where())
# db = client["ttc"]
# alerts = db["alerts"]

# alerts.insert_one({"test": "MongoDB connection successful"})
# print("Successfully connected and inserted test document.")


# GTFS-ALERT Test
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import datetime

response = requests.get("https://bustime.ttc.ca/gtfsrt/alerts")
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

for entity in feed.entity:
    if entity.HasField("alert"):
        alert = entity.alert

        # Get active period
        active_periods = []
        for ap in alert.active_period:
            start = datetime.datetime.fromtimestamp(ap.start).isoformat() if ap.HasField("start") else "unknown"
            end = datetime.datetime.fromtimestamp(ap.end).isoformat() if ap.HasField("end") else "unknown"
            active_periods.append({"start": start, "end": end})

        # Informed entities (routes, stops)
        affected = [{"route_id": e.route_id, "stop_id": e.stop_id} for e in alert.informed_entity]

        print("\n🛑 TTC ALERT")
        print("Header:", alert.header_text.translation[0].text if alert.header_text.translation else "N/A")
        print("Description:", alert.description_text.translation[0].text if alert.description_text.translation else "N/A")
        print("Cause:", alert.cause)
        print("Effect:", alert.effect)
        print("Severity:", alert.severity_level)
        print("Active Periods:", active_periods)
        print("Affected Entities:", affected)
        print("More Info:", alert.url.translation[0].text if alert.url.translation else "N/A")

# ALERT-CONSUME-ETL Script 
# Testing to see if Alerts are being read
# print("Listening to Alerts...")
# for msg in consumer:
#     try:
#         # Decode GTFS-RT Protobuf
#         feed = gtfs_realtime_pb2.FeedMessage()
#         feed.ParseFromString(msg.value)

#         for entity in feed.entity:
#             if entity.HasField("alert"):
#                 alert = entity.alert.description_text.translation[0].text
#                 print(f"📢 {alert}\n")

#     except DecodeError as e:
#         print("Unable to fetch specific alert.")

#     finally:
#         consumer.close()
#         print("Consumer closed")