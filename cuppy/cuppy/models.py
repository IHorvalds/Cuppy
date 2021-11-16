from django.db import models
from django.contrib.auth.models import Group

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
