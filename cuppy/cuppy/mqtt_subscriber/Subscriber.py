import os
import uuid
from cuppy.settings import MQTT_PORT, MQTT_BROKER_URL, DEBUG, MQTT_DEBUG_PRINTS
from ..models import MQTTCentralClient
from background_task import background

# generate client ID with pub prefix randomly
# client_id = f"python-mqtt-{random.randint(0, 100)}"

class MQTTSubscriber:

    def __init__(self, p_mqtt_client: MQTTCentralClient) -> None: # p_mqtt_client is of type MQTTCentralClient
        self.mqtt_client = p_mqtt_client

    # def read_should_stop(self):
    #     current_value = 0
    #     try:
    #         with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/central/" + str(self.mqtt_client.client_id)), 'r') as f:
    #             try:
    #                 current_value = int(f.read().strip())
    #             except:
    #                 current_value = 0
    #     except:
    #         with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/central/" + str(self.mqtt_client.client_id)), 'w') as f:
    #             f.write("0")
    #     return current_value

    # def write_should_stop(self, value):
    #     with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/central/" + str(self.mqtt_client.client_id)), 'w') as f:
    #         f.write(str(value))

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_disconnect(client, userdata, rc):
            if rc == 0:
                print("Disconnected to MQTT Broker!")
            else:
                print("Failed to disconnect, return code %d\n", rc)

        self.mqtt_client.mqtt_client.on_connect = on_connect
        self.mqtt_client.mqtt_client.on_disconnect = on_disconnect
        self.mqtt_client.mqtt_client.connect(MQTT_BROKER_URL, MQTT_PORT)


    def subscribe(self):
        def on_message(msg_client, userdata, msg):
            # TODO: Update models here.
            if DEBUG and MQTT_DEBUG_PRINTS:
                print("Got message {} on topic {}".format(msg.payload.decode(), msg.topic))
            try:
                current_val = float(msg.payload.decode())
                if msg.topic == "cuppy/sensor/lux":
                    self.mqtt_client.plant.current_lux = current_val
                elif msg.topic == "cuppy/sensor/moisture":
                    self.mqtt_client.plant.current_humidity = current_val
                elif msg.topic == "cuppy/sensor/temp":
                    self.mqtt_client.plant.current_temperature = current_val
                self.mqtt_client.plant.save()
            except:
                ## How did the sensor even send it if it wasn't a float??? haccccc
                pass

        for topic in self.mqtt_client.topics:
            self.mqtt_client.mqtt_client.subscribe(topic)

        self.mqtt_client.mqtt_client.on_message = on_message

    @background(schedule=0)
    def run(client_id):
        try:
            mqtt_client = MQTTCentralClient.objects.get(client_id=uuid.UUID(client_id))
        except:
            # ermmmmm wtf happened????
            return
        
        mqtt_sub = MQTTSubscriber(mqtt_client)
        mqtt_sub.connect_mqtt()
        mqtt_sub.mqtt_client.mqtt_client.loop_start()
        mqtt_sub.subscribe()

        while not mqtt_sub.mqtt_client.should_stop:
            mqtt_sub.mqtt_client.refresh_from_db()
    
        print("Stopped central")
        mqtt_sub.mqtt_client.mqtt_client.loop_stop()
        mqtt_sub.mqtt_client.mqtt_client.disconnect()



# if __name__ == "__main__":
#     run()
@background(schedule=0)
def start_subscriber():
    print('hi there', flush=True)
    central_client = MQTTCentralClient.objects.all().first()

    if central_client is None:
        central_client = MQTTCentralClient()
        central_client.save()
    
    central_client.should_stop = False
    central_client.save()
    central_client.refresh_from_db()
    MQTTSubscriber.run(str(central_client.client_id))

@background(schedule=0)
def stop_subscriber():
    print("Stopping central")
    central_client = MQTTCentralClient.objects.all().first()
    if central_client is not None:
        central_client.should_stop = True
        central_client.save()
        central_client.refresh_from_db()