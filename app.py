from flask import Flask, render_template, request
from pydobot import Dobot
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('logs.json')
robot = None

# Rota para controlar o robô
@app.route('/', methods=['GET', 'POST'])
def control():
    logs = db.all()
    if request.method == 'POST':
        command = request.form['command']
        x = request.form['x']
        y = request.form['y']
        z = request.form['z']
        if robot is not None:
            robot.send(command)
            db.insert({'command': command, 'x': x, 'y': y, 'z': z})
    return render_template('control.html', logs=logs)

class SimulatedDobot:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True
        print('Conectado ao Dobot (simulado)')

    def disconnect(self):
        self.connected = False
        print('Desconectado do Dobot (simulado)')

    def send(self, command):
        if self.connected:
            print(f'Enviando comando para o Dobot (simulado): {command}')
        else:
            print('Erro: Dobot não está conectado (simulado)')

# Simulando a conexão com o Dobot
def connect_robot():
    global robot
    print('Conectando ao Dobot (simulado)...')
    robot = SimulatedDobot()
    print('Conectado ao Dobot (simulado)')
    robot.connect()

# Simulando a desconexão com o Dobot
def disconnect_robot():
    global robot
    if robot is not None:
        robot.disconnect()
        print('Desconectado do Dobot (simulado)')
        robot = None

# Função para conectar o robô
#def connect_robot():
    #global robot
    #print('Conectando ao Dobot...')
    #robot = Dobot(port='COM7')
    #print('Conectado ao Dobot')
    #robot.connect()

# Função para desconectar o robô
#def disconnect_robot():
    #global robot
    #if robot is not None:
        #robot.disconnect()
        #print('Desconectado do Dobot')
        #robot = None

# Inicializa o servidor
if __name__ == '__main__':
    connect_robot()
    app.run()
    disconnect_robot()