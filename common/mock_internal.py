#!/bin/python3
from mock_service import *
import abstract_device

ADD_DEVICE = 1
ADD_DEVICE_AT_TIME = 2
REMOVE_DEVICE = 3
REMOVE_DEVICE_AT_TIME = 4

if __name__ == '__main__':
    mocks = create_mocks()
    print(mocks.find_devices())