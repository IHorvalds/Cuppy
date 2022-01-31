from django.contrib.auth.models import User, Group
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from cuppy_sensors_actuators.actuators.Actuators import start_all_actuators

from cuppy_sensors_actuators.sensors.Sensors import start_all_sensors, stop_all_sensors
from cuppy_sensors_actuators.actuators.Actuators import (
    start_all_actuators,
    stop_all_actuators,
)
from .models import Requirement, Plant, MQTTSensorActuatorClient, MQTTCentralClient
from rest_framework import viewsets, permissions, authentication
from cuppy.cuppy.serializers import (
    UserSerializer,
    GroupSerializer,
    RequirementSerializer,
    PlantSerializer,
    MQTTCentralClientSerializer,
    MQTTSensorActuatorClientSerializer,
)

from .mqtt_subscriber.Subscriber import start_subscriber, stop_subscriber


class UserViewSet(viewsets.ModelViewSet):
    """
    View, Edit users.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    View, Edit groups
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]


class RequirementViewSet(viewsets.ModelViewSet):
    """
    View, Edit plant requirements
    """

    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [permissions.AllowAny]


class PlantViewSet(viewsets.ModelViewSet):
    """
    \... with plants
    """

    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  ## TODO: only is authernticated user belongs to owners group


class SensorActuatorViewSet(viewsets.ModelViewSet):
    """
    \... and with sensors and actuators
    """

    queryset = MQTTSensorActuatorClient.objects.all()
    serializer_class = MQTTSensorActuatorClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class CentralClientViewSet(viewsets.ModelViewSet):
    """

    \... and finally with the central MQTT client.
    """

    queryset = MQTTCentralClient.objects.all()
    serializer_class = MQTTCentralClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartStopSensors(APIView):
    """Start and Stop Sensors

    Initialize and start the sensors. This will connect them to the MQTT broker.
    OR
    Stop the sensors. Disconnect them from the MQTT broker.
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        # operation_description="apiview post description override",
        manual_parameters=[
            openapi.Parameter(
                "method",
                openapi.IN_QUERY,
                description="Operation Name",
                type=openapi.TYPE_STRING,
                enum=["start", "stop"],
                required=True,
            )
        ],
        responses={
            # 200,
            500: "Issue with application. Please review views.py > class StartStopSensors!"
        },
    )
    def get(self, request, format=None):
        if "method" in request.query_params and request.query_params["method"].lower() == "start" :
            start_all_sensors()
            return Response(status=200)
        if "method" in request.query_params and request.query_params["method"].lower() == "stop":
            stop_all_sensors()
            return Response(status=200)

        return Response(
            status=500,
            data={"error": "Issue with sensors. Please review class StartStopSensors!"},
        )


