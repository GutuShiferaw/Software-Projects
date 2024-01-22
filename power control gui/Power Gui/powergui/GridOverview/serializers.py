from rest_framework import serializers
from datetime import date
from .models import WindSpeed
from .models import totalLoad, totalPower
from .models import totalDiesel, totalWind, totalSolar,batterySOC, batteryPower
class DateSerializer(serializers.Serializer):
    date = serializers.DateField()

class WindSpeedSerializer(serializers.Serializer):
    speed = serializers.FloatField()

class TotalPowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalPower
        fields = ('power',)

class TotalLoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalLoad
        fields = ('load',)

class DieselSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalDiesel
        fields = ('power',)
class WindSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalWind
        fields = ('power',)
class SolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = totalSolar
        fields = ('power',)
class batterySocSerializer(serializers.ModelSerializer):
    class Meta:
        model = batterySOC
        fields = ('level',)
class batteryPowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = batteryPower
        fields = ('power',)

