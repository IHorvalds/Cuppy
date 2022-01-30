from uuid import RESERVED_MICROSOFT
from background_task.models import Task
from django.contrib.auth.models import User, UserManager
from django.db.models.query import RawQuerySet

from django.test import TestCase

from cuppy.cuppy.models import MQTTCentralClient, Plant, Requirement

# Create your tests here.

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

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', email='bob@example.com', password='12345')
        
    def test_create_user(self):
        userMock = User.objects.get(username='bob')
        self.assertEqual(userMock,self.user)
        
class CreateRequirementTestCase(TestCase):
    def setUp(self):
        self.requirement = Requirement()
        self.requirement.plant_species = "nuj"
        self.requirement.min_humidity_level = 1
        self.requirement.max_humidity_level = 10
        self.requirement.average_lux_amount_per_day = 5
        self.requirement.target_temperature = 7
        self.requirement.save()
        
    def test_create_requirement(self):
        requirementMock = Requirement.objects.get(plant_species="nuj")
        self.assertEqual(requirementMock,self.requirement)
        
class CreatePlantTestCase(TestCase):
    def setUp(self):
        requirement = Requirement()
        requirement.plant_species = "nuj"
        requirement.min_humidity_level = 1
        requirement.max_humidity_level = 10
        requirement.average_lux_amount_per_day = 5
        requirement.target_temperature = 7
        requirement.save()
        self.plant = Plant()
        self.plant.current_humidity = 0
        self.plant.current_lux = 0
        self.plant.current_temperature = 1
        self.plant.plant_species = requirement
        self.plant.save()
    
    def test_create_plant(self):
        plantMock = Plant.objects.get(plant_species="nuj")
        self.assertEqual(plantMock,self.plant)
        
class CreateMQTTCentralTestCase(TestCase):
    def setUp(self):
        plant = default_plant()
        self.central = MQTTCentralClient()
        self.central.plant = plant
        self.central.save()
        self.id = self.central.client_id
        
    def test_create_central(self):
        centralMock = MQTTCentralClient.objects.get(client_id = self.id)
        self.assertEqual(centralMock,self.central)