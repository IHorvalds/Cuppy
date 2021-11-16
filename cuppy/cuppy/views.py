from django.contrib.auth.models import User, Group
from django.db.models import query
from rest_framework.decorators import permission_classes
from .models import Requirement, Plant
from rest_framework import viewsets, permissions
from cuppy.cuppy.serializers import UserSerializer, GroupSerializer, RequirementSerializer, PlantSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    View, Edit users.
    """
    queryset = User.objects.all().order_by('-date_joined')
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
    permission_classes = [permissions.IsAuthenticated] ## TODO: only is authernticated user belongs to owners group