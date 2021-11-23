# python 3.6

import random
import time
from paho.mqtt import client as mqtt_client

broker = "mqtt.eclipseprojects.io"
port = 1883
topic = "cuppy/sensor/lux"
# generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 1000)}"

current_lux = 300.0
max_variance = 25.0


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    global current_lux

    while True:
        time.sleep(2)
        current_lux = round(
            current_lux + random.uniform(-max_variance, max_variance), 1
        )

        result = client.publish(topic, current_lux)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Sent `{current_lux}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()
