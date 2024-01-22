from io import BytesIO
import urllib
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DateSerializer
from .serializers import WindSpeedSerializer
from .models import DateModel
from .models import WindSpeed
from .models import totalPower
from .models import totalLoad
from .models import totalDiesel, totalWind, totalSolar,batterySOC, batteryPower
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import TotalPowerSerializer, TotalLoadSerializer, DieselSerializer, WindSerializer, SolarSerializer,batterySocSerializer, batteryPowerSerializer

# Create your views here.

def GridOverview(request):
    last_date_id = DateModel.objects.last().id
    my_date_model = DateModel.objects.get(id=last_date_id) 
    date = my_date_model.date
    
    last_speed_id = WindSpeed.objects.last().id
    speed_model = WindSpeed.objects.get(id=last_speed_id)
    speed = speed_model.average_speed  
    
    context = {'date': date, 'speed': speed}
    return render(request, 'overview.html', context)
    


@api_view(['POST'])
def save_date(request):
    serializer = DateSerializer(data=request.data)
    if serializer.is_valid():
        date_data = serializer.validated_data['date']
        date_model = DateModel(date=date_data)
        date_model.save()
        return Response({'success': True})
    else:
        return Response(serializer.errors, status=400)
@api_view(['POST'])
def save_speed(request):
    serializer = WindSpeedSerializer(data=request.data)
    if serializer.is_valid():
        speed_data = serializer.validated_data['speed']
        speed_model = WindSpeed(average_speed=speed_data)
        speed_model.save()
        return Response({'success': True})
    else:
        return Response(serializer.errors, status=400)

def dateview(request):
    last_object_id = DateModel.objects.last().id
    my_model = DateModel.objects.get(id=last_object_id) 
    date = my_model.date
    context = {'date': date}
    return render(request, 'overview.html', context)

def windview(request):
    last_id = WindSpeed.objects.last().id
    speed_model = WindSpeed.objects.get(id=last_id)
    speed = speed_model.average_speed  
    context = {'speed': speed}
    return render(request, 'overview.html', context)

@csrf_exempt
def save_totalPower(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        power_data = totalPower(power=data['power'])
        power_data.save()
        return JsonResponse({'success': True})
@csrf_exempt
def save_totalLoad(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        power_data = totalLoad(load=data['load'])
        power_data.save()
        return JsonResponse({'success': True})

@csrf_exempt
def save_diesel(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        power_data = totalDiesel(power=data['power'])
        power_data.save()
        return JsonResponse({'success': True})

@csrf_exempt
def save_wind(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        power_data = totalWind(power=data['power'])
        power_data.save()
        return JsonResponse({'success': True})


@csrf_exempt
def save_solar(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        power_data = totalSolar(power=data['power'])
        power_data.save()
        return JsonResponse({'success': True})
@csrf_exempt
def save_batterySoc(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        soc_data = batterySOC(level=data['level'])
        soc_data.save()
        return JsonResponse({'success': True})
@csrf_exempt
def save_batteryPower(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        battpower_data = batteryPower(power=data['power'])
        battpower_data.save()
        return JsonResponse({'success': True})


def power_load_vs_time(request):
    # get the latest objects for TotalPower and TotalLoad
    power_data = totalPower.objects.latest('id')
    load_data = totalLoad.objects.latest('id')

    # convert the latest objects to dictionaries using serializers
    power_serializer = TotalPowerSerializer(power_data)
    load_serializer = TotalLoadSerializer(load_data)
    

    # create a dictionary containing time, power, and load
    data = {
        'time': [0]*24,
        'power': [0]*24,
        'load': [0]*24,
    }

    # populate the power and load data in the dictionary
    data['power'] = power_serializer.data['power']
    data['load'] = load_serializer.data['load']
    data['time'] = list(range(1, 25))
    return JsonResponse(data)

def gen_vs_time(request):
    # get the latest objects for TotalPower and TotalLoad
    diesel = totalDiesel.objects.latest('id')
    wind = totalWind.objects.latest('id')
    solar = totalSolar.objects.latest('id')

    # convert the latest objects to dictionaries using serializers
    diesel_serializer = DieselSerializer(diesel)
    wind_serializer = WindSerializer(wind)
    solar_serializer = SolarSerializer(solar)

    # create a dictionary containing time, power, and load
    data = {
        'time': [0]*24,
        'diesel': [0]*24,
        'wind': [0]*24,
        'solar': [0]*24
    }
    # populate the power and load data in the dictionary
    data['diesel'] = diesel_serializer.data['power']
    data['wind'] = wind_serializer.data['power']
    data['solar'] = solar_serializer.data['power']
    data['time'] = list(range(1, 25))
    return JsonResponse(data)

def Batt_vs_time(request):
    # get the latest objects for TotalPower and TotalLoad
    level = batterySOC.objects.latest('id')
    batt_power = batteryPower.objects.latest('id')

    # convert the latest objects to dictionaries using serializers
    soc_serializer = batterySocSerializer(level)
    battpower_serializer = batteryPowerSerializer(batt_power)

    # create a dictionary containing time, power, and load
    data = {
        'time': [0]*24,
        'level': [0]*24,
        'power': [0]*24
    }
    # populate the power and load data in the dictionary
    data['level'] = soc_serializer.data['level']
    data['power'] = battpower_serializer.data['power']
    data['time'] = list(range(1, 25))
    return JsonResponse(data)
