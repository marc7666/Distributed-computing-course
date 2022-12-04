"""
__author__ = mcr99
__created__ = 13/11/2022
"""
from datetime import date
import paho.mqtt.client as mqtt
import pymongo
from kafka import KafkaProducer
from pickle import loads, load, dumps


def connect_to_mongo():
    """
    This method establishes connection to a mongodb database and gets the DB and the collection.
    If the connection is not possible, a message is sent reporting the error.
    The connection to the DB is performed through a username and a password.
    :return: None
    """
    global COLLECTION
    try:
        client = pymongo.MongoClient(
            "mongodb://marc:2022@192.168.10.102:27017/")
        db = client["temperatures"]
        COLLECTION = db["temperatures"]
        print("Connected successfully to the MongoDB")
    except:
        print("Unable to connect with the specified DB")


def save_to_db(data):
    """
    This method saves the data received from the MQTT broker to the database.
    If the insertion is not possible, a message is dispaayed reporting the error
    :param data: List that contains all the temperatures.
    :return: None
    """
    try:
        to_save = {"id_clien": data[0], "temperature": data[1]}
        print(to_save)
        COLLECTION.insert_one(to_save)
        print("Data inserted successfully")
    except:
        print("Unable to insert the data")


def on_message(client, userdata, message):
    """
    This method receives the client data through the MQTT broker.
    The information that arrives from the broker, looks like: ClientID-Lecture. Hence, we've to split it up.
    The information is saved in a Mongo database and is sent to the analytics module.
    :param client: client id
    :param userdata: lectures (temperatures)
    :param message: Complete message
    :return: None
    Note: The parameters client and userdata, are not used in this implementation, but are part of the parameters
    of the method, because the library defines the method on_message in this way.
    """
    data_received = message.payload.decode()
    data_to_store = data_received.split("-")
    save_to_db(data_to_store)
    producer.send('analytics', {"v": float(data_to_store[1]), "ts": date.today() , "sensor": data_to_store[0] })
    print(data_to_store)

global producer

if __name__ == '__main__':
    connect_to_mongo()
    client=mqtt.Client("MarcC_Cloud")
    client.connect("test.mosquitto.org")
    print("Connected to a broker!")
    client.subscribe("marcc/temperature")
    producer=KafkaProducer(
        bootstrap_servers = ['192.168.10.103:9092'], value_serializer = lambda x: dumps(x))
    client.on_message= on_message
    client.loop_forever()
