from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from tambola.draft_api.serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializers = UserSerializer
    permissions = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializers = GroupSerializer
    permissions = [permissions.IsAuthenticated]