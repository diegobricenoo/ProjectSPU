# from flask import Flask


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

import imp
import serial
from flask import Flask, render_template
import sys
import threading

app = Flask(__name__)
# ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
# ser.reset_input_buffer()

# if __name__=='__main__':
#     while True:
#         # ser.write(b"Hello from Raspberry Pi!\n")
#         if ser.in_waiting>0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line, file=sys.stderr)




def webserver(state):
    app.config['STATE'] = state
    # If running on, say, a Raspberry Pi, use 0.0.0.0 so that
    # you can connect to the web server from your intranet.
    app.run(host='0.0.0.0', use_reloader=False, debug=True)

def main():
    state = SharedState()
    web_thread = threading.Thread(target=webserver, args=(state,))
    web_thread.start()

    state.set('counter', 0)
    while True:
        # Do whatever you want in the foreground thread
        state.set('counter', state.get('counter') + 1)
        print(state.get('counter'), file=sys.stderr)

class SharedState():
    def __init__(self):
        self.lock = threading.Lock()
        self.state = dict()

    def get(self, key):
        with self.lock:
            return self.state.get(key)

    def set(self, key, value):
        with self.lock:
            self.state[key] = value
            
@app.route('/')
def hello():
    # print("HERE", file=sys.stderr)
    return render_template('index.html')