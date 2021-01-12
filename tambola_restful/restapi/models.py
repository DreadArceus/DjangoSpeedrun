from django.db import models
from django.contrib.postgres.fields import ArrayField


class Ticket(models.Model):
    key = models.CharField(max_length=13, blank=False)
    grid = ArrayField(
        ArrayField(
            models.CharField(max_length=2),
            size=3,
        ),
        size=9,
    )


class Call(models.Model):
    value = models.IntegerField()


class Secret(models.Model):
    key = models.CharField(max_length=13, blank=False)
    discord_id = models.BigIntegerField()


class Result(models.Model):
    game_id = models.IntegerField()
    winners = ArrayField(
        ArrayField(
            models.CharField(max_length=50),
            size=2,
        ),
    )
