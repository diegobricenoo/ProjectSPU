# from flask import Flask


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

import serial
from flask import Flask, render_template
import sys
import threading

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# @app.before_first_request
# def before_first_request_func():
#     while True:
#         # ser.write(b"Hello from Raspberry Pi!\n")
#         if ser.in_waiting>0:
#             line = ser.readline().decode('latin-1').rstrip()
#             print(line, file=sys.stderr)


def run_app():
    app.run(host='0.0.0.0',debug=False, threaded=True)

def while_function():
    while True:
        # ser.write(b"Hello from Raspberry Pi!\n")
        if ser.in_waiting>0:
            line = ser.readline().decode('latin-1').decode('utf-8').rstrip()
            print(line, file=sys.stderr)

if __name__ == "__main__":
    first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=while_function)
    first_thread.start()
    second_thread.start()
    

@app.route('/')
def hello():
    # state = app.config['STATE']
    # counter = state.get(counter)
    # print("HERE", file=sys.stderr)
    return render_template('index.html')

# @app.before_first_request
# def before_first_request_func():
#     print("This function will run once")




# def webserver(state):
#     app.config['STATE'] = state
#     # If running on, say, a Raspberry Pi, use 0.0.0.0 so that
#     # you can connect to the web server from your intranet.
#     app.run(host='0.0.0.0', use_reloader=False, debug=True)

# def main():
#     state = SharedState()
#     web_thread = threading.Thread(target=webserver, args=(state,))
#     web_thread.start()

#     state.set('counter', 0)
#     while True:
#         # Do whatever you want in the foreground thread
#         state.set('counter', state.get('counter') + 1)
#         print(state.get('counter'), file=sys.stderr)

# class SharedState():
#     def __init__(self):
#         self.lock = threading.Lock()
#         self.state = dict()

#     def get(self, key):
#         with self.lock:
#             return self.state.get(key)

#     def set(self, key, value):
#         with self.lock:
#             self.state[key] = value