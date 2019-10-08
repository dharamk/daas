#!/bin/python3

class MockDeviceService:
    def __init__(self, actions=None):
        self.devices = None
        self.actions = None
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def find_devices(self):
        MOCKDEVICES_ACTIONLIST = [
        {"name": "mock_device_1", "mock_devid": "MOCK_DEVID_0001"},
        {"name": "mock_device_2", "mock_devid": "MOCK_DEVID_0002"},
        {"name": "mock_device_3", "mock_devid": "MOCK_DEVID_0003"},
        {"name": "mock_device_4", "mock_devid": "MOCK_DEVID_0004"},
        {"name": "mock_device_5", "mock_devid": "MOCK_DEVID_0005"},
        {"name": "mock_device_6", "mock_devid": "MOCK_DEVID_0006"},
        ]
        return MOCKDEVICES_ACTIONLIST

    def find_device_by_id(self, devid):
        pass

def create_mocks():
    return mockservice

mockservice = MockDeviceService()

