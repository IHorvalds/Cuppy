from django.test import TestCase
# Create your tests here.

import os
import time
from cuppy.settings import BASE_DIR
from cuppy.cuppy.models import MQTTCentralClient, MQTTSensorActuatorClient, Plant, Requirement
from cuppy_sensors_actuators.sensors.Sensors import MQTTSensor
from cuppy_sensors_actuators.actuators.Actuators import MQTTActuator
from cuppy_sensors_actuators.sensors.Sensors import stop_all_sensors, MQTTSensor

def default_plant():
    requirement = Requirement()
    requirement.plant_species = "nuj"
    requirement.min_humidity_level = 1
    requirement.max_humidity_level = 10
    requirement.average_lux_amount_per_day = 5
    requirement.target_temperature = 7
    requirement.save()
    plant = Plant()
    plant.current_humidity = 0
    plant.current_lux = 0
    plant.current_temperature = 1
    plant.plant_species = requirement
    plant.save()
    return plant


class TempSensorTestCase (TestCase):
    # sensor = None
    # database = None
    def setUp(self):
        # MQTTSENSORActuatorClient() pentru a crea in noua baza de date obiectul de care avem nevoie si dupa trebuie populata baza.
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = False
        self.client.plant = plant
        self.client.value_file = "temperature_value.txt"
        self.client.save()
        
    async def test_sensor_can_read(self):
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "temperature_value.txt"), 'w') as f:
                f.write("30.0")
        
        self.client.should_stop_loop = False
        m = MQTTSensor(self.client)
        
        self.assertEqual(m.read_value(),30.0)
        
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "temperature_value.txt"))
        
class TempActuatorTestCase(TestCase):
    def setUp(self):
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = True
        self.client.plant = plant
        self.client.value_file = "temperature_value.txt"
        self.client.save()
        
    async def test_actuator_can_write(self):
        
        value = 2.0
        msg = type('',(object,),{"topic": "cuppy/sensor/temp"})()
        m = MQTTActuator(self.client)
        m.write_value("",msg,value)
        
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators","sensors", self.client.value_file), 'r') as f:
            value_from_file = float(f.read().strip())
        
        # 2 < 7 => trebuie sa adaugam la expected value un 2
        self.assertEqual(value+2,value_from_file)
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "temperature_value.txt"))
        
class HumSensorTestCase(TestCase):
    def setUp(self):
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = False
        self.client.plant = plant
        self.client.value_file = "moisture_value.txt"
        self.client.save()
        
    async def test_sensor_can_read(self):
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "moisture_value.txt"), 'w') as f:
                f.write("30.0")
        
        self.client.should_stop_loop = False
        m = MQTTSensor(self.client)
        
        self.assertEqual(m.read_value(),30.0)
        
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "moisture_value.txt"))
        
class HumActuatorTestCase(TestCase):
    def setUp(self):
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = True
        self.client.plant = plant
        self.client.value_file = "moisture_value.txt"
        self.client.save()
        
    async def test_actuator_can_write(self):
        
        value = -1.0
        msg = type('',(object,),{"topic": "cuppy/sensor/moisture"})()
        m = MQTTActuator(self.client)
        m.write_value("",msg,value)
        
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators","sensors", self.client.value_file), 'r') as f:
            value_from_file = float(f.read().strip())
        
        # 2 < 7 => trebuie sa adaugam la expected value un 2
        self.assertEqual(value+2,value_from_file)
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "moisture_value.txt"))
    
    
class LuxSensorTestCase (TestCase):
    # sensor = None
    # database = None
    def setUp(self):
        # MQTTSENSORActuatorClient() pentru a crea in noua baza de date obiectul de care avem nevoie si dupa trebuie populata baza.
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = False
        self.client.plant = plant
        self.client.value_file = "lux_value.txt"
        self.client.save()
        
    async def test_sensor_can_read(self):
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "lux_value.txt"), 'w') as f:
                f.write("30.0")
        
        self.client.should_stop_loop = False
        m = MQTTSensor(self.client)
        
        self.assertEqual(m.read_value(),30.0)
        
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "lux_value.txt"))
        
class  LuxActuatorTestCase(TestCase):
    def setUp(self):
        plant = default_plant()
        
        self.client = MQTTSensorActuatorClient()
        self.client.is_actuator = True
        self.client.plant = plant
        self.client.value_file = "lux_value.txt"
        self.client.save()
        
    async def test_actuator_can_write(self):
        
        value = -2.0
        msg = type('',(object,),{"topic": "cuppy/sensor/lux"})()
        m = MQTTActuator(self.client)
        m.write_value("",msg,value)
        
        with open(os.path.join(BASE_DIR, "cuppy_sensors_actuators","sensors", self.client.value_file), 'r') as f:
            value_from_file = float(f.read().strip())
        
        # 2 < 7 => trebuie sa adaugam la expected value un 2
        self.assertEqual(value+2,value_from_file)
        os.remove(os.path.join(BASE_DIR, "cuppy_sensors_actuators/sensors/" + "lux_value.txt"))

# penutr central si probabil o sa fie nevoie sa testam daca acesta reuseste sa scrie o valoare data in baza de date.
# 4 teste pentru senzorii/actuatori de moisture/lux
# teste api / ca poti sa creezi plante/useri