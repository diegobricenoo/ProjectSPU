import serial
from flask import Flask, render_template, request
import sys
import threading

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
# ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
# ser.reset_input_buffer()

carsWaitingS1="There is NO cars waiting at S1"
carsWaitingS2="There is cars waiting at S2"
carsWaitingS3="There is cars waiting at S3"


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
    formValues = {"minimumGreenTimeHorizontal": 0,
                  "minimumGreenTimeVertical": 0,
                  "lightThreshold": 0,
                  "yellowTime": 0,
                  "maximumGreenTimeHorizontal": 0,
                  "maximumGreenTimeVertical": 0}

    if request.method == 'POST':
        formValues = {"minimumGreenTimeHorizontal": request.form.get('minimumGreenTimeHorizontal'),
                      "minimumGreenTimeVertical": request.form.get('minimumGreenTimeVertical'),
                      "lightThreshold": request.form.get('lightThreshold'),
                      "yellowTime": request.form.get('yellowTime'),
                      "maximumGreenTimeHorizontal": request.form.get('maximumGreenTimeHorizontal'),
                      "maximumGreenTimeVertical": request.form.get('maximumGreenTimeVertical')}

    return render_template('index.html', minimumGreenTimeHorizontal=formValues["minimumGreenTimeHorizontal"],
                           minimumGreenTimeVertical=formValues["minimumGreenTimeVertical"],
                           lightThreshold=formValues["lightThreshold"],
                           yellowTime=formValues["yellowTime"],
                           maximumGreenTimeHorizontal=formValues["maximumGreenTimeHorizontal"],
                           maximumGreenTimeVertical=formValues["maximumGreenTimeVertical"],
                           carsWaitingS1=carsWaitingS1,carsWaitingS2=carsWaitingS2,carsWaitingS3=carsWaitingS3)


if __name__ == "__main__":
    # first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=while_function)
    # first_thread.start()
    # second_thread.start()
    app.run(host='0.0.0.0', debug=True)
