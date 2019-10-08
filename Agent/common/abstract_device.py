#!/bin/python3
"""
Define an abstract Device interface - which can
be subclassed by actual devices, simulated devices
or device families.
"""
import abc


class DeviceType:
    DEVICE_RAW = "raw"
    DEVICE_MBED = "mbed"
    DEVICE_MOCK = "mock"

    def __init__(self):
        pass

class DeviceStatus:
    DEVICE_AVAILABLE = "available"
    DEVICE_BUSY = "busy"
    DEVICE_IMAGE = "flashing"

class _Device(metaclass=abc.ABCMeta):

    def __init__(self):
        self.id = None
        self.type = None
        self.name = None
        self.status = DeviceStatus.DEVICE_AVAILABLE

    def get_type(self):
        return self.type

    def set_type(self, t):
        self.type = t

    def get_id(self):
        return self.id

    def set_id(self, device_id):
        self.id = device_id

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def set_status(self, new_status):
        self.status = new_status

    def get_status(self):
        return self.status

    def clone(self):
        return copy.copy(self)

    def open(self):
        pass

    def close(self):
        pass

    def stdin(self):
        """
        Device's STDIN port ,i.e.
        serial write method from Host on device's serial port.
        """
        pass

    def stdout(self):
        """
        Device's STDOUT port ,i.e.
        serial read method from Host on device's serial port.
        """
        pass

    def stderr(self):
        pass

