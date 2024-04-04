from flask import Flask, render_template, request
from tinydb import TinyDB, Query
import pydobot

robot = pydobot.Dobot(port='COM3', verbose=False)

robot.speed(30, 30)

app = Flask(__name__)
db = TinyDB('logs.json')

@app.route('/')
def index():
    current_pose = robot.pose()
    return render_template('index.html')

@app.route('/logs')
def logs():
    logs = db.all()
    return render_template('logs.html', logs=logs)

@app.route('/command', methods=['POST'])
def send_command():
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    
    db.insert({'x': x, 'y': y, 'z': z, 'r': r})
    
    robot.move_to(float(x), float(y), float(z), float(r))
    
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    robot.move_to(0, 0, 0, 0)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

robot.close()