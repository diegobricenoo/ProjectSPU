# from flask import Flask


# app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Hello, World!'

import serial
from flask import Flask, render_template, request
import sys
import threading

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
ser.reset_input_buffer()

# @app.before_first_request
# def before_first_request_func():
#     while True:
#         # ser.write(b"Hello from Raspberry Pi!\n")
#         if ser.in_waiting>0:
#             line = ser.readline().decode('latin-1').rstrip()
#             print(line, file=sys.stderr)


def run_app():
    app.run(host='0.0.0.0',debug=True)#, threaded=True,use_reloader=False

def while_function():
    while True:
        # ser.write(b"Hello from Raspberry Pi!\n")
        if ser.in_waiting>0:
            line = ser.readline().decode('latin-1').rstrip()
            print(line, file=sys.stderr)

if __name__ == "__main__":
    # first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=while_function)
    # first_thread.start()
    # second_thread.start()
    app.run(host='0.0.0.0',debug=True)
    

@app.route('/', methods=['POST', 'GET'])
def hello():
    # state = app.config['STATE']
    # counter = state.get(counter)
    # print("HERE", file=sys.stderr)
    if request.method == 'POST':
        var=request.form["test"]
        print(var)
        return "success"

    return render_template('index.html')

# @app.before_first_request
# def before_first_request_func():
#     print("This function will run once")

