from serial import tools,Serial
from serial.tools import list_ports
import time
import subprocess
import RPi.GPIO as GPIO
import serial




class Arduino:
    # GPIO.setup(4, GPIO.IN)         #Read output from PIR motion sensor
    def __init__(self, baud_rate,hubnbr) -> None:
        self.hubnbr = hubnbr
        self.turnArdOn()
        self.baud_rate = baud_rate
        self.com_port = self.find_port()
        self.ser = Serial(self.com_port, self.baud_rate, timeout = 1)
        print(self)
        
    def toggle_usb_power(self, action):
        command = f"sudo uhubctl -l 1-1 -p {self.hubnbr} -a {action}"
        subprocess.call(command, shell=True)

    def turnArdOn(self):
        self.toggle_usb_power("on")
        self.state = True
    
    def turnArdOff(self):
        self.ser.close()
        self.toggle_usb_power("off")
        self.state = False

    def connectArd(self):
        for _ in range(10):
            try:
                self.ser = Serial(self.com_port, self.baud_rate, timeout = 1)
                print("successfull reconnect")
                return True
            except:
                self.com_port = self.find_port()
        print("reconnect failed")
        return False

    def closeArd(self):
        self.ser.close()
        

    def find_port(self):
        for port in list_ports.comports():
            try:
                arduino = Serial(port[0], self.baud_rate, timeout=1)
                time.sleep(2)
                res = arduino.readlines()
                if b'Screen' in res and self.baud_rate == 9600:
                    arduino.flush()
                    return port[0]
                if b'\r\n' in res and self.baud_rate == 115200:
                    arduino.flush()
                    return port[0]
                arduino.flush()
            except:
                # print("did not find any available port")
                pass
        print("did not find any available port")
        return None
    
    def check_message(ser, expected_message):
        while True:
            received_message = ser.readline().decode().strip()
            print(f"Received: {received_message}")
            if received_message == expected_message:
                return True

    def __str__(self) -> str:
        return f"the arduino with a baudrate : {self.baud_rate} \nis connected to port: {self.com_port}"
    

# screen = Arduino(9600)
# sand = Arduino(115200)