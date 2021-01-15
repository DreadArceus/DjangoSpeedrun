# Generated by Django 3.1.5 on 2021-01-14 14:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0005_auto_20210112_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game_Calls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField()),
                ('calls', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Game_Secrets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField()),
                ('secrets', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), size=3), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Game_Tickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.IntegerField()),
                ('tickets', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=2), size=3), size=9), size=None)),
            ],
        ),
        migrations.DeleteModel(
            name='Call',
        ),
        migrations.DeleteModel(
            name='Secret',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]