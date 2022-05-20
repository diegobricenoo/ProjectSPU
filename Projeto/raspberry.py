#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 57600, timeout=1)
    ser.reset_input_buffer()

    while True:
        # ser.write(b"Hello from Raspberry Pi!\n")
        if ser.in_waiting>0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)