"""cuppy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import routers
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from cuppy.cuppy import views

schema_view = get_swagger_view(title="Cuppy API")

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"plant_requirement", views.RequirementViewSet)
router.register(r"plants", views.PlantViewSet)
router.register(r"sensors", views.SensorActuatorViewSet)
router.register(r"central", views.CentralClientViewSet)
# router.register(r"openapi", schema_view)

urlpatterns = [
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("sensor_control/", views.StartStopSensors.as_view(), name="sensors"),
    path(
        "central_control/", views.StartStopCentralSubscriber.as_view(), name="central"
    ),
    path("actuator_control/", views.StartStopActuators.as_view(), name="actuator"),
    path("openapi/", schema_view, name="openapi"),
    path("", include(router.urls)),
]
