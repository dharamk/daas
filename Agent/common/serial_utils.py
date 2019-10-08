#!/bin/python3
import serial

def do_serial_read(serial):
    ser_lines = serial.readlines()
    # print("Serial lines: {}".format(ser_lines))
    non_empty_lines = list(filter(lambda line : line and line != b'', ser_lines))
    return non_empty_lines