class StartStopCentralSubscriber(APIView):
    """Start and stop the central subscriber."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        # operation_description="apiview post description override",
        manual_parameters=[
            openapi.Parameter(
                "method",
                openapi.IN_QUERY,
                description="Operation Name",
                type=openapi.TYPE_STRING,
                enum=["start", "stop"],
                required=True,
            )
        ],
        responses={
            # 200,
            500: "Issue with application. Please review views.py > class StartStopCentralSubscriber!"
        },
    )
    def get(self, request, format=None):
        if "method" in request.query_params and request.query_params["method"].lower() == "start":
            start_subscriber()
            return Response(status=200)
        if "method" in request.query_params and request.query_params["method"].lower() == "stop":
            stop_subscriber()
            return Response(status=200)

        return Response(
            status=500,
            data={
                "error": "Issue with application. Please review views.py > class StartStopCentralSubscriber!"
            },
        )


class StartStopActuators(APIView):
    """
    Start stop the actuators
    """

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        # operation_description="apiview post description override",
        manual_parameters=[
            openapi.Parameter(
                "method",
                openapi.IN_QUERY,
                description="Operation Name",
                type=openapi.TYPE_STRING,
                enum=["start", "stop"],
                required=True,
            )
        ],
        responses={
            # 200,
            500: "Issue with application. Please review views.py > class StartStopActuators!"
        },
    )
    def get(self, request, format=None):
        if "method" in request.query_params and request.query_params["method"].lower() == "start":
            start_all_actuators()
            return Response(status=200)
        if "method" in request.query_params and request.query_params["method"].lower() == "stop":
            stop_all_actuators()
            return Response(status=200)

        return Response(
            status=500,
            data={
                "error": "Issue with application. Please review views.py > class StartStopActuators!"
            },
        )


class InitializePlant(APIView):
    """
    """

    permission_classes = [permissions.IsAuthenticated]
    
    requirements = Requirement.objects.all()
    plant_species = list(map(lambda plant: plant.plant_species, requirements))
    @swagger_auto_schema(
        # operation_description="apiview post description override",
        manual_parameters=[
            openapi.Parameter(
                "plant",
                openapi.IN_QUERY,
                description="Plant name",
                type=openapi.TYPE_STRING,
                enum=plant_species,
                required=True,
            ),
            openapi.Parameter(
                "target_temperature",
                openapi.IN_QUERY,
                description="Target temperature",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "average_lux_amount_per_day",
                openapi.IN_QUERY,
                description="Average lux amount per day",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "min_humidity",
                openapi.IN_QUERY,
                description="Minimum humidity",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                "max_humidity",
                openapi.IN_QUERY,
                description="Maximum humidity",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            # 200,
            500: "Issue with application."
        },
    )
    def get(self, request, format=None):
        plant_species_id = ""
        original_requirements = []
        custom_max_humidity = ""
        custom_min_humidity = ""
        custom_target_temperature = ""
        custom_average_lux_amount_per_day = ""
        create_new_requirements = False

        try:
            plant_species_id = request.query_params["plant"]
            original_requirements = Requirement.objects.filter(plant_species=plant_species_id)[0]
        except:
            return Response(
                status=500,
                data={"error": "Please select the plant species."},
            )
        try:        
            custom_max_humidity = request.query_params["max_humidity"]
            create_new_requirements = True
        except:
            custom_max_humidity = original_requirements.max_humidity_level


        try:
            custom_min_humidity = request.query_params["min_humidity"]
            create_new_requirements = True
        except:
            custom_min_humidity = original_requirements.min_humidity_level


        try:
            custom_target_temperature = request.query_params["target_temperature"]
            create_new_requirements = True
        except:
            custom_target_temperature = original_requirements.target_temperature


        try:            
            custom_average_lux_amount_per_day = request.query_params["average_lux_amount_per_day"]
            create_new_requirements = True
        except:
            custom_average_lux_amount_per_day = original_requirements.average_lux_amount_per_day

        if not(create_new_requirements):
            p = Plant(current_humidity = 0, current_temperature = 0, current_lux = 0, plant_species_id = plant_species_id)
            p.save()
            return Response(status=200)
        else:
            requirements = Requirement.objects.all()
            last_custom_id = ""
            for r in requirements:
                if(plant_species_id  + "_custom" in r.plant_species):
                    if last_custom_id == "" or last_custom_id < r.plant_species:
                        last_custom_id = r.plant_species
            newPlantId = ""
            if last_custom_id == "":
                newPlantId = plant_species_id  + "_custom1"
            else:
                newPlantId = plant_species_id  + "_custom" + str(int(last_custom_id[last_custom_id.index("custom")+6:]) + 1)

            r = Requirement(
                plant_species=newPlantId,
                target_temperature = custom_target_temperature,
                min_humidity_level = custom_min_humidity,
                max_humidity_level = custom_max_humidity,
                average_lux_amount_per_day = custom_average_lux_amount_per_day
            )
            r.save()

            p = Plant(current_humidity = 0, current_temperature = 0, current_lux = 0, plant_species_id = newPlantId)
            p.save()
            return Response(status=200)

        return Response(status=200)
    
        

class InitializePlantCustom(APIView):
    """
    """

    permission_classes = [permissions.IsAuthenticated]
    
    requirements = Requirement.objects.all()
    plant_species = list(map(lambda plant: plant.plant_species, requirements))
    @swagger_auto_schema(
        # operation_description="apiview post description override",
        manual_parameters=[
            openapi.Parameter(
                "plant",
                openapi.IN_QUERY,
                description="Plant name",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "target_temperature",
                openapi.IN_QUERY,
                description="Target temperature",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "average_lux_amount_per_day",
                openapi.IN_QUERY,
                description="Average lux amount per day",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "min_humidity",
                openapi.IN_QUERY,
                description="Minimum humidity",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "max_humidity",
                openapi.IN_QUERY,
                description="Maximum humidity",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            # 200,
            500: "Issue with application."
        },
    )
    def get(self, request, format=None):
        plant_species = request.query_params["plant"]
        custom_max_humidity = request.query_params["max_humidity"]
        custom_min_humidity = request.query_params["min_humidity"]
        custom_target_temperature = request.query_params["target_temperature"]  
        custom_average_lux_amount_per_day = request.query_params["average_lux_amount_per_day"]

        r = Requirement(
            plant_species = plant_species,
            target_temperature = custom_target_temperature,
            min_humidity_level = custom_min_humidity,
            max_humidity_level = custom_max_humidity,
            average_lux_amount_per_day = custom_average_lux_amount_per_day
        )
        r.save()

        p = Plant(current_humidity = 0, current_temperature = 0, current_lux = 0, plant_species_id = plant_species)
        p.save()
        return Response(status=200)
    