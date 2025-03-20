from confluent_kafka import Consumer, KafkaException
import json

# Kafka settings
KAFKA_BROKER = "localhost:29092"
TOPIC = "users"
GROUP_ID = "user-group"

# Configure the Kafka consumer
consumer_config = {
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest"  # Read messages from the beginning if no offset is stored
}

consumer = Consumer(consumer_config)
consumer.subscribe([TOPIC])

print("Waiting for messages...")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages every second
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())

        # Deserialize JSON message
        user_data = json.loads(msg.value().decode("utf-8"))
        print(f"Received message: {user_data}")

except KeyboardInterrupt:
    print("Consumer stopped.")

finally:
    consumer.close()