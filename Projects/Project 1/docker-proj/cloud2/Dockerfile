#Specifying the base image
FROM python:latest
#here the dockerfile is pulling the python 3.10 from docker hub which already has python installed so we have all the things we need to have python in our container.

WORKDIR ./cloud2.py

#Here we added the python file that we want to run in docker and define its location.
COPY cloud2.py .

#Here we installed the dependencies, we are using the pygame library in our main.py file so we have to use the pip command for installing the library
RUN pip install pymongo
RUN pip install paho-mqtt
RUN pip install kafka-python
RUN pip install pandas


EXPOSE 5000:5000

#lastly we specified the entry command this line is simply running python ./main.py in our container terminal
CMD [ "python3","-u", "cloud2.py" ]