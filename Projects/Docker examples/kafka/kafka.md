# HANDS ON WITH KAFKA

- Start the docker-compose
```bash
docker compose up -d 
```
create a new topic

```bash
docker exec -it kafka  kafka-topics --create --topic test -partitions 3 --replication-factor 1 --bootstrap-server localhost:9092
```
list all topics
```bash
docker exec -it kafka  kafka-topics --list --bootstrap-server localhost:9092
```

describe a topic

```bash
docker exec kafka  kafka-topics --describe --topic test --bootstrap-server localhost:9092
```

delete a topic

```bash
docker exec kafka  kafka-topics --delete --topic test --bootstrap-server localhost:9092
```

build producer docker

```bash
docker build -t kafka-producer .
```

run producer

```bash
docker run --network=host --name producer -d kafka-producer 
```

build the consumer
```bash
docker build -t kafka-consumer .
```

run the consumer
```bash
docker run --network=host --name consumer kafka-consumer
```

describe the consumer groups
```bash
docker exec kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group my-group
```