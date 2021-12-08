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

class MQTTActuator:
    # This is actually a subscriber, not a publisher.
    def __init__(self, p_mqtt_client: MQTTSensorActuatorClient) -> None:
        self.mqtt_client = p_mqtt_client        
        self.sensor_file = p_mqtt_client.value_file
        self.requirements = p_mqtt_client.plant.plant_species

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
        
        if DEBUG:
            def on_disconnect(client, userdata, rc):
                if rc == 0:
                    print("Disconnected to MQTT Broker!")
                else:
                    print("Failed to disconnect, return code %d\n", rc)
            self.mqtt_client.mqtt_client.on_disconnect = on_disconnect
        self.mqtt_client.mqtt_client.disconnect()

        self.mqtt_client.mqtt_client.on_connect = on_connect
        self.mqtt_client.mqtt_client.connect(MQTT_BROKER_URL, MQTT_PORT)

    def subscribe(self):
        def on_message(msg_client, userdata, msg):
            # TODO: Update models here.
            pass
            # Write to the sensor file whatever value you got in msg_client + 2. This should emulate adding water/light/temperature whatever

            ## Do this if the value you got is not between the parameters. also +2 because we can add water/light/temp, we can't really subtract it.
            if DEBUG and MQTT_DEBUG_PRINTS:
                print("Got message {} on topic {}".format(msg.payload.decode(), msg.topic))

            try:
                new_val = float(msg.payload.decode().strip())
            except:
                return # weird value in the sensor file???

            if msg.topic == "cuppy/sensor/lux":
                thresh = 100
                required_value  = self.requirements.average_lux_amount_per_day
                if max(0, required_value - thresh) > new_val: # > required_value + thresh:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val + 2.0))
                if required_value + thresh < new_val: # > required_value + thresh:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val - 2.0))
            elif msg.topic == "cuppy/sensor/moisture":
                min_level  = self.requirements.min_humidity_level
                max_level = self.requirements.max_humidity_level
                if min_level > new_val:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val + 2.0))
                if  max_level < new_val:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val - 2.0))
            elif msg.topic == "cuppy/sensor/temp":
                required_temperature  = self.requirements.target_temperature
                thresh = 1.5 # Celsius
                print(required_temperature, thresh, new_val)
                print("asdhagsbdhabskjhbaskjhbajkshbaksjhbasdjkhbaskdhbasdkjhbasdkjhbasdkjhbasdkjhbasd")
                if required_temperature - thresh > new_val:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val + 2.0))
                if required_temperature + thresh < new_val:
                    with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + self.sensor_file), 'w') as f:
                        f.write(str(new_val - 2.0))

            


        self.mqtt_client.mqtt_client.subscribe(self.mqtt_client.topic)

        self.mqtt_client.mqtt_client.on_message = on_message
        


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
        
        mqtt_actuator = MQTTActuator(mqtt_client)
        mqtt_actuator.connect_mqtt()
        mqtt_actuator.subscribe()
        mqtt_actuator.mqtt_client.mqtt_client.loop_start()

        while not mqtt_actuator.mqtt_client.should_stop_loop:
            mqtt_actuator.mqtt_client.refresh_from_db()
        
        if DEBUG:
            print("Stopped actuators")
        mqtt_actuator.mqtt_client.mqtt_client.loop_stop()
        mqtt_actuator.mqtt_client.mqtt_client.disconnect()


# if __name__ == "__main__":
#     run()
@background(schedule=0)
def start_all_actuators():
    if DEBUG:
        print("started actuators")
    actuators = MQTTSensorActuatorClient.objects.filter(is_actuator=True)

    for a in actuators:
        a.should_stop_loop = False
        a.save()
        a.refresh_from_db()
        MQTTActuator.run(str(a.client_id))
        if DEBUG:
            print("Started ", a.topic)

@background(schedule=0)
def stop_all_actuators():
    if DEBUG:
        print("Stopping actuators")
    actuators = MQTTSensorActuatorClient.objects.filter(is_actuator=True)

    for a in actuators:
        a.should_stop_loop = True
        a.save()
        a.refresh_from_db()