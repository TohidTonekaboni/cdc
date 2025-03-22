CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    score INT
);



docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'
# create a topic
docker exec -it kafka kafka-topics.sh --create --topic users --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
# list of topics
docker exec -it kafka kafka-topics.sh --list --bootstrap-server localhost:9092
# list of consumer groups
docker exec -it kafka kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
