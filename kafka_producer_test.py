from confluent_kafka import Producer
import time
import json

# Kafka broker settings
KAFKA_BROKER = "localhost:29092"
TOPIC = "users"

# Configure the Kafka producer
producer_config = {
    "bootstrap.servers": KAFKA_BROKER
}

producer = Producer(producer_config)


def delivery_report(err, msg):
    """ Callback function for message delivery reports """
    if err:
        print(f"Message failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Sending messages
for i in range(1000):
    user_data = {
        "id": i,
        "name": f"User{i}",
        "email": f"user{i}@gmail.com"
    }

    # Serialize data as JSON
    message = json.dumps(user_data)

    # Send message
    producer.produce(TOPIC, value=message, callback=delivery_report)

    producer.flush()  # Ensures message is sent
    time.sleep(5)  # Simulate message intervals

print("Finished sending messages.")