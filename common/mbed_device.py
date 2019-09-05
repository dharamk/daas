#!/bin/python3
from abstract_device import DeviceType
from abstract_device import _Device
import serial
from serial.serialutil import SerialException

from serial_utils import *
# from mbed_host_tests.host_tests_toolbox import flash_dev


def do_serial_read(serial):
    ser_lines = serial.readlines()
    # print("Serial lines: {}".format(ser_lines))
    non_empty_lines = list(filter(lambda line : line and line != b'', ser_lines))
    return non_empty_lines


class MbedDevice(_Device):
    def __init__(self, target_id=None, target_obj=None):
        super(MbedDevice, self).__init__()
        self.id = target_id
        self.type = DeviceType.DEVICE_MBED
        self.name = None
        self.mbed_obj = target_obj

    def open(self, baudrate=115200):
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
        if not self.serial:
            raise ValueError
        if not self.serial.is_open:
            try:
                self.serial.open()
            except SerialException as e:
                print('Could not open Port:{}'.format(self.serial.port))
                raise e

        # print("Found Serial Object {}".format(self.serial))
        try:
            read_lines = do_serial_read(self.serial)
            # print(read_lines)
            return read_lines

        except SerialException as e:
            raise e

        # serial_port = uart = dev_obj.get('comm_info').get('uart')
        # if uart is None:
        #     _lines.error_set = True
        #     _lines.error_message = 'UART COMM NOT FOUND'
        #     return _lines

        # serial_obj = uart['serial_obj']
        # if serial_obj is None:
        #     _lines.error_set = True
        #     _lines.error_message = 'UART SERIAL NOT FOUND'
        #     return _lines
        # print('--> Serial Object found')

        # if serial_obj.isOpen() is False:
        #     print("Found Serial-Port[{}] in CLOSED state...Opening it".format(serial_obj.name))
        #     try:
        #         serial_obj.open()
        #     except SerialException as e:
        #         print("Could not Open Serial-Port {}".format(e))
        #         _lines.error_set = True
        #         _lines.error_message = 'SERIAL OPEN ERROR'
        #         return _lines
        pass

    def stderr(self):
        pass

    def get_mount_dir(self):
        if self.mbed_obj:
            # print(self.mbed_obj)
            return self.mbed_obj['mount_point']
        return None

    def download_image(self, binary_image_path):
        try:
            from mbed_host_tests.host_tests_toolbox import flash_dev
        except (IOError, ImportError, OSError) as e:
            print(e)
            raise e

        if not binary_image_path:
            raise ValueError

        mount_dir = self.get_mount_dir()
        if not mount_dir:
            print("xxxx Downloading - No Mount path found xxxx")
            raise False

        # it turns out - flashing an image in mbed-os world is merely
        # copying and sync the binary image in the mount directory -
        # anyway, all that is well-abstracted under flash_dev() method
        if not flash_dev(mount_dir, binary_image_path, program_cycle_s=4):
            print("xxxx Downloading image failed xxxx")
            return False

        self.reset()
        return True

    def reset(self):
        if self.serial:
            try:
                self.serial.sendBreak()
            except:
                try:
                    self.serial.setBreak(False) # For Linux the following setBreak() is needed to release the reset signal on the target mcu.
                except:
                    return False
            return True

