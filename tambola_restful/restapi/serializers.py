from rest_framework import serializers
from .models import GameTickets, GameCalls, GameSecrets, Result


class GameTicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTickets
        fields = ['game_id', 'tickets']


class GameCallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameCalls
        fields = ['game_id', 'calls']


class GameSecretsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSecrets
        fields = ['game_id', 'secrets']


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['game_id', 'winners']
