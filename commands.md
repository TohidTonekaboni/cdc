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

# MYSQL Connector
curl -X POST http://localhost:8083/connectors -H "Content-Type: application/json" -d '{
  "name": "mysql-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "cdc_mysql_user",
    "database.password": "cdc_mysql_password",
    "database.server.id": "1",
    "database.include.list": "CDC_DB",
    
    "topic.prefix": "mysql_cdc",
    
    "database.history.kafka.bootstrap.servers": "kafka:29092",
    "database.history.kafka.topic": "mysql_cdc_schema_history"
  }
}'
curl -X GET http://localhost:8083/connectors/mysql-connector/status | jq .
curl -X DELETE http://localhost:8083/connectors/mysql-connector