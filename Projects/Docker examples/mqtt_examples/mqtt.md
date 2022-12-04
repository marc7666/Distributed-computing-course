# Getting Started With MQTT

## Deploy a mqtt docker
1. Create the docker-compose/docker command to run the `mqtt docker` as specified in the [documentation](https://hub.docker.com/_/eclipse-mosquitto)
> I had problems with the newest version and the solution was to use an old one `1.6.2`. I don't know if it is already corrected

2. Start the mqtt broker
```bash
docker compose up -d
```

3. Explore the mqtt and test it with the MQTT Explorer application

4. Create the script with your favourite language to publish and subscribe to an MQTT topic

5. Build a docker with the created scripts
```bash
docker build -t mqtt-test .
```
6. Run the subscribing script in the docker
```bash
docker run --add-host=host.docker.internal:host-gateway mqtt-test python3 -u subscribe.py
```
> In this docker, we need to add the "localhost" of our host machine, as the docker has its own localhost. The host's localhost will be named `host.docker.internal` in the docker

> To be able to see the outputs of the python script, we need to set the flat `-u` unbuffered output. or the script will not print anything

7. Run the publishing script to publish some messages in the topic
```bash
docker run --add-host=host.docker.internal:host-gateway mqtt-test python3 publish.py 
```