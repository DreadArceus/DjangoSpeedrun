from django.db import models
from django.contrib.postgres.fields import ArrayField


class Ticket(models.Model):
    grid = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=9,
        ),
        size=3,
    )
