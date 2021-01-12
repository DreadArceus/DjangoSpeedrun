from rest_framework import serializers
from .models import Ticket, Call, Secret, Result


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'key', 'grid']


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = ['id', 'value']


class SecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secret
        fields = ['id', 'key', 'discord_id']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['game_id', 'winners']
