#!/bin/python3
from abstract_device import DeviceType
from abstract_device import _Device


class MockDevice(_Device):
    """
    Simulated Device class - subclassing Abstract device model
    """
    def __init__(self, target_id=None, target_obj=None):
        super(MockDevice, self).__init__()
        self.id = target_id
        self.type = DeviceType.DEVICE_MOCK
        self.name = None
        self.mock_obj = target_obj

    def open(self, baudrate=None):
        print("Opened Device")
        pass

    def close(self):
        print("Closed Device")

    def stdin(self):
        """
        Device's STDIN port ,i.e. serial write method
        from Host on device's serial port.
        """
        pass

    def stdout(self):
        """
        Device's STDOUT port ,i.e. serial read method
        from Host on device's serial port.
        """
        pass

    def stderr(self):
        pass
