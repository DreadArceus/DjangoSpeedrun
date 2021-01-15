from django.db import models
from django.contrib.postgres.fields import ArrayField


class GameTickets(models.Model):
    game_id = models.BigIntegerField()
    tickets = ArrayField(
        ArrayField(  # grid
            ArrayField(
                models.CharField(max_length=2),
                size=3,
            ),
            size=9,
        )
    )


class GameCalls(models.Model):
    game_id = models.BigIntegerField()
    calls = ArrayField(models.IntegerField())


class GameSecrets(models.Model):
    game_id = models.BigIntegerField()
    secrets = ArrayField(
        models.JSONField()
    )


class Result(models.Model):
    game_id = models.BigIntegerField()
    winners = ArrayField(
        ArrayField(
            models.CharField(max_length=50),
            size=2,
        ),
    )
