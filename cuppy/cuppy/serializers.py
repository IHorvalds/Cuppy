from django.contrib.auth.models import User, Group
from .models import Requirement, Plant
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class RequirementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Requirement
        fields = ['url', 'plant_species', 'min_humidity_level', 'max_humidity_level', 'average_lux_amount_per_day', 'target_temperature']

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = ['url', 'current_humidity', 'current_lux', 'current_temperature', 'plant_species', 'owner_group']