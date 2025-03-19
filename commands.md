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