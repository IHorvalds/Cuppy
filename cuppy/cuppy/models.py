from functools import cached_property
from django.db import models
from django.contrib.auth.models import Group
import uuid
from paho.mqtt import client as mqtt_client

class Requirement(models.Model):
    plant_species = models.CharField(max_length=256, primary_key=True)
    min_humidity_level = models.FloatField() ## What do we measure this in???
    max_humidity_level = models.FloatField()
    average_lux_amount_per_day = models.FloatField() ## unit: lux/hour
    target_temperature = models.FloatField()

class Plant(models.Model):
    """
    Default integer id by django
    """
    current_humidity = models.FloatField()
    current_lux = models.FloatField()
    current_temperature = models.FloatField()
    plant_species = models.ForeignKey(Requirement, on_delete=models.DO_NOTHING) ## when we delete the Requirement row, don't delete the plant too
    owner_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True) ## when we delete the Group, set owner to NULL, aka everyone. Change the group ownership before delete a group

class MQTTCentralClient(models.Model):
    """MQTT Central client

    Technically, we don't need a whole entity for this because it's only gonna be one, **but**
    django has this nice ORM so we don't have to deal with it ourselves. Let's let it do its thing.
    """
    client_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    unit_token = models.UUIDField(default=uuid.uuid4, editable=False) ## this __should__ help with not publishing everything to every cup in existence.
    should_stop = models.BooleanField(default=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=False) ## Plant must exist before we can make a sensor. Because i say so.

    @property
    def topics(self):
        return list(x.topic for x in MQTTSensorActuatorClient.objects.filter(central_client_id=self.client_id, is_actuator=False))

    @cached_property
    def mqtt_client(self):
        return mqtt_client.Client(str(self.client_id), userdata=str(self.unit_token))

class MQTTSensorActuatorClient(models.Model):
    """MQTT Sensor/Actuator Client
    We keep a reference to its randomly generated client_id and its topic. 
    So we can just reinitialize without losing data from the broker. 

    Also, tie each sensor to a plant. There could be multiple plants in the pot. We don't care.

    Sensors push messages to the broker, actuators pull.

    Sensors push periodically, actuators do something when they get a message.
    """
    client_id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    is_actuator = models.BooleanField()
    should_stop_loop = models.BooleanField(default=True)
    value_file = models.CharField(max_length=256)
    topic = models.CharField(max_length=256) ## Only one logical sensor/actuator per topic. 
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=False) ## Plant must exist before we can make a sensor. Because i say so.
    central_client = models.ForeignKey(MQTTCentralClient, on_delete=models.SET_NULL, null=True)

    @cached_property
    def mqtt_client(self):
        return mqtt_client.Client(str(self.client_id))