"""
__author__ = mcr99
__created__ = 25/11/2022
"""
import paho.mqtt.client as mqtt
import pymongo
from kafka import KafkaConsumer
import pandas as pd
from pickle import loads, load, dumps


def connect_to_mongo():
    """
    This method establishes connection to a mongodb database and gets the DB and the collection.
    If the connection is not possible, a message is sent reporting the error.
    :return: None
    """
    global COLLECTION
    try:
        client = pymongo.MongoClient(
            "mongodb://marc:2022@192.168.10.102:27017/")
        db = client["temperatures"]
        COLLECTION = db["analytics_results"]
        print("Connected successfully to the MongoDB")
    except:
        print("Unable to connect with the specified DB")


def save_to_db(data):
    """
    This method saves the data received from the MQTT broker to the database.
    If the insertion is not possible, a message is dispalyed reporting the error.
    :param data: List that contains all the temperatures.
    :return: None
    """
    try:
        print(data)
        COLLECTION.insert_one(data[0])
        print("Data inserted successfully")
    except:
        print("Unable to insert the data")


if __name__ == '__main__':
    connect_to_mongo()
    consumer = KafkaConsumer(
        'analytics_results', 
        bootstrap_servers=['192.168.10.103:9092'], #Kafka ip
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='analytics-group',
        value_deserializer=lambda x: loads(x))

    for message in consumer:
        message = message.value
        save_to_db(message)
        print(message)
