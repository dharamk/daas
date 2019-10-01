import concurrent.futures as futures
import grpc
import framework_pb2_grpc
import framework_pb2

import requests

from serial.serialutil import SerialException
from agent_scanner import DeviceScanner
from agent_settings import *
from agent_auth import AgentAuthentication

def handle_serial_connect(server, dev_id):

    response = framework_pb2.SerialEvent()
    scanner = server.deviceScanner
    device = scanner.get_device(dev_id)

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
        pr0int("Sending Invoke Response ---> Event: {}".format(response.event))
        return response


def handle_serial_disconnect(server, dev_id):

    response = framework_pb2.SerialEvent()
    scanner = server.deviceScanner
    device = scanner.get_device(dev_id)

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
        print("Sending Invoke Response ---> Event: {}".format(response.event))
        return response


def handle_serial_reset(server, dev):
    response = framework_pb2.SerialEvent()
    response.device.device_id = dev
    response.event = framework_pb2.SerialEvent.SERIAL_RESET_DONE

    return response


def handle_device_reset(server, dev):

    response = framework_pb2.SerialEvent()
    response.device.device_id = dev
    response.event = framework_pb2.SerialEvent.SERIAL_RESET_DONE
    return response


def create_DeviceInfo_body(syncResponse, dev, found=True):
    obj = syncResponse.devices.add()
    obj.device_id = dev
    obj.device_status = \
        (framework_pb2.DeviceInfo.DEVICE_NOT_FOUND,
         framework_pb2.DeviceInfo.DEVICE_FOUND)[found]
    return obj


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

        dev_id = request.device_id
        # print('Got ReadLInes Command -->{}'.format(dev_id))
        dev_obj = self.server.get_device(dev_id)

        _lines = framework_pb2.SerialRead(error_set=False, device_id=dev_id)
        if dev_obj is None:
            # Handle invalid 'readline' - figure out a way of saying
            # DEVICE NOT FOUND
            _lines.error_set = True
            _lines.error_message = 'DEVICE NOT FOUND'
            return _lines
        try:
            read_lines = dev_obj.stdout()
            # print("Reading lines:{}".format(read_lines))
            _lines.lines.extend(read_lines)
            _lines.hostagent_id = self.server.host_id
        except Exception as e:
            print("Could not Open Serial-Port {}".format(e))
            _lines.error_set = True
            _lines.error_message = 'SERIAL READ ERROR'

        return _lines


class DeviceAgentServicer(framework_pb2_grpc.DeviceAgentServicer):

    def __init__(self, server):
        self.server = server

    def sync(self, request, context):
        print('Got Sync Request for: {}'.format(request.device_id))

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


class DeviceImageUploader(framework_pb2_grpc.DeviceImageUploadServicer):
    def __init__(self, server):
        self.server = server

    def store_dev_image(self, dev_id, bin_image, image_type="hex"):
        from pathlib import Path
        # Go to home directory
        try:
            home_dir = Path.home()
            AGENT_ROOT_DIR = ".agent"
            home_dir = home_dir / AGENT_ROOT_DIR
            IMAGE_PATH_SUFFIX = "tmp/images"
            home_dir = home_dir / IMAGE_PATH_SUFFIX
            Path.exists
            file_name = dev_id + "." + image_type
            print(file_name)
            home_dir = home_dir / file_name
            # ~/.agent/tmp/images/<dev_id>.hex
            print(home_dir)

            with open(str(home_dir), 'wb') as binary_file:
                binary_file.write(bin_image)

        except Exception as e:
            raise e
        else:
            return home_dir
            pass

        return home_dir

    def upload(self, request, context):
        print("Got Upload DeviceImage Reqeuest for: {}".format(request.device_id))
        print("Binary data length: {}".format(len(request.blob)))
        rsp = framework_pb2.UploadResponse()
        rsp.device_id = request.device_id
        dev = self.server.get_device(request.device_id)

        if dev:
            image_path = self.store_dev_image(request.device_id, request.blob)
            ret = dev.download_image(image_path)
            if ret:
                rsp.download_status = framework_pb2.UploadResponse.DOWNLOAD_COMPLETED
        else:
            rsp.download_status = framework_pb2.UploadResponse.DOWNLOAD_DEVICE_NOT_FOUND

        return rsp


