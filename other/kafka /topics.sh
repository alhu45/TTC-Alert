kafka-topics --create --topic alerts \
  --bootstrap-server localhost:9092 \
  --partitions 20 \ 
  --replication-factor 1 \

kafka-topics --create --topic vehicle \
  --bootstrap-server localhost:9092 \
  --partitions 20 \
  --replication-factor 1 \

kafka-topics --create --topic trips \
  --bootstrap-server localhost:9092 \
  --partitions 20 \
  --replication-factor 1 \

kafka-topics --create --topic nearby_routes \
  --bootstrap-server localhost:9092 \
  --partitions 20 \
  --replication-factor 1 \
  
# Partitions in a topic is like lanes of messages, so more partitons, more parallelism. 
# Replication is how many Kafka Brokers will hold the data. If there is 1, no replications, but 3 means at least 3 brokers. 

# See if the script is executable
# chmod +x topics.sh
# ./topics.sh

# Create Topics
# kafka-topics --list --bootstrap-server localhost:9092

# See the topics active in broker
# /usr/local/opt/kafka/bin/kafka-topics --bootstrap-server localhost:9092 --list


# See the detail on each topic
# kafka-topics --bootstrap-server localhost:9092 --describe --topic alerts
