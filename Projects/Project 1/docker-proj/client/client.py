"""
__author__ = mcr99
__created__ = 01/11/2022
"""
import random
import paho.mqtt.client as mqtt
import re
from time import sleep


# pylint: disable=W1514
def process_file(file_name, data_separation='\n'):
    """
    This method reads the file where are placed all the values and put them inside a list,
    that will be returned, and ignores all values that are not numbers.
    :param file_name: File where are placed the temperatures
    :param data_separation: Default data separation -> \n
    :return: List with all the values
    """
    with open(file_name, 'r') as file:
        # Special characters to ignore
        regex = re.compile('[@_!#$%^&*()<>?/|}{~:]')
        data = []
        try:
            for line in file:
                value = line.split(data_separation)  # Splitting a line by \n
                if not value[0].isalpha() and regex.search(value[0]) is None:
                    # Only appending the numbers
                    data.append(value[0])
        finally:
            file.close()
    return data


def data_every_10_seconds(clientId, data):
    """
    This method sends to the MQTT broker a lecture every 10 seconds
    :param data: List where are placed all the values
    :return: None
    """
    i = 0
    while True:
        i += 1
        if i == len(data):
            i = 0
        client.publish('marcc/temperature', clientId + "-" + data[i])
        #client.publish('marcc/temperature', 16)
        # print("16")
        print(data[i])
        i = (i + 1) % len(data)
        sleep(10)


if __name__ == '__main__':
    temperatures = process_file("data2.csv")
    clientId = "MarcC_"+str(random.randint(0, 100))
    client = mqtt.Client(clientId)
    client.connect("test.mosquitto.org")
    data_every_10_seconds(clientId,temperatures)
