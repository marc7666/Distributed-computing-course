# Getting Started With Docker
## INSTALL DOCKER
To create a docker, we first need to install the docker application

Install it following the instructions in [https://www.docker.com/](https://www.docker.com/)

## EXPERIMENT WITH DOCKER
###### Start a mongodb docker
to start a mongo docker, is very simple. Just run a new container with the mongo image
```bash
docker run --name mongo-database -d mongo:4.2.23
```
**It is important to always set the version of the docker after the semicolon, to avoid problems with newer versions.**

###### print the running containers

```bash
docker ps
```

###### Enter the docker to run commands in it
```bash
docker exec -it mongo-database /bin/bash
```

###### Populate test db with some data

```mongo
use test;
db.test.insert([{"aaa":"1234"},{"aaa":12}]);
```

###### Get back the data

```mongo
use test
db.test.find({});
```

###### Stop and remove the containers

```bash
docker stop mongo-database
docker rm mongo-database
```

###### Store mongo data outside the docker

If we use the internal storage of the docker, it is possible we migth run out of space. Also, if for any reason, the docker is removed, all the information will be deleted.
To be able to keep the stored database independently from the docker, we must build a volume to keep the information in our local sistem

```bash
docker run --name mongo-database -v /Users/eloigabal/class/mongodb:/data/db -d mongo:4.2.23
```

###### Connect different dockers to work together

In docker, we can create virtual networks to connect the different dockers between them, by default all dockers start no network,

We can manage networks
```bash 
docker network ls
```
Create a new network
```bash
docker network create mongo
```

run the docker using the new network

```bash
docker run --name mongo-database -v /Users/eloigabal/class/mongodb:/data/db --network mongo -d mongo:4.2.23
```

start the new docker to log-in the  database
```bash 
docker run -it --network mongo mongo:4.2.23 mongo -host mongo-database
```

###### Bind the dockers to a port for external access

```bash
docker run --name mongo-database -p 27017 -v /Users/eloigabal/class/mongodb:/data/db --network mongo -d mongo:4.2.23
```

```bash
docker run --name express -p 8081:8081 --network mongo -e ME_CONFIG_MONGODB_SERVER=mongo-database -d mongo-express:0.54.0
```

## BUILD A DOCKER

```bash
docker build -t mydocker .
```

## USE THE DOCKER COMPOSE
###### Start the docker compose platform
```bash
docker compose up -d
```
###### Remove the docker compose platform
```bash
docker compose down
```