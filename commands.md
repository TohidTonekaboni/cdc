# go inside mysql_container container
docker exec -it mysql_container mysql -u root -p

SHOW DATABASES;
use CDC_DB
SHOW TABLES;

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    score INT
);

DESCRIBE students;

# ################################## KAFKA #########################################################
docker ps --format 'table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}'

# list of kafka topics
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list
# list of consumer groups
docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list
# delete a consumer group
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --delete --group <consumer-group-name>

# create topic
docker exec kafka kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic users

# show messages with detail
docker exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic users --from-beginning --property print.timestamp=true --property print.key=true --property print.value=true


# debezium
# get list of plugins
curl -s -XGET http://localhost:8083/connector-plugins|jq '.[].class'
# get list of connectors
curl -s -X GET http://localhost:8083/connectors

# POSTGRES Connector
curl -i -X POST http://localhost:8083/connectors/ -H "Accept: application/json" -H "Content-Type: application/json" -d '{
  "name": "postgres-cdc",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "cdc",
    "database.password": "cdc123",
    "database.dbname": "cdc_db",
    "database.server.name": "postgres_server",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.autocreate.mode": "filtered",
    "table.include.list": "public.students",
    "database.history.kafka.bootstrap.servers": "kafka:9092",
    "database.history.kafka.topic": "schema-changes.postgres",
    "topic.prefix": "cdc_posgres_topic"
  }
}'

curl -s -X GET http://localhost:8083/connectors/postgres-cdc/status | jq '.'
