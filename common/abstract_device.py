#!/bin/python3
"""
Define an abstract Device interface - which can
be subclassed by actual devices, simulated devices
or device families.
"""
import abc
import copy
import collections

import serial
from serial.serialutil import SerialException

class DeviceType:
    DEVICE_RAW = "raw"
    DEVICE_MBED = "mbed"
    DEVICE_MOCK = "mock"

class _Device(metaclass=abc.ABCMeta):

    def __init__(self):
        self.id = None
        self.type = None
        self.name = None

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


class MbedDevice(_Device):
    def __init__(self, target_id=None, target_obj=None):
        super(MbedDevice, self).__init__()
        self.id = target_id
        self.type = DeviceType.DEVICE_MBED
        self.name = None
        self.mbed_obj = target_obj

    def open(self,baudrate=115200):
        serial_port = self.mbed_obj["serial_port"]
        if serial_port is None:
            raise ValueError

        print('Found Serial-port for Device-ID: {} {}'.format(serial_port, self.id))

        try:
            serial_obj = serial.serial_for_url(serial_port, timeout=0.1, do_not_open=True)
            serial_obj.baudrate = baudrate
            serial_obj.open()
            print("Opened Serial Port")

            self.serial = serial_obj  # add serial object attribute
        except SerialException as e:
            print('Could not open Port:{}'.format(serial_port))
            raise e

    def close(self):
        try:
            if not self.serial:
                raise ValueError
            elif self.serial.isOpen():
                print("Found Serial Object {}".format(self.serial))
                self.serial.close()
            else:
                pass
        except (AttributeError, SerialException) as e:
            raise e
        else:
            print("Closed Serial Port")


    def stdin(self):
        """
        Device's STDIN port ,i.e. serial write method from Host on device's serial port.
        """
        pass

    def stdout(self):
        """
        Device's STDOUT port ,i.e. serial read method from Host on device's serial port.
        """
        pass

    def stderr(self):
        pass


"""
Simulated Device class - subclassing Abstract device model
"""
class DeviceSimulated(_Device):
    def __init__(self):
        super().__init__()
        self.type = _Device.DEVICE_TYPE_SIMULATED

    """
    Standard I/O port routines for communicating with this device
    """
    def open_stdio(self):
        pass

    """
    reads from the device
    """
    def get_stdout(self):
        line = None
        return line
    """
    writes to the device
    """
    def set_stdin(self, line):
        pass

    def close_stdio(self):
        pass


class Device(_Device):
    def __init__(self):
        super().__init__()
        self.type = _Device.DEVICE_TYPE_PHYSICAL

"""
class DeviceScanner:
    COMM_TYPE_SERIAL = 0x1
    devices = dict()
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def add_device(self, device_id, dev_type=_Device.DEVICE_TYPE_SIMULATED, ports, comm_type=COMM_TYPE_SERIAL):
        if not device_id:
            raise ValueError('Empty Device ID not allowed')

        if device_id in devices:
            print("Already present Device-ID %s" % device_id)
            return devices[device_id]

        # Create a device Object structure to hold all information
        # related to this device

        devices[device_id]= Device

        device_obj = self.devices[device_id]
        device_obj["name"] = name
        device_obj["id"] = device_id
        device_obj["comm_info"] = dict()

        uart = dict()
        uart["serial_port"] = ports[1]
        uart["jtag"] = ports[0]
        uart["vid"] = None
        uart["pid"] = None
        uart['settings'] = None
        device_obj["comm_info"]["uart"] = uart

        session_info = dict()
        session_info["session_id"] = None
        session_info["user_id"] = None
        session_info["lease_time"] = None
        session_info["is_downloading"] = False

        device_obj["session_info"] = session_info

        device_obj["reboot_count"] = 0
        device_obj["plugged_in_time"] = 0
        device_obj["download_count"] = 0

        device_obj["heartbeat_enabled"] = False

        print(device_obj)

        if not device_obj:
            raise ValueError("can't create Device Object with ID %s" % device_id)

        # return device_obj

    def remove_device(self, dev_id):
        if not dev_id:
            raise ValueError('Empty Device ID not allowed')

        device = devices.pop(dev_id, None)
        if not device:
            print("Device(Id: {}) not found. Already removed?".format(dev_id))

    def get_dev_serials(self):
        for dev in self.devices.keys():
            ser_obj = self.devices[dev]['serial']

    s = DeviceSimulated()
    s.set_id("1234")
    print(s.get_type())
    print(s.get_id())

    t = Device()
    print(t.get_type())

    s2 = s.clone()
    print(s2.get_type())
    print(s2.get_id())
"""