from time import sleep
from json import dumps
from kafka import KafkaProducer
my_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )
for n in range(500):
    print("sending")
    my_data = {'num': n}
    my_producer.send('test', value=my_data)
    sleep(5)