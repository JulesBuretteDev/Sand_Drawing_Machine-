import serial
import time
import datetime
import subprocess
import board
import adafruit_dht
import psutil
import RPi.GPIO as GPIO
import requests

class Value:

    def __init__(self,name:str,id:int,val:str):
        self.name = name
        self.id = id
        self.val = val

    def __str__(self) -> str:
        return f"{self.name}: {self.val} : id : {self.id}\n"

class Values:

    def __init__(self,values : list[Value] = []) -> None:
        self.values = values

    def addVal(self, values):
        self.values.append(values)

    def __str__(self) -> str:
        res = ""
        for val in self.values:
            res += val.__str__()
        return f"{res}"

class Arduino:
    def __init__(self,port, baud_rate:int = 9600) -> None:
        self.com_port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.com_port, self.baud_rate, timeout = 1)


    def find_port(self):
        ports = ['/dev/ttyACM{}'.format(i) for i in range(1, 10)]
        for port in ports:
            try:
                arduino = serial.Serial(port, 9600, timeout=1)
                arduino.close()
                return port
            except:
                pass
        print("did not find any available port")
        return None
    
    def __str__(self) -> str:
        return f"port: {self.com_port}"

def disable_usb_port_linux(port):
    subprocess.run(['sudo', 'udevadm', 'test-builtin', 'usb', f'{port}:1.0'], check=True, capture_output=True)
    subprocess.run(['sudo', 'udevadm', 'trigger', '--attr-match=subsystem=usb', '--action=remove'], check=True)

def enable_usb_port_linux(port):
    subprocess.run(['sudo', 'udevadm', 'test-builtin', 'usb', f'{port}:1.0'], check=True, capture_output=True)
    subprocess.run(['sudo', 'udevadm', 'trigger', '--attr-match=subsystem=usb', '--action=add'], check=True)

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
                time.sleep(0.5)

def makeValues(values):
    "function to search the values for the raspy"
    values[0].val = time.strftime('%H:%M')
    values[1].val = time.strftime("%A")
    values[2].val = time.strftime("%B")
    values[3].val = time.strftime('%Y')
    values[4].val = sensor.temperature
    values[5].val = getWeather()
    values[6].val = sensor.humidity
    values[7].val = time.strftime('%d')
    values[8].val = presence

def sendValue(value:Value,arduino:Arduino):
    "function to send a value to the arduino"
    myArduino.ser.write(f"{value.id}={value.val}".encode())

def getTempAndHumid():
        temp = sensor.temperature
        humidity = sensor.humidity
        return temp,humidity


for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

def getWeather():
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']

myValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,"")])
memValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,"")])
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
    print(presence)
    time.sleep(10)
        
