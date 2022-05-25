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
    app.run(host='0.0.0.0', debug=True)  # , threaded=True,use_reloader=False


def while_function():
    while True:
        # ser.write(b"Hello from Raspberry Pi!\n")
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line, file=sys.stderr)


@app.route('/', methods=["POST", "GET"])
def hello():
    # state = app.config['STATE']
    # counter = state.get(counter)
    # print("HERE", file=sys.stderr)
    formValues={"minimumGreenTimeHorizontal":0,
    "minimumGreenTimeVertical":0,
    "lightThreshold":0,
    "yellowTime":0,
    "maximumGreenTimeHorizontal":0,
    "maximumGreenTimeVertical":0}
    if request.method == 'POST':
        formValues={"minimumGreenTimeHorizontal":request.form.get('minimumGreenTimeHorizontal'),
        "minimumGreenTimeVertical":request.form.get('minimumGreenTimeVertical'),
        "lightThreshold":request.form.get('lightThreshold'),
        "yellowTime":request.form.get('yellowTime'),
        "maximumGreenTimeHorizontal":request.form.get('maximumGreenTimeHorizontal'),
        "maximumGreenTimeVertical":request.form.get('maximumGreenTimeVertical')}

    return render_template('index.html', minimumGreenTimeHorizontal=formValues["minimumGreenTimeHorizontal"],
                               minimumGreenTimeVertical=formValues["minimumGreenTimeVertical"], 
                               lightThreshold=formValues["lightThreshold"], 
                               yellowTime=formValues["yellowTime"], 
                               maximumGreenTimeHorizontal=formValues["maximumGreenTimeHorizontal"], 
                               maximumGreenTimeVertical=formValues["maximumGreenTimeVertical"])


if __name__ == "__main__":
    # first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=while_function)
    # first_thread.start()
    second_thread.start()
    app.run(host='0.0.0.0', debug=True)

# @app.before_first_request
# def before_first_request_func():
#     print("This function will run once")
