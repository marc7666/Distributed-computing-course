#Specifying the base image
FROM python:latest

#Specifying the path where the client file is placed.

WORKDIR ./client.py

#Files that will be runed in the docker container.
COPY client.py .
COPY data2.csv .

#Installing the dependencies
RUN pip install paho-mqtt


#Finally, we run the file. This command is the "./client.py" cmd equivalent.
CMD [ "python3", "-u", "client.py" ]