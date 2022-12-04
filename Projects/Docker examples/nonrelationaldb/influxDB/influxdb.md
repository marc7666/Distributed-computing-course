# HANDS ON INFLUXDB
### Start the influxDB docker

```bash
docker compose up -d
```

#### SET UP the influxDB
Navigate to the "localhost:8086" and create the user, passowr and bucket

#### We can load data in multiple ways (see documentation online)
We will create a dokcer to generate random data

```batch
docker build -t influx-test .
docker run --network=host influx-test
```

### We can go to the UI to experiment with the visualization