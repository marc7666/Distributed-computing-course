import paho.mqtt.publish as publish
publish.single(f"ClassTest/variable",
               "helloWorld",
               hostname="host.docker.internal")
