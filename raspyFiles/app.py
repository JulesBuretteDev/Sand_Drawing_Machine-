from flask import Flask, render_template, jsonify
import threading

app = Flask(__name__)

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the real-time position of the extruder
@app.route('/position')
def get_position():
    # Replace the following lines with your own code to retrieve the real-time position
    x = 0.0
    y = 0.0

    # Return the position as a JSON response
    return jsonify(x=x, y=y)

def getValue():
    while 1: 
        x = input("x:")
        y = input("y:")

thread1 = threading.Thread(target=getValue)
thread1.start()

if __name__ == '__main__':
    app.run(debug=True)

