from confluent_kafka import Consumer, KafkaException
import json

# Kafka settings
KAFKA_BROKER = "localhost:29092"
TOPIC = "cdc_posgres_topic.public.students"
GROUP_ID = "students-group"

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

        # Decode raw message
        raw_value = msg.value()
        if not raw_value:  # Check if message is empty
            print("Received an empty message.")
            continue

        try:
            # Decode JSON (assuming Debezium format)
            message = json.loads(raw_value.decode("utf-8"))
            operation = message.get("op")  # Operation type (c = create, u = update, d = delete)
            source_table = message.get("source", {}).get("table")
            timestamp = message.get("ts_ms")
            
            # Extract actual data
            after_data = message.get("after")  # The new row data after INSERT/UPDATE
            before_data = message.get("before")  # The old row data before UPDATE/DELETE

            print("\n📥 New Kafka Message Received:")
            print(f"🗂 Table: {source_table}")
            print(f"⏳ Timestamp: {timestamp}")
            print(f"🛠 Operation: {operation}")

            if after_data:
                print(f"✅ Inserted/Updated Row: {after_data}")
            if before_data:
                print(f"❌ Deleted/Old Row: {before_data}")

        except json.JSONDecodeError as e:
            print(f"❌ JSON Decode Error: {e}")
            print(f"🔍 Raw Message: {raw_value}")

except KeyboardInterrupt:
    print("Consumer stopped.")
finally:
    consumer.close()
