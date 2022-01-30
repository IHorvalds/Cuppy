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
