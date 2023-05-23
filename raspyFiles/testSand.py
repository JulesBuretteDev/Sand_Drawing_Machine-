import fullcontrol as fc #imported with fullControlXYZ from GitHub
import serial
import time
import random as rd
import os

class MySandPrinter:
    minPointY = 0
    minPointX = 0
    maxPointX = 270
    maxPointY = 300

    def __init__(self,port) -> None:
        "initialisation de de l'imprimante, avec son port et son baudrate"
        self.bufferSize = 0
        self.com = serial.Serial(port,115200,timeout=1)
        time.sleep(2)
        while self.com.readline() != b'':
            print(self.com.readline())
        self.stepsList = []
    
    def addSteps(self,listOfSteps):
        if(len(listOfSteps) > 1):
            self.stepsList.extend(listOfSteps)
        else: 
            self.stepsList.append(listOfSteps)

    def randomValue(self):
        "retourne une valeur random dans les limites de l'imprimante"
        return fc.Point(x=rd.randint(self.minPointX,self.maxPointX),y=rd.randint(self.minPointY,self.maxPointY))

    def writePoint(self,val:fc.Point):
        "Envoie un point a l'imprimante sous le bon format"
        return f"G1 X{val.x} Y{val.y} F3000\r\n"

    def sendAValue(self,value):
        "Methode permettant d'envoyer un message a l'imprimante"
        self.com.flush()
        self.com.write(f"{value}\r\n".encode())

    def sendCheck(self):
        "Methode permettant de bloquer le script tant que la valeur n'a pas été accepté"
        while self.com.readline() != b'ok\r\n':
            print("waiting for buffer")
            time.sleep(1)
        time.sleep(0.5)
        print(self.com.readline())
        self.com.flush()
        
        
        

    def manualPrinting(self):
        "Permet de gérer les Gcodes envoyer a la main"
        data = input("Data to send : ")
        if(data == "quit"):
            self.com.close()
            quit()
        self.sendAValue(data)
        self.sendCheck()

    def autoPrinting(self):
        "Envoie des Gcode a la suite de maniere aleatoire"
        self.com.flush()
        self.sendAValue(self.writePoint(self.randomValue()))
        self.sendCheck()

    def trySending(self):
        msg = self.stepsList[0]
        self.com.flush()
        self.sendAValue(msg)
        if b"ok" in self.com.readline():
            self.stepsList.pop(0)
            return True
        return False


    def playPattern(self,file):
        self.stepsList = []
        self.addSteps(Sandify(file).steps)
        while len(self.stepsList) != 0:
            while(self.trySending() == False):
                pass
            


class Sandify:
    def __init__(self,filename : str) -> None:
        self.filename = filename
        self.steps = []
        with open(filename, 'r') as file:
            for line in file:
                self.steps.append(line)
            file.close()
        



# Initialisation 
dir_path = os.path.dirname(os.path.realpath(__file__))
sandPrinter = MySandPrinter("COM3")




while 1:
    wtd = input("what to do? ")
    if "G" in wtd :
        sandPrinter.sendAValue(wtd)
        sandPrinter.sendCheck()
    else: 
        try: 
            sandPrinter.playPattern(os.path.join(dir_path,"SandifyFiles",f"{wtd}.gcode"))
        except:
            print("this file as not been found")
    
    # sandPrinter.autoPrinting()
    
    
