import serial
import time
import datetime
import subprocess
import board
import adafruit_dht
# import psutil
import RPi.GPIO as GPIO
import requests

from myClass import *
from Data import * 

def disable_usb_port_linux(port):
    subprocess.call(["sudo", "ifconfig", port, "down"])

def enable_usb_port_linux(port):
    subprocess.call(["sudo", "ifconfig", port, "up"])

def disable_usb_port(port):
    subprocess.run(['devcon', 'disable', f'USB\\{port}'], check=True, capture_output=True)

def enable_usb_port(port):
    subprocess.run(['devcon', 'enable', f'USB\\{port}'], check=True, capture_output=True)

def checkValues(id):
    return myValues.values[id].val != memValues.values[id].val

def sendValuesToArduino(values,memValues):
    "function to send the values the values that has changed to the arduino"
    for k in range(len(values)):
        if(checkValues(k)):
            sendValue(values[k],myArduino)
            memValues[k].val = values[k].val
            while(len(myArduino.ser.read_all()) == 0):
                time.sleep(0.1)

def makeValues(values):
    "function to search the values for the raspy"
    values[0].val = time.strftime('%H:%M')
    values[1].val = time.strftime("%A")
    values[2].val = time.strftime("%B")
    values[3].val = time.strftime('%Y')
    values[4].val, values[6].val = getTempAndHumid()
    values[5].val, values[9].val = getWeather()
    values[7].val = time.strftime('%d')
    values[8].val = presence
    

def sendValue(value:Value,arduino:Arduino):
    "function to send a value to the arduino"
    # print(f"{value.id}={value.val}")
    myArduino.ser.write(f"{value.id}={value.val}".encode())

def getTempAndHumid():
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            return temp,humidity
        except:
                # print("trouble dht")
                return memValues.values[4].val,memValues.values[6].val
        

def getWeather():
    try:
        response = requests.get(url)
        data = response.json()
        return str(int(float(data['main']['temp']) - 273.15)), data['weather'][0]['description'] 
    except:
        return "T.xt", "descr"

myValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,""),Value("descW",9,"")])
memValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,""),Value("descW",9,"")])
# print(myValues)
myArduino = Arduino("/dev/ttyACM0")
# print(myArduino)
# arduino = serial.Serial(timeout=0)
sensor = adafruit_dht.DHT11(board.D23)
memNow = ""

GPIO.setup(4, GPIO.IN)         #Read output from PIR motion sensor
presence=GPIO.input(4)
api_key = "5317595bb8e0c71dd94fe21a6512e8f4"
city_name = "Paris"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

time.sleep(3)
while True:
    time.sleep(1)
    myvalues = myValues.values
    mymemvalues = memValues.values
    if myvalues[0].val != time.strftime('%H:%M'):
        makeValues(myvalues)
        sendValuesToArduino(myvalues,mymemvalues)
    # if(len(myArduino.ser.read_all()) > 0):
    #     print("ok")
    # print(presence)
    time.sleep(10)
    # what = input("what to do o/f")
    # if what == "f":
    #     disable_usb_port_linux("/dev/ttyACM0")
    # if what == "o":
    #     enable_usb_port_linux("/dev/ttyACM0")
        
