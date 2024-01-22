from django.db import models

class DateModel(models.Model):
    date = models.DateField()
    # add more fields as needed
class WindSpeed(models.Model):
    average_speed = models.FloatField()
class totalPower(models.Model):
    power = models.JSONField()
class totalLoad(models.Model):
    load = models.JSONField()
class totalDiesel(models.Model):
    power = models.JSONField()
class totalWind(models.Model):
    power = models.JSONField()
class totalSolar(models.Model):
    power = models.JSONField()
class batterySOC(models.Model):
    level = models.JSONField()
class batteryPower(models.Model):
    power = models.JSONField()