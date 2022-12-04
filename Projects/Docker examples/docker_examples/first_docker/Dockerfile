FROM ubuntu:20.04
# used to avoid asking for confirmation in the apt-get install
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y python3 python3-pip
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
# it will create a default command when running the docker
CMD ["python3"]
