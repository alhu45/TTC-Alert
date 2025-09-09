# 🚍 Transit Delay Alert System

This project is a real-time ETL pipeline that consumes GTFS-RT (General Transit Feed Specification Realtime) feeds, processes them using Apache Kafka, stores transit data in MongoDB Atlas, and sends SMS alerts via Twilio when delays are detected.

## 🧩 Key Features

- **GTFS-RT Feed Ingestion:** Fetches real-time transit data from public transit agencies.
- **Kafka Streaming:** Streams data through Apache Kafka topics for scalable and reliable data processing.
- **ETL Pipeline:** Transforms, filters, and enriches the data for downstream use.
- **MongoDB Atlas:** Stores structured and queryable transit data in a cloud database.
- **Twilio SMS Alerts:** Automatically sends real-time delay alerts to subscribed users.
- **Dockerized Architecture:** Easily deployable with Docker Compose.
- **Hosted on AWS EC2:** Cloud-hosted for scalability and availability.
- **Kubernetes**


