#!/bin/python3
from multiprocessing import Process, Queue
import time
import sys
import queue as std_queue
import threading


from mbed_os_tools.detect.main import create
from mbed_os_tools.detect.main import mbed_os_support
from mbed_os_tools.detect.main import mbed_lstools_os_info
from abstract_device import *
from abstract_device import DeviceType
from mbed_device import MbedDevice
from mock_device import MockDevice

from mock_service import *

COMMON_LIBS_PATH = "../common/"
sys.path.append(COMMON_LIBS_PATH)


MBED_OS_TOOLS_PATH = "../third-party/mbed-os-tools"
# COMMON_LIBS_PATH = "../common"
sys.path.append(MBED_OS_TOOLS_PATH)
# sys.path.append(COMMON_LIBS_PATH)


def core_scanner(obj):
    cached = obj.get_all_devices()
    tmp = dict()

    # Handle Mock device list
    mocks = obj.mocks
    if obj.scan_services[DeviceType.DEVICE_MOCK]:
        mock_devs_list = mocks.find_devices()
        # print(mock_devs_list)
        for mocked in mock_devs_list:
            tmp[mocked["mock_devid"]] = True
            if mocked["mock_devid"] in cached:
                pass
            else:
                obj.add_device(mocked["mock_devid"], DeviceType.DEVICE_MOCK, mocked)

        mock_cached_devs = obj.get_all_devices_by_type(DeviceType.DEVICE_MOCK)
        for c in mock_cached_devs:
            if c not in tmp:
                obj.remove_device(c)

    # Handle Mbed Devices
    mbeds = obj.mbeds
    mbed_devs_list = mbeds.find_candidates()
    # print(mbed_devs_list)
    for mbed in mbed_devs_list:
        tmp[mbed["target_id_usb_id"]] = True
        if mbed["target_id_usb_id"] in cached:
            # print("dev: {} was in cached-list".format(mbed["target_id_usb_id"]))
            # device is already present in cached-list - figure out a way to quickly
            # check that objects are same(i.e. same dev_id, same mount-point etc.)
            pass
        else:
            # A new device found by mbedls...add it to the cached list
            obj.add_device(mbed["target_id_usb_id"], DeviceType.DEVICE_MBED, mbed)

    mbed_cached_devs = obj.get_all_devices_by_type(DeviceType.DEVICE_MBED)
    # print(mbed_cached_devs)
    for c in mbed_cached_devs:
        if c not in tmp:
            obj.remove_device(c)

def parse_and_handle_command(loop, cmd):
    if cmd == "stop_scan":
        return

def scanner_main_loop(obj):
    while True:
        """
        Main Event loop.
        i.  Check all the changes happened in respective service - if there is a change - report it.
        ii. Check if there is a command to be processed - if yes - handle the command.
        iii. If required - prepare the response and send it back as event
        """
        try:
            command = obj.scanner_queue.get_nowait()
        except std_queue.Empty as e:
            pass
        else:
            print(command)
            # If we receive a 'Halt' command - scanner is about to terminate
            # clean things up and get out of the loop
            if command == "stop_scan":
                break;
            # else - parse and handle commands appropriately
            parse_and_handle_command(obj, command)

        core_scanner(obj)

        time.sleep(0.5)

    print("Scanner main process is stopping now...")


class DeviceScanner:

    def __init__(self, device_queue=None, mock=False, raw=False):
        self.scan_services = dict()
        self.cached = dict()

        self.scan_services[DeviceType.DEVICE_RAW] = raw
        self.scan_services[DeviceType.DEVICE_MBED] = True
        self.scan_services[DeviceType.DEVICE_MOCK] = mock
        self.scanner_queue = None
        self.device_queue = device_queue
        self.mbeds = create()
        self.mocks = create_mocks()


    def get_all_devices(self):
        return self.cached.keys()

    def get_all_devices_by_type(self, dev_type):
        devs = dict()
        for d in self.cached:
            if self.cached[d].type == dev_type:
                devs[d] = self.cached[d]
        return devs

    def start(self):
        self.scanner_queue = Queue()
        self.scanner = threading.Thread(target=scanner_main_loop, args=(self,))
        # A container for mbed-os devices
        self.mbedls = None
        # service for raw/vid/pid/hw_id devices
        if self.scan_services[DeviceType.DEVICE_RAW]:
            self.rawlsusb = None
        if self.scan_services[DeviceType.DEVICE_MOCK]:
            self.mockls = None
        self.scanner.daemon = True
        self.scanner.start()

    def get_device(self, dev_id):
        if dev_id not in self.cached:
            return None
        return self.cached[dev_id]

    def add_device(self, dev_id, dev_type=None, _obj=None):
        if not dev_id or not dev_type:
            raise ValueError

        if dev_type == DeviceType.DEVICE_MBED:
            self.cached[dev_id] = MbedDevice(dev_id, _obj)
        elif dev_type == DeviceType.DEVICE_RAW or dev_type ==DeviceType.DEVICE_MOCK:
            raise NotImplementedError

        # Generate a notification/event that a new Device has been added
        if not self.device_queue:
            self.device_queue.put(["Device Added", dev_id])
        pass

    def remove_device(self, dev_id):
        if not dev_id:
            return

        self.cached.pop(dev_id)
        if not self.device_queue:
            self.device_queue.put(["Device Removed", dev_id])


    def stop(self):
        self.scanner_queue.put("stop_scan");
        self.scanner.join()
        self.scanner.terminate()

    def invoke_command(self, cmd):
        if self.scanner.is_alive():
            self.scanner_queue.put(["cmd_received", cmd])


def test_device_open_close(scanner, dev_id):
    if not scanner or not dev_id:
        return
    device = scanner.get_device(dev_id)
    cached = scanner.get_all_devices()

    if not device:
        print("test: Device not found {}".format(dev_id))
        return
    try:
        device.open()
        time.sleep(2.0)
        device.close()
    except (ValueError, SerialException, AttributeError) as e:
        print(e)
    except OSError as d:
        print(d)

if __name__ == '__main__':

    dev_queue = Queue()

    s = DeviceScanner(dev_queue, mock=True)
    s.start()
    count = 0
    while True:
        time.sleep(0.5)
        try:
            queue_elem = dev_queue.get_nowait()
        except std_queue.Empty as e:
            # print("queue was empty - ignore it")
            pass
        else:
            print(queue_elem)
        count += 1
        s.invoke_command("foo")
        dev_id = '19060000c8121e0600c8121e00000000000000002e127069'
        # test_device_open_close(s, dev_id)
        if count > 100000:
            break
    print("main after time.sleep()")
    s.stop()
