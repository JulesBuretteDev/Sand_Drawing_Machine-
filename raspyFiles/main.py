from myClass import *
from arduinoFile import *
from flask import Flask, render_template, request
import subprocess
import threading

app = Flask(__name__)



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
    if myArduino.state == True:
        turnArdOff(myArduino)
        myArduino.state = False
        # sendAllValuesToArduino(myValues,memValues)
    if myArduino.state == False:
        turnArdOn(myArduino)
        myArduino.state = True
    return render_template('index.html', position=imprimante.position_extrudeur, nom_imprimante=imprimante.nom_imprimante, reglages=imprimante.reglages,values =myValues.AllMyValues)

imprimante = Imprimante3DIHM()

def launchWeb():
    if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True)
    else:
        print('not in main script')


def launchBoth():
    # thread1 = threading.Thread(target=launchWeb)
    # thread2 = threading.Thread(target=launchArduino)

    # Start the threads
    # thread1.start()
    # thread2.start()
    launchWeb()
    launchArduino()
    


launchBoth()
# launchArduino()
# launchWeb()