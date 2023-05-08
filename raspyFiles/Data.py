import Adafruit_DHT
import RPi.GPIO as GPIO
import time

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

PIR_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def getData():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    motion_detected = GPIO.input(PIR_PIN)
    data = {'temperature': temperature, 'humidity': humidity, 'motion': motion_detected}
    return data

while True:
    data = getData()
    print(data)
    time.sleep(1)