class AgentService:

    def __init__(self, ip_address, port, host_id, name=None, auth=None):
        # Hold a dictionary for all the attached devices
        if not (host_id and ip_address):
            raise ValueError('Empty HostAgent ID or IP-Address not allowed')
        self.host_id = host_id
        if not name:
            self.name = "HostAgent-" + host_id
        else:
            self.name = name

        self.address = ip_address

        self.server_port = port
        self.server_started = False
        self.scanner_started = False
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        self.remoteSync = DeviceAgentServicer(self)
        self.remoteSerial = RemoteSerialServicer(self)
        self.deviceScanner = DeviceScanner()
        self.remoteImageUploader = DeviceImageUploader(self)
        self.auth = auth

        framework_pb2_grpc.add_DeviceAgentServicer_to_server(self.remoteSync, self.server)
        framework_pb2_grpc.add_RemoteSerialServicer_to_server(self.remoteSerial, self.server)
        framework_pb2_grpc.add_DeviceImageUploadServicer_to_server(self.remoteImageUploader, self.server)
        self.server.add_insecure_port('[::]:'+ str(port))

        print("Preparing Agent Instance {}:{}".format(self.address,self.server_port))

        # self.db = AgentDBServiceFirestoreAdminPrivilege(self)
        # self.db_agent_doc = AgentDocument(self)

    def start(self):
        self.deviceScanner.start()
        self.server.start()
        self.server_started = True
        self.scanner_started = True
        print("All services started Ok.")


    def stop(self):
        self.deviceScanner.stop()
        self.server.stop(0)
        self.server_started = False
        self.scanner_started = False


    def get_device_list(self):
        return [v for v in self.deviceScanner.get_all_devices()]

    def get_device(self, device_id):
        return self.deviceScanner.get_device(device_id)

    def has_device(self, device_id):
        if self.deviceScanner.get_device(device_id) is None:
            return False
        else:
            return True

    def get_host_id(self):
        return self.host_id

    def http_post_connection_status(self):
        if self.auth and self.auth.is_authenticated:
            body = {
                'idToken': self.auth.token_id,
                'aid': EMWEBED_AGENT_APP_SETTINGS['aid'],
                'grpc_port': self.server_port,
                'ip_address': self.address
            }

            ep = EMWEBED_SERVER_AGENT_ENDPOINTS['connection_status']
            full_url = EMWEBED_SERVER_URI + ep
            try:
                response = requests.post(full_url, json=body)
                response.raise_for_status()
            except HTTPError as http_err:
                print('HTTP error occured: {}'.format(http_err))
            except Exception as e:
                print('Other error: {}'.format(e))
            else:
                print('Success!!')
        else:
            raise Exception("User is not logged-in")


    def http_post_device_list(self):
        if self.auth and self.auth.is_authenticated:
            body = {
                'idToken': self.auth.token_id,
                'aid': EMWEBED_AGENT_APP_SETTINGS['aid'],
            }

            devs = self.get_device_list()
            if not devs:
                body['devices']['detected'] = devs
            try:
                response = requests.post(full_url, json=body)
                response.raise_for_status()
            except HTTPError as http_err:
                print('HTTP error occured: {}'.format(http_err))
            except Exception as e:
                print('Other error: {}'.format(e))
            else:
                print('Success!!')
        else:
            raise Exception("User is not logged-in")

    def http_post_service_status(self):
        pass


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

    agent = AgentService('localhost', args.port, str(args.id))

    agent.deviceScanner.add_device(args.device_info[0],
                                              args.device_info[1],
                                              [args.device_info[2],
                                              args.device_info[3]])
    # add_dummy_devices(hostagent_server)
    agent.start()
    try:
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        print('[Server] Keyboard interrupted')
        agent.stop()

