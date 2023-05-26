
import time
import adafruit_dht
import board
import requests



api_key = "5317595bb8e0c71dd94fe21a6512e8f4"
city_name = "Paris"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"


sensor = adafruit_dht.DHT11(board.D23)



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
        if self.heure.val != time.strftime('%H:%M'):
            self.heure.val = time.strftime('%H:%M')
            self.heure.send = 0
    
    def getJour(self):
        if self.jour.val != time.strftime("%A"):
            self.jour.val = time.strftime("%A")
            self.jour.send = 0

    def getMois(self):
        if self.mois.val != time.strftime("%B"):
            self.mois.val = time.strftime("%B")
            self.mois.send = 0

    def getAnnee(self):
        if self.annee.val != time.strftime("%Y"):
            self.annee.val = time.strftime("%Y")
            self.annee.send = 0

    def getTempHumid(self):
        if self.temp.val != getTempAndHumid()[0]:
            self.temp.val,self.humid.val = getTempAndHumid()
            self.temp.send,self.humid.send = 0,0

    def getWeather(self):
        if self.netTemp.val != getWeatherFromWeb()[0]:
            self.netTemp.val,self.descW.val = getWeatherFromWeb()
            self.netTemp.send,self.descW.send = 0,0

    def getDateDuJour(self):
        if self.dateJour.val != time.strftime("%d"):
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
                    time.sleep(1)
    
    def valuesToZ(self):
        for value in self.AllMyValues:
            value.send = 0
    
    def sendValue(self,value:Value,arduino):
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
        response = requests.get(url)
        data = response.json()
        return str(int(float(data['main']['temp']) - 273.15)), data['weather'][0]['description'] 
    except:
        print(f"cannot find weather ")
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
