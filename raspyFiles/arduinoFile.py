import serial
import time
import subprocess
import board
# import psutil
import RPi.GPIO as GPIO
from myClass import *




def toggle_usb_power(hub_number, k, action):
    command = f"sudo uhubctl -l {hub_number} -p {k} -a {action}"
    subprocess.call(command, shell=True)

def turnArdOn(myArduino):
     toggle_usb_power("1-1",1,"on")
     myArduino = Arduino("/dev/ttyACM0",9600)
     myValues.valuesToZ()
     return myArduino

def turnArdOff(myArduino):
     myArduino.ser.close()
     toggle_usb_power("1-1",1,"off")
     return myArduino
     

    

# def makeValues(values):
#     "function to search the values for the raspy"
#     values[0].val = time.strftime('%H:%M')
#     values[1].val = time.strftime("%A")
#     values[2].val = time.strftime("%B")
#     values[3].val = time.strftime('%Y')
#     values[4].val, values[6].val = getTempAndHumid()
#     values[5].val, values[9].val = getWeather()
#     values[7].val = time.strftime('%d')
#     # values[8].val = str(presence)
    


def getTempAndHumid():
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            return temp,humidity
        except:
                # print("trouble dht")
                return "NA","NA"
        
toggle_usb_power("1-1",1,"on")
myArduino = Arduino("/dev/ttyACM0",9600)


GPIO.setup(4, GPIO.IN)         #Read output from PIR motion sensor


def launchArduino():
    time.sleep(3)
    # myArduino.connectArd(myArduino)
    while True:
        # print("here")
        time.sleep(1)
        if myArduino.state == True:
            myValues.getAllValue()
            print("lkjdsqhfg")
            myValues.sendValuesToArduino(myArduino)
        if myArduino.state == False:
            myValues.getAllValue()
        print(myValues)
