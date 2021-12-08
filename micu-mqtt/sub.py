# python3.6
import random
import time
from paho.mqtt import client as mqtt_client
from cuppy.settings import MQTT_PORT, MQTT_BROKER_URL, MQTT_TOPICS


broker = "mqtt.eclipseprojects.io"
port = 1883
topics = ["cuppy/sensor/temp", "cuppy/sensor/moisture", "cuppy/sensor/lux"]
alert_topics = {"temp": "cuppy/alert/temp",
                "moist": "cuppy/alert/moisture",
                "lux": "cuppy/alert/lux"
                }
# generate client ID with pub prefix randomly
client_id = f"python-mqtt-{random.randint(0, 100)}"

MIN_LUX = 0
MAX_LUX = 100

MIN_TEMP = 0
MAX_TEMP = 100

MIN_MOIST = 0
MAX_MOIST = 100

curr_lux = None
curr_moist = None
curr_temp = None


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
        global curr_lux, curr_moist, curr_temp
        info = msg.payload.decode()

        print(f"Received `{info}` from `{msg.topic}` topic")

        if msg.topic == "cuppy/sensor/lux":
            curr_lux = float(info)
        elif msg.topic == "cuppy/sensor/moisture":
            curr_moist = float(info)
        elif msg.topic == "cuppy/sensor/temp":
            curr_temp = float(info)

    for topic in MQTT_TOPICS:
        client.subscribe(topic)

    client.on_message = on_message


def check_if_in_boundaries(curr, min_val, max_val):
    return (curr > min_val) and (curr < max_val)


def alert_topic(client, topic, curr, min_val, max_val):
    global alert_topic
    if not check_if_in_boundaries(curr, min_val, max_val):
        result = client.publish(alert_topics[topic], curr)

        status = result[0]
        if status == 0:
            print(f"Sent alert `{curr}` to topic `{alert_topics[topic]}`")
        else:
            print(f"Failed to send message to topic {alert_topics[topic]}")


def publish(client):
    global curr_lux, curr_moist, curr_temp
    global MIN_MOIST, MAX_MOIST, MIN_TEMP, MAX_TEMP, MIN_LUX, MAX_LUX

    prev_lux, prev_moist, prev_temp = curr_lux, curr_moist, curr_temp

    while True:
        time.sleep(2)

        print(curr_lux, curr_temp, curr_moist)
        print(prev_lux, prev_temp, prev_moist)

        if prev_lux != curr_lux:
            prev_lux = curr_lux
            if prev_lux is not None:
                alert_topic(client, "lux", curr_lux, MIN_LUX, MAX_LUX)

        if prev_moist != curr_moist:
            prev_moist = curr_moist
            if prev_moist is not None:
                alert_topic(client, "moist", curr_moist, MIN_MOIST, MAX_MOIST)

        if prev_temp != curr_temp:
            prev_temp = curr_temp
            if prev_temp is not None:
                alert_topic(client, "temp", curr_temp, MIN_TEMP, MAX_TEMP)


def run():
    client = connect_mqtt()
    subscribe(client)

    client.loop_start()
    publish(client)


if __name__ == "__main__":
    run()
