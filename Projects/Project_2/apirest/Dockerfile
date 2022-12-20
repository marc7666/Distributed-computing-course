#Specifying the base image
FROM python:latest
#here the dockerfile is pulling the python 3.10 from docker hub which already has python installed so we have all the things we need to have python in our container.

WORKDIR .

#Here we added the python file that we want to run in docker and define its location.
COPY pr2sql.py .
RUN mkdir static
COPY ./static/swagger.json ./static

#Here we installed the dependencies, we are using the pygame library in our main.py file so we have to use the pip command for installing the library
RUN pip install mysql-connector-python
RUN pip install flask_swagger_ui
RUN pip install flask_cors
RUN pip install jsonschema
RUN pip install pymongo


EXPOSE 5000:5000

#lastly we specified the entry command this line is simply running python ./main.py in our container terminal
CMD [ "python3","-u", "pr2sql.py" ]