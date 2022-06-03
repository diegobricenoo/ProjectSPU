import serial
from flask import Flask, render_template, request
import sys
import threading

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)
ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
ser.reset_input_buffer()

carsWaitingS1 = "There is NO cars waiting at S1"
carsWaitingS2 = "There is NO cars waiting at S2"
carsWaitingS3 = "There is NO cars waiting at S3"

formValues = {"minimumGreenTimeHorizontal": 5,
              "minimumGreenTimeVertical": 5,
              "lightThreshold": 50,
              "yellowTime": 5,
              "maximumGreenTimeHorizontal": 10,
              "maximumGreenTimeVertical": 10}

previousFormValues=formValues


def run_app():
    app.run(host='0.0.0.0', debug=True)  # , threaded=True,use_reloader=False


def while_function():
    # ser.write(b"Hello from Raspberry Pi!\n")
    global formValues, carsWaitingS1, carsWaitingS2, carsWaitingS3
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line, file=sys.stderr)
            if "-" in line:
                # print("HERE")
                lineSplit = line.split("-")
                print(lineSplit)
                try:
                    carsWaitingS1 = "There is cars waiting at S1" if lineSplit[
                        0] == '1' else "There is NO cars waiting at S1"
                    carsWaitingS2 = "There is cars waiting at S2" if lineSplit[
                        1] == '1' else "There is NO cars waiting at S2"
                    carsWaitingS3 = "There is cars waiting at S3" if lineSplit[
                        2] == '1' else "There is NO cars waiting at S3"
                    # print(carsWaitingS1)
                    # print(carsWaitingS2)
                    # print(carsWaitingS3)
                except:
                    print("erro")


@app.route('/', methods=["POST", "GET"])
def hello():
    global previousFormValues,formValues, carsWaitingS1, carsWaitingS2, carsWaitingS3
    # print(formValues)
    if request.method == 'POST':
        formValues = {"minimumGreenTimeHorizontal": formValues["minimumGreenTimeHorizontal"] if request.form.get('minimumGreenTimeHorizontal') == "0" else request.form.get('minimumGreenTimeHorizontal'),
                      "minimumGreenTimeVertical": formValues["minimumGreenTimeVertical"] if request.form.get('minimumGreenTimeVertical') == "0" else request.form.get('minimumGreenTimeVertical'),
                      "lightThreshold": formValues["lightThreshold"] if request.form.get('lightThreshold') == "0" else request.form.get('lightThreshold'),
                      "yellowTime": formValues["yellowTime"] if request.form.get('yellowTime') == "0" else request.form.get('yellowTime'),
                      "maximumGreenTimeHorizontal": formValues["maximumGreenTimeHorizontal"] if request.form.get('maximumGreenTimeHorizontal') == "0" else request.form.get('maximumGreenTimeHorizontal'),
                      "maximumGreenTimeVertical": formValues["maximumGreenTimeVertical"] if request.form.get('maximumGreenTimeVertical') == "0" else request.form.get('maximumGreenTimeVertical')}
        # print(formValues)
        if previousFormValues!=formValues:
            ser.write("{}-{}-{}-{}-{}-{}".format(formValues["minimumGreenTimeVertical"], formValues["minimumGreenTimeHorizontal"], formValues["lightThreshold"],
                    formValues["yellowTime"], formValues["maximumGreenTimeVertical"], formValues["maximumGreenTimeHorizontal"]).encode("utf-8"))
            previousFormValues=formValues

    return render_template('index.html', minimumGreenTimeHorizontal=formValues["minimumGreenTimeHorizontal"],
                           minimumGreenTimeVertical=formValues["minimumGreenTimeVertical"],
                           lightThreshold=formValues["lightThreshold"],
                           yellowTime=formValues["yellowTime"],
                           maximumGreenTimeHorizontal=formValues["maximumGreenTimeHorizontal"],
                           maximumGreenTimeVertical=formValues["maximumGreenTimeVertical"],
                           carsWaitingS1=carsWaitingS1, carsWaitingS2=carsWaitingS2, carsWaitingS3=carsWaitingS3)


if __name__ == "__main__":
    # first_thread = threading.Thread(target=run_app)
    second_thread = threading.Thread(target=while_function)
    # first_thread.start()
    second_thread.start()
    app.run(host='0.0.0.0', debug=True, port=8000)
