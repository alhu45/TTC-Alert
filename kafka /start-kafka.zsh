# Start Kafka broker
/usr/local/opt/kafka/bin/kafka-server-start /usr/local/etc/kafka/server.properties

# Use to see if it is executable
chmod +x start-kafka.zsh
./start-kafka.zsh

# To kill Kafka
lsof -i :9093    
kill -9 <PID>