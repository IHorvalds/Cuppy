import time
import os
import uuid
from cuppy.settings import MQTT_PORT, MQTT_BROKER_URL, DEBUG, BASE_DIR, MQTT_DEBUG_PRINTS
from cuppy.cuppy.models import MQTTSensorActuatorClient, MQTTCentralClient
from background_task import background

"""Background tasks.

The sensors and actuators and everythign related to mqtt, need to be run in parallel
and as far away from the WSGI side of things as possible.

See django-background-tasks https://django-background-tasks.readthedocs.io/en/latest/
"""

# def read_should_stop(sensor):
#     current_value = 0
#     try:
#         with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/stop_" + sensor.value_file), 'r') as f:
#             try:
#                 current_value = int(f.read().strip())
#             except:
#                 current_value = 0
#     except:
#         with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/stop_" + sensor.value_file), 'w') as f:
#             f.write("0")
#     return current_value

# def write_should_stop(sensor, value):
#     with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/stop_" + sensor.value_file), 'w') as f:
#         f.write(str(value))

class MQTTSensor:

    def __init__(self, p_mqtt_client) -> None:
        self.mqtt_client = p_mqtt_client        
        self.sensor_file = p_mqtt_client.value_file

    def get_central_client() -> MQTTCentralClient:
        central_client = MQTTCentralClient.objects.all().first()
        
        if central_client is None:
            central_client = MQTTCentralClient()
            central_client.save()
        
        return central_client

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.mqtt_client.mqtt_client.on_connect = on_connect
        self.mqtt_client.mqtt_client.connect_async(MQTT_BROKER_URL, MQTT_PORT)

    def publish(self):

        should_stop = self.mqtt_client.should_stop_loop

        while True and not should_stop:
            time.sleep(2)

            current_value = self.read_value()


            ## Write 0 in that file if you want it to continue, 1 if you want it to stop
            self.mqtt_client.refresh_from_db()
            should_stop = self.mqtt_client.should_stop_loop
            # print(should_stop)

            result = self.mqtt_client.mqtt_client.publish(self.mqtt_client.topic, current_value)
            # result: [0, 1]
            status = result[0]
            if DEBUG and MQTT_DEBUG_PRINTS:
                if status == 0:
                    print(f"Sent `{current_value}` to topic `{self.mqtt_client.topic}`")
                else:
                    print(f"Failed to send message to topic {self.mqtt_client.topic}")
        
        # Finished. Exit.
        if DEBUG:
            print("Stopped sensors")
        self.mqtt_client.mqtt_client.loop_stop()
        if DEBUG:
            def on_disconnect(client, userdata, rc):
                if rc == 0:
                    print("Disconnected to MQTT Broker!")
                else:
                    print("Failed to disconnect, return code %d\n", rc)
            self.mqtt_client.mqtt_client.on_disconnect = on_disconnect
        self.mqtt_client.mqtt_client.disconnect()

    def read_value(self):
        current_value = 0.0;
        try:
            with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators","sensors", self.sensor_file), 'r') as f:
                try:
                    current_value = float(f.read().strip())
                except:
                    current_value = 0.0
        except:
            with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators","sensors", self.sensor_file), 'w') as f:
                f.write("")
        return current_value


    @background(schedule=0)
    def run(client_id):
        """
        Run this method to connect to the broker and start sending data
        """
        try:
            mqtt_client = MQTTSensorActuatorClient.objects.get(client_id=uuid.UUID(client_id))
        except:
            # ermmmmm wtf happened????
            return
        
        mqtt_sensor = MQTTSensor(mqtt_client)
        mqtt_sensor.mqtt_client.mqtt_client.loop_start()
        mqtt_sensor.connect_mqtt()
        mqtt_sensor.publish()


# if __name__ == "__main__":
#     run()
@background(schedule=0)
def start_all_sensors():
    if DEBUG:
        print("started sensors")
    sensors = MQTTSensorActuatorClient.objects.filter(is_actuator=False)

    for s in sensors:
        s.should_stop_loop = False
        s.save()
        s.refresh_from_db()
        MQTTSensor.run(str(s.client_id))
        if DEBUG:
            print(s.topic)

@background(schedule=0)
def stop_all_sensors():
    if DEBUG:
        print("Stopping sensors")
    sensors = MQTTSensorActuatorClient.objects.filter(is_actuator=False)

    for s in sensors:
        s.should_stop_loop = True
        s.save()
        s.refresh_from_db()