from serial import tools,Serial
from serial.tools import list_ports
import time
import adafruit_dht
import board
import requests



api_key = "5317595bb8e0c71dd94fe21a6512e8f4"
city_name = "Paris"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

portNames = [
    "/dev/ttyUSB0",
    "/dev/ttyUSB1",
    "/dev/ttyUSB2",
    "/dev/ttyUSB3",
    "/dev/ttyACM0",
    "/dev/ttyACM1",
    "/dev/ttyACM2",
    "/dev/ttyACM3"
]
sensor = adafruit_dht.DHT11(board.D23)



class Arduino:
    def __init__(self,port, baud_rate) -> None:
        self.baud_rate = baud_rate
        self.com_port = port
        self.ser = Serial(self.com_port, self.baud_rate, timeout = 1)
        self.state = True
        

    def connectArd(self):
        for _ in range(10):
            try:
                self.ser = Serial(self.com_port, self.baud_rate, timeout = 1)
            except:
                self.find_port()

    def closeArd(self):
        self.ser.close()
        

    def get_tty_devices(self):
        tty_devices = []
        for port in portNames:
            tty_devices.append(port)
        return self.find_port(tty_devices)

    def find_port(self):
        # print(portNames)

        for port in portNames:
            try:
                arduino = Serial(port, self.baud_rate, timeout=1)
                self.check_message(arduino,"Grbl 1.1h ['$' for help]")
                # arduino.write("$$".encode())
                # cpt = 0
                # while(len(arduino.read_all()) == 0 and cpt < 5):
                #     cpt +=1
                #     time.sleep(1)
                # print(arduino.read_all())
                print(f"connected to port {port} with a baudrate of {self.baud_rate}")
                return port
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
        return f"port: {self.com_port}"
    



class Value:

    def __init__(self,name:str,id:int,val:str,send:int):
        self.name = name
        self.id = id
        self.val = val
        self.send = send

    def __str__(self) -> str:
        return f"{self.name}: {self.val} : id : {self.id} : state : {self.send}\n"

class Values:
    # allValues = ["heure","jour","mois","annee","temp","netTemp","humid","dateJour","presence","descW","notNow","plotX","plotY"]

    def __init__(self) -> None:
        self.heure = Value("heure",0,"",0)
        self.jour = Value("jour",1,"",0)
        self.mois = Value("mois",2,"",0)
        self.annee = Value("annee",3,"",0)
        self.temp = Value("temp",4,"",0)
        self.netTemp = Value("netTemp",5,"",0)
        self.humid = Value("humid",6,"",0)
        self.dateJour = Value("dateJour",7,"",0)
        self.presence = Value("presence",8,"",0)
        self.descW = Value("descW",9,"",0)
        self.notNow = Value("notNow",10,"",0)
        self.plotX = Value("plotX",11,"0",0)
        self.plotY = Value("plotY",12,"0",0)
        self.AllMyValues = [self.heure,self.jour,self.mois,self.annee,self.temp,self.netTemp,self.humid,self.dateJour,self.presence,self.descW,self.notNow,self.plotX,self.plotY]

    def getHeure(self):
        self.heure.val = time.strftime('%H:%M')
        self.heure.send = 0
    
    def getJour(self):
        self.jour.val = time.strftime("%A")
        self.jour.send = 0

    def getMois(self):
        self.mois.val = time.strftime("%B")
        self.mois.send = 0

    def getAnnee(self):
        self.annee.val = time.strftime("%Y")
        self.annee.send = 0

    def getTempHumid(self):
        self.temp.val,self.humid.val = getTempAndHumid()
        self.temp.send,self.humid.send = 0,0

    def getWeather(self):
        self.netTemp.val,self.descW.val = getWeatherFromWeb()
        self.netTemp.send,self.descW.send = 0,0

    def getDateDuJour(self):
        self.dateJour.val = time.strftime("%d")
        self.dateJour.send = 0

    def getAllValue(self):
        self.getHeure()
        self.getJour()
        self.getMois()
        self.getAnnee()
        self.getTempHumid()
        self.getWeather()
        self.getDateDuJour()

    def sendValuesToArduino(self,arduino):
        "function to send the values the values that has changed to the arduino"
        for value in self.AllMyValues:
            if(value.send == 0):
                self.sendValue(value,arduino)
                print(value)
                value.send = 1
                while(len(arduino.ser.read_all()) == 0):
                    pass
    
    def valuesToZ(self):
        for value in self.AllMyValues:
            value.send = 0
    
    def sendValue(self,value:Value,arduino:Arduino):
        "function to send a value to the arduino"
        # print(f"{value.id}={value.val}")
        arduino.ser.write(f"{value.id}={value.val}".encode())

    def __str__(self) -> str:
        res = ""
        for val in self.AllMyValues:
            res += str(val)
        return res




def getTempAndHumid():
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            return temp,humidity
        except:
                # print("trouble dht")
                return "NA", "NA"
        
def getWeatherFromWeb():
    try:
        response = requests.get(data.url)
        data = response.json()
        return str(int(float(data['main']['temp']) - 273.15)), data['weather'][0]['description'] 
    except:
        print("cannot find weather")
        return "NA", "NA"
        

class Imprimante3DIHM:
    def __init__(self):
        self.position_extrudeur = (0, 0, 0)
        self.nom_imprimante = "Imprimante 3D"
        self.reglages = ["Réglage 1", "Réglage 2", "Réglage 3"]
        

myValues = Values()
# memValues = Values()


# myValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,"1"),Value("descW",9,""),Value("notNow",10,""),Value("plotX",11,""),Value("plotY",12,"")])
# memValues = Values([Value("heure",0,""),Value("jour",1,""),Value("mois",2,""),Value("annee",3,""),Value("temp",4,""),Value("netTemp",5,""),Value("humid",6,""),Value("dateJour",7,""),Value("presence",8,"0"),Value("descW",9,""),Value("notNow",10,""),Value("plotX",11,""),Value("plotY",12,"")])
