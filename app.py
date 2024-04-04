from flask import Flask, render_template, request
from tinydb import TinyDB, Query
import pydobot

# Code for simulating the robot connection
# class SimulatedRobot:
#     def __init__(self):
#         self.current_pose = (0, 0, 0, 0)

#     def speed(self, x, y):
#         pass

#     def pose(self):
#         return self.current_pose

#     def move_to(self, x, y, z, r):
#         self.current_pose = (x, y, z, r)

#     def close(self):
#         pass

#robot = SimulatedRobot()

robot = pydobot.Dobot(port='COM7', verbose=False)

robot.speed(50, 50)

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
    
    robot.move_to(float(x), float(y), float(z), float(r), wait=True)
    
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    db.insert({'x': 0, 'y': 0, 'z': 0, 'r': 0})
    robot.move_to(0, 0, 0, 0, wait=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

robot.close()