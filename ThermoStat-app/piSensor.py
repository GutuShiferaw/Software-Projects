import RPi.GPIO as GPIO
import time, urllib.request, json, requests

readPIN = 14
ledPIN = 3

def getCurrentMode():
    with urllib.request.urlopen("http://localhost:8000/mode/1/") as url:
        data = json.load(url)
        if (data['name']=="manual"):
            return False #manual
        else:
            return True #auto
        
        
def getCurrentState():
    with urllib.request.urlopen("http://localhost:8000/state/1/") as url:
        data = json.load(url)
        if (data['name']=="off"):
            return False #off
        else:
            return True #on
        
        
def setCurrentState(val):
    requests.put("http://localhost:8000/state/1/", json = {'name': val})
    
    
def runAuto():
    if (GPIO.input(readPIN)==1):
        GPIO.output(ledPIN, GPIO.HIGH)
        setCurrentState('on')
    else:
        GPIO.output(ledPIN, GPIO.LOW)
        setCurrentState('off')
   
   
def runManual():
    if (getCurrentState()):
        GPIO.output(ledPIN, GPIO.HIGH)
    else:
        GPIO.output(ledPIN, GPIO.LOW)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(readPIN, GPIO.IN)
GPIO.setup(ledPIN, GPIO.OUT)
GPIO.setwarnings(True)

while True:
    if (getCurrentMode()):
        runAuto()
    else:
        runManual()
    time.sleep(5)