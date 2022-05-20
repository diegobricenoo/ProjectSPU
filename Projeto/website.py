# from flask import Flask


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

import serial
from flask import Flask

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

if __name__=='__main__':
    app.run(host='0.0.0.0')


@app.route('/')
def hello():
    while True:
        # ser.write(b"Hello from Raspberry Pi!\n")
        if ser.in_waiting>0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
    return 'Hello, World!'