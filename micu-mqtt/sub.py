# python3.6
import random
from paho.mqtt import client as mqtt_client
from cuppy.settings import MQTT_PORT, MQTT_BROKER_URL, MQTT_TOPICS

# generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 100)}"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect_async(MQTT_BROKER_URL, MQTT_PORT)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # TODO: Update models here.

    for topic in MQTT_TOPICS:
        client.subscribe(topic)

    client.on_message = on_message


def run():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_start()
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()



if __name__ == "__main__":
    run()