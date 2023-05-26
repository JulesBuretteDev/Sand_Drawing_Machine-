from MyArduino import *
from MyValues import *
from flask import Flask, render_template, request
import subprocess
import threading
import RPi.GPIO as GPIO

app = Flask(__name__)


#setup

subprocess.call("sudo uhubctl -l 1-1 -p 3 -a off", shell=True)
subprocess.call("sudo uhubctl -l 1-1 -p 4 -a off", shell=True)

time.sleep(3)
myScreen = Arduino(9600,2)



@app.route('/')
def index():
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages,values =myValues.AllMyValues)

@app.route("/sendXY", methods=["POST"])
def submit_XY_form():
    myValues.plotX.val = request.form.get("myX")
    myValues.plotY.val = request.form.get("myY")
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages,values =myValues.AllMyValues)

@app.route('/toggle', methods=['POST'])
def toggle():
    myValues.presence.val = "1" if myValues.presence.val == "0" else "0"
    if myScreen.state == True:
        myScreen.turnArdOff()
        myScreen.state = False
        # sendAllValuesToArduino(myValues,memValues)
    if myScreen.state == False:
        myScreen.turnArdOn()
        myValues.valuesToZ()
        myScreen.state = True
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages,values =myValues.AllMyValues)



imprimante = Imprimante3DIHM()
GPIO.setup(4, GPIO.IN)  

def launchWeb():
    if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True)
    else:
        print('not in main script')

def launchScreen():
    # myArduino.connectArd(myArduino)
    while True:
        # print("here")
        time.sleep(1)
        if myScreen.state == True:
            myValues.getAllValue()
            myValues.sendValuesToArduino(myScreen)
        if myScreen.state == False:
            myValues.getAllValue()
        # print(myValues)


def launchBoth():
    # thread1 = threading.Thread(target=launchWeb)
    thread2 = threading.Thread(target=launchScreen)

    # Start the threads
    # thread1.start()
    thread2.start()
    launchWeb()
    # launchArduino()
    


launchBoth()