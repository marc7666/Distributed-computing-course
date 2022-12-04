#Specifying the base image
FROM python:latest

#Specifying the path where the cloud file is placed

WORKDIR ./cloud.py

#Here we added the python file that we want to run in docker and define its location.
COPY cloud.py .

#Files that will be runed in the docker container
RUN pip install pymongo
RUN pip install paho-mqtt
RUN pip install kafka-python


EXPOSE 5000:5000

#Finally, we run the file. This command is the "./cloud.py" cmd equivalent
CMD [ "python3","-u", "cloud.py" ]