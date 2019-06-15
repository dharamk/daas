import concurrent.futures as futures
import grpc
import framework_pb2_grpc
import framework_pb2

import serial
from serial.serialutil import SerialException

class DeviceImageDownloader:
    def __init__(self):
        pass


def handle_serial_connect(server, dev_id):

    response = framework_pb2.SerialEvent()
    scanner = server.get_scanner()
    device = scanner.get_device()

    response.device.device_id = dev_id

    if not device:
        response.event = framework_pb2.SerialEvent.SERIAL_NOT_AVAILABLE
        return response
    try:
        device.open()
    except (ValueError, SerialException):
        response.event = framework_pb2.SerialEvent.SERIAL_NOT_AVAILABLE
    else:
        response.event = framework_pb2.SerialEvent.SERIAL_CONNECTED
    finally:
        print("Sending Invoke Response ---> Event: {}".format(_response.event))
        return response


def handle_serial_disconnect(server, dev_id):

    response = framework_pb2.SerialEvent()
    scanner = server.get_scanner()
    device = scanner.get_device()

    response.device.device_id = dev_id
    if not device:
        response.event = framework_pb2.SerialEvent.SERIAL_NOT_AVAILABLE
        return response

    try:
        device.close()
    except (ValueError, SerialException, AttributeError):
        response.event = framework_pb2.SerialEvent.SERIAL_NOT_AVAILABLE
    else:
        response.event = framework_pb2.SerialEvent.SERIAL_DISCONNECTED
    finally:
        print("Sending Invoke Response ---> Event: {}".format(_response.event))
        return response

def handle_serial_reset(server, dev):
    _response = framework_pb2.SerialEvent()
    _response.device.device_id = dev
    _response.event = framework_pb2.SerialEvent.SERIAL_RESET_DONE

    return _response


def handle_device_reset(server, dev):

    _response = framework_pb2.SerialEvent()
    _response.device.device_id = dev
    _response.event = framework_pb2.SerialEvent.SERIAL_RESET_DONE
    return _response

class RemoteSerialCommandHandler:

    def __init__(self):
        self.handlers = dict()
        self.handlers[framework_pb2.SerialCmd.SERIAL_CONNECT] = handle_serial_connect
        self.handlers[framework_pb2.SerialCmd.SERIAL_DISCONNECT] = handle_serial_disconnect
        self.handlers[framework_pb2.SerialCmd.SERIAL_RESET] = handle_serial_reset
        self.handlers[framework_pb2.SerialCmd.SERIAL_DEVICE_RESET] = handle_device_reset

    def get_handler(self, cmd):
        return self.handlers.get(cmd)

class RemoteSerialServicer(framework_pb2_grpc.RemoteSerialServicer):
    def __init__(self, server):
        self.serial_cmd_handler = RemoteSerialCommandHandler()
        self.server = server

    def Invoke(self, request_iterator, context):

        for serial_cmd in request_iterator:
            print('Got Request {}'.format(serial_cmd))
            command = serial_cmd.command
            dev = serial_cmd.device.device_id
            print("Got Invoke Command --> {} {}".format(command, dev))
            func = self.serial_cmd_handler.get_handler(command)
            if func is None:
                raise StopIteration
            else:
                _response = func(self.server, dev)

            print('yielded response {} {}'.format(_response.event, _response.device.device_id))
            yield _response

    def WriteLine(self, request, context):
        pass

    def readLines(self, request, context):

        dev = request.device_id
        print('Got ReadLInes Command -->{}'.format(dev))
        dev_obj = self.server.get_device(dev)

        _lines = framework_pb2.SerialRead(error_set=False,device_id=request.device_id)
        if dev_obj is None:
            # Handle invalid 'readline' - figure out a way of saying
            # DEVICE NOT FOUND
            _lines.error_set = True
            _lines.error_message = 'DEVICE NOT FOUND'
            return _lines

        uart = dev_obj.get('comm_info').get('uart')
        if uart is None:
            _lines.error_set = True
            _lines.error_message = 'UART COMM NOT FOUND'
            return _lines

        serial_obj = uart['serial_obj']
        if serial_obj is None:
            _lines.error_set = True
            _lines.error_message = 'UART SERIAL NOT FOUND'
            return _lines
        print('--> Serial Object found')

        if serial_obj.isOpen() is False:
            print("Found Serial-Port[{}] in CLOSED state...Opening it".format(serial_obj.name))
            try:
                serial_obj.open()
            except SerialException as e:
                print("Could not Open Serial-Port {}".format(e))
                _lines.error_set = True
                _lines.error_message = 'SERIAL OPEN ERROR'
                return _lines
        try:
            read_lines = do_serial_read(serial_obj)
            print("Reading lines:{}".format(read_lines))
            _lines.lines.extend(read_lines)

            _lines.hostagent_id = self.server.host_id
        except SerialException as e:
            print("Could not Open Serial-Port {}".format(e))
            _lines.error_set = True
            _lines.error_message = 'SERIAL READ ERROR'

        return _lines

class DeviceAgentServicer(framework_pb2_grpc.DeviceAgentServicer):

    def __init__(self, server):
        self.server = server

    def sync(self, request, context):
        print('Got Sync Request for: {}.'.format(request.device_id))

        response = framework_pb2.SyncResponse()
        response.hostagent_id = self.server.get_host_id()

        if request.device_id[0] == 'all':
            devs = self.server.get_device_list()
            for dev in devs:
                dev_info = create_DeviceInfo_body(response, dev, True)
                #print(dev_info)
        else:
            for dev in request.device_id:
                if self.server.has_device(dev):
                    create_DeviceInfo_body(response, dev, True)
                else:
                    create_DeviceInfo_body(response, dev, False)
        print('-----Serving SYNC response back to Client --------')
        print(response)
        return response

class LocalDeviceScanner:
    COMM_TYPE_SERIAL = 0x1

    def __init__(self, devices):
        if devices is None:
            raise ValueError

        self.devices = devices

    def start(self):
        pass

    def add_device(self, name, device_id, ports, comm_type=COMM_TYPE_SERIAL):
        if not device_id:
            raise ValueError('Empty Device ID not allowed')
        devices = self.devices.keys()

        if device_id in devices:
            print("Already present Device-ID %s" % device_id)
            return self.devices[device_id]

        # Create a device Object structure to hold all information
        # related to this device

        self.devices[device_id]=dict()

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

    def remove_device(self, device_id):
        if not device_id:
            raise ValueError('Empty Device ID not allowed')

        device_obj = self.devices.pop(device_id, None)
        if not device_obj:
            print("[{}] Device-ID {} not found. Already removed?".format(self.name, device_id))

    def get_dev_serials(self):
        for dev in self.devices.keys():
            ser_obj = self.devices[dev]['serial']

class AgentService:

    def __init__(self, ip_address, port, host_id, name=None):
        # Hold a dictionary for all the attached devices
        if not (host_id and ip_address):
            raise ValueError('Empty HostAgent ID or IP-Address not allowed')
        self.host_id = host_id
        if not name:
            self.name = "HostAgent-" + host_id
        else:
            self.name = name

        self.address = ip_address

        self.devices = dict()

        self.server_port = port

        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        self.remoteSync = DeviceAgentServicer(self)
        self.remoteSerial = RemoteSerialServicer(self)
        self.deviceScanner = LocalDeviceScanner(self.devices)

        framework_pb2_grpc.add_DeviceAgentServicer_to_server(self.remoteSync, self.server)
        framework_pb2_grpc.add_RemoteSerialServicer_to_server(self.remoteSerial, self.server)
        self.server.add_insecure_port('[::]:'+str(port))

    def start(self):
        self.deviceScanner.start()
        self.server.start()

    def stop(self):
        self.server.stop(0)

    def get_device_list(self):
        return [v for v in self.devices.keys()]

    def get_device(self, device_id):
        return self.devices.get(device_id)

    def has_device(self, device_id):
        if self.devices.get(device_id) is None:
            return False
        else:
            return True

if __name__ == "__main__":
    default_port = 12121
    import argparse

    parser = argparse.ArgumentParser(
        description='HostAgent Server Argument Parser')

    parser.add_argument(
        '--port',
        nargs='?',
        help='Server port number',
        default=default_port)

    parser.add_argument(
        '--id',
        nargs='?',
        help='Host Agent ID')

    parser.add_argument(
        '--device_info',
        nargs=4,
        help='Device ID and Ports(of device being attached)')

    args = parser.parse_args()
    if args.port is None:
        print('[Server] Using Default port {}'.format(default_port))
        args.port = default_port

    if args.id is None:
        parser.error("must provide a Host Agent ID")

    if args.device_info is None:
        parser.error("must provide Attached device ports")

    print(args.device_info)

    hostagent_server = AgentService('localhost', args.port, str(args.id))

    hostagent_server.deviceScanner.add_device(args.device_info[0],
                                              args.device_info[1],
                                              [args.device_info[2],
                                              args.device_info[3]])
    # add_dummy_devices(hostagent_server)
    hostagent_server.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        print('[Server] Keyboard interrupted')
        hostagent_server.stop()

