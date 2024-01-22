from django.shortcuts import render
from rest_framework import viewsets
from .models import Mode, State
from .serializers import ModeSerializer, StateSerializer
from django.http import HttpResponse
import urllib.request, json, requests

class ModeViewSet(viewsets.ModelViewSet):
    queryset = Mode.objects.all()
    serializer_class = ModeSerializer
    
class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

def control(request):
    auth=('pi','password123')
    if request.method == 'POST':
        if request.POST['mode']=='auto':
            values = {'name':'auto'}
            print("AUTO")
        else:
            values = {'name':'manual'}
            print("MANUAL")
        r=requests.put('http://localhost:8000/mode/1/', data=values, auth=auth)
        if  'state' in request.POST:
            if request.POST['state']=='on':
                print("ON")
                values = {'name':'on'}
            else:
                print("OFF")
                values = {'name':'off'}
            r=requests.put('http://localhost:8000/state/1/', data=values, auth=auth)
    
    context = {
        'currentmode': str(Mode.objects.all()[0]),
        'currentstate': str(State.objects.all()[0]),
    }
       
    return render(request, 'myapi/control.html', context)

# Create your views here.
