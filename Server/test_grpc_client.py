#!/bin/python3

import grpc
import threading
import enum
import time
import sys

sys.path.append("..")

GRPC_PROTOBUF_PATH = "../grpc"
sys.path.append(GRPC_PROTOBUF_PATH)

import framework_pb2
import framework_pb2_grpc
from host_list import get_agent_list

class AgentTableKeys(enum.Enum):
    agent = 0
    channel = 1
    stubs = 2
    devices = 3


def getAgentTableEntry(agent):
    """
    Agent-Table Entry object Helper function
    """
    if agent is None:
        return None

    t = dict()
    # t["agent"] = <Actual Agent Object>
    t[AgentTableKeys.agent.name] = agent
    # t["channel"] = None ; Will be updated during rest of the operations
    t[AgentTableKeys.channel.name] = None
    # t["stubs"] = <Empty list> ; To maintain all the grpc stubs we need to maintain
    t[AgentTableKeys.stubs.name] = list()
    # t["devices"] = <Empty list>; Maintain all device objects associated with this unique Agent
    t[AgentTableKeys.devices.name] = list()

    return t


class AgentMap:

    def __init__(self, agents=None):
        """
        Initialize a AgentMap object.
        One for managing the devices directly and another
        table for Hostagents. It will start with an initial list
        of hostagents(list of hostagent-id objects to start with)

        'device_id_0':
            'agent_id': 'agent_01'

        {
            'hostagent_01' :
                {
                    'hostagent': hostagent,
                    'channel': grpc_channel,
                    'stubs':[syncStub, SerialStub],
                    'devices': ['device_id_0', 'device_id_1', 'device_id_3']
                },
            'hostagent_02' :
            {

            },
        }
        """
        self.read_lock = threading.Lock()
        self.agents = dict()

        # For each Agent given in the list - create a table based on its ID -
        # Each agent passed in this Map should have a unique field 'agent_id'
        if agents:
            for agent in agents:
                self.agents[agent.agent_id] = getAgentTableEntry(agent)

    def addHostAgent(self, new_agent):
            agent_tbl = self.agents
            self.read_lock.acquire()
            d = agent_tbl.get(new_agent.agent_id)
            if d is None:
                entry = getAgentTableEntry(new_agent)
                agent_tbl[new_agent.agent_id] = entry
            self.read_lock.release()

    """
    Takes a string hostagent_id as key and returns Agentmap value
    comprising of channels, stubs, hostagent info etc
    """
    def get_agent(self, agent_id):
        agent_tbl = self.agents
        try:
            d = agent_tbl[agent_id]
        except KeyError as e:
            print(e)
            return None
        return d

    def get_all_agents(self):
        agent_tbl = self.agents
        return agent_tbl.values()

    def get_sync_stub(self, agent_id):
        agent_tbl = self.agents
        try:
            d = agent_tbl[agent_id]
        except KeyError as e:
            print(e)
            return None
        return d[AgentTableKeys.stubs.name][0]

    def get_all_sync_stubs(self):
        sync_stubs = [v[AgentTableKeys.stubs.name][0]
                      for v in self.agents.values()]
        return sync_stubs

    def get_serial_stub(self, host_id):
        agent_tbl = self.agents
        try:
            d = agent_tbl[host_id]
        except KeyError as e:
            print(e)
            return None
        return d[AgentTableKeys.stubs.name][1]

    def get_all_serial_stubs(self):
        serial_stubs = [v[AgentTableKeys.stubs.name][1]
                        for v in self.agents.values()]
        return serial_stubs

    def get_device_image_upload_stub(self, dev_id, agent_id):
        agent_tbl = self.agents
        try:
            d = agent_tbl[agent_id]
        except KeyError as e:
            print(e)
            return None
        return d[AgentTableKeys.stubs.name][2]

def create_SyncRequest_body(device_ids):
    obj = framework_pb2.SyncRequest()
    obj.device_id.extend(device_ids)
    return obj


def create_SerialCmd(dev_id, command, user_id="server"):
    obj = framework_pb2.SerialCmd()
    obj.command = command
    obj.device.device_id = dev_id
    obj.user_id = user_id
    return obj


def create_UploadRequest(dev_id, agent_id, bin_file):
    obj = framework_pb2.DeviceImage()
    obj.device_id = dev_id
    obj.agent_id = agent_id
    # obj.blob = b'helloiamsupposedtobebinarydatabutrightnowimjustdemonstratinghowtosendbinarydatafiles'
    return obj


def start_serial(devices):
    # for device in devices:
    #     channel = device['channel']
    pass


def connect_hostagent(host, is_secure=False):

    url = host[AgentTableKeys.agent.name].get_url()
    print(url)
    if url is None:
        raise ValueError
    try:
        channel = host[AgentTableKeys.channel.name] = grpc.insecure_channel(url)
    except Exception as e:
        raise e

    stubs = host[AgentTableKeys.stubs.name]
    stubs.append(framework_pb2_grpc.DeviceAgentStub(channel))
    stubs.append(framework_pb2_grpc.RemoteSerialStub(channel))
    stubs.append(framework_pb2_grpc.DeviceImageUploadStub(channel))

    print("Stubs added are: {}".format(stubs))


class DeviceTable:
    def __init__(self):
        self.devices = dict()
        self.read_lock = threading.Lock()

    def _add_device(self, _dev_id, agent_id):
        self.read_lock.acquire()
        self.devices[_dev_id] = agent_id
        self.read_lock.release()

    def _remove_device(self, _dev_id):
        self.read_lock.acquire()
        self.devices.pop(_dev_id, None)
        self.read_lock.release()

    def get_devices(self):
        return list(self.devices.keys())

    def get_agent(self, dev_id):
        return self.devices.get(dev_id)


def serial_command_iterator(dev_id, command):
    cmds = [create_SerialCmd(dev_id, framework_pb2.SerialCmd.SERIAL_CONNECT)]
    for cmd in cmds:
        yield cmd


"""
Starts a service which reads the serial logs from remote devices to which
serial connection has been established.

"""
class RemoteSerialReader:
    def __init__(self, server):
        self.server = server
        self.lock = threading.Lock()
        self.reader_alive = False
        self.cached_devices = None
        self.serial_devices = list()

    def start(self, use_cached=True):
        if not self.reader_alive:
            if not self.cached_devices:
                self.serial_devices = list()
            elif use_cached and self.cached_devices:
                self.serial_devices = self.cached_devices
            self.use_cached = use_cached
            self.reader = threading.Thread(target=self.remote_reader,
                                           name="Remote Serial Reader Thread")
            self.reader.daemon = True
            self.reader_alive = True
            self.reader.start()

    def stop(self):
        if self.reader_alive:
            self.reader_alive = False
        time.sleep(0.5)
        self.reader.join()
        self.reader = None
        if self.use_cached:
            self.cached_devices = self.serial_devices
        self.serial_devices = None

    def add_serial_device(self, device_id):
        self.lock.acquire()
        if not self.serial_devices.__contains__(device_id):
            print('Added Device to Serial-Read-Loop '+ device_id)
            self.serial_devices.append(device_id)
            print(self.serial_devices)
        self.lock.release()

    def remove_serial_device(self, device_id):
        self.lock.acquire()
        if self.serial_devices.__contains__(device_id):
            print('Removed Device from Serial-Read-Loop '+ device_id)
            self.serial_devices.remove(device_id)
        self.lock.release()

    def remote_reader(self):
        srv = self.server
        while self.reader_alive:
            time.sleep(1.0)
            self.lock.acquire()
            for dev in self.serial_devices:
                agent_id = srv.device_map.get_agent(dev)
                serial_stub = srv.host_map.get_serial_stub(agent_id)
                # print("Reading Lines from Host:{} Device:{} -->".format(host_id, dev))
                if serial_stub:
                    obj = framework_pb2.SerialDevice(device_id=dev)
                    serial_read = serial_stub.readLines(obj)
                    # print(serial_read)
                    for line in serial_read.lines:
                        pass
                        # print(line.rstrip('\r\n'))

            self.lock.release()


class AgentManager:

    def __init__(self):
        self.device_map = DeviceTable()
        self.host_map = AgentMap()
        self.remote_serial_reader = RemoteSerialReader(self)

    def _start(self):
        agents = get_agent_list()
        if agents:
            for host in agents:
                self.host_map.addHostAgent(host)

    def _connect(self, agent_id):
        if not agent_id:
            printf("Error Agent-ID not specififed")
            raise ValueError

        if agent_id == 'all':
            agents = self.host_map.get_all_agents()
            for agent in agents:
                connect_hostagent(agent)
        else:
            agent = self.host_map.get_agent(host_id)
            connect_hostagent(agent)

    def _sync_all(self):
        hosts = self.host_map.get_all_agents()
        sync_stubs = self.host_map.get_all_sync_stubs()
        syncRequest = create_SyncRequest_body(['all'])
        # First Stub is SyncService
        for stub in sync_stubs:
            syncResponse = stub.sync(syncRequest)
            print(syncResponse.hostagent_id)
            print(syncResponse.devices)
            for dev in syncResponse.devices:
                self.device_map._add_device(dev.device_id, syncResponse.hostagent_id)

    def _sync(self, sync_all=True, agent_id=None):

        if sync_all:
            self._sync_all()
        elif agent_id is not None:
            agent = self.host_map.get_agent(agent_id)
            syncRequest = create_SyncRequest_body(['all', ])
            stub = self.host_map.get_sync_stub(agent_id)
            stub = host[AgentTableKeys.stubs.name][0]
            syncResponse = stub.sync(syncRequest)

            for dev_info in syncResponse.devices:
                self.device_map._add_device(dev_info.device_id, syncResponse.hostagent_id)

            print("-------------------")

            print(syncResponse.hostagent_id)
            print(syncResponse.devices)

    def dump_devices(self):
        print(self.device_map.get_devices())
        return self.device_map.get_devices()

    def setup_serial(self, dev_id):
        print('--> Setting up Serial on {}'.format(dev_id))
        agent_id = self.device_map.get_agent(dev_id)
        print("--> Device located on Host: {}".format(agent_id))
        if agent_id is None:
            raise ValueError

        agent = self.host_map.get_agent(agent_id)
        if agent is None:
            raise ValueError
        response_list = list()

        serial_stub = self.host_map.get_serial_stub(agent_id)

        cmd_iterator = serial_command_iterator(dev_id, framework_pb2.SerialCmd.SERIAL_CONNECT)

        events = serial_stub.Invoke(cmd_iterator)
        print(events)

        for event in events:
            print('--> Got Event {} {} {}'.format(event, event.event, event.device.device_id))

        if event.event == framework_pb2.SerialEvent.SERIAL_CONNECTED:
            return True

        return False

        # for response in response_list:
        #     print(response.event)
        #     print(response.device.device_id)
        #     print(response.device.serial_name)


    def upload_device_image(self, image_path, dev_id=None, agent_id=None):
        if not image_path:
            raise ValueError
        if not dev_id:
            dev_id = "all"

        if not agent_id:
            agent_id = "all"

        # Hack Hack Hack to quickly try the rpc
        dev_id = '19091301f3080e1602f3080e00000000000000002e127069'
        agent_id = 'a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
        image_path = "image.hex"
        with open(image_path, "rb") as binary_file:
        # Read the whole file at once
            bdata = binary_file.read()
            print(len(bdata))
            uploadRequest = create_UploadRequest(dev_id, agent_id, None)
            uploadRequest.blob = bdata
            device_stub = self.host_map.get_device_image_upload_stub(dev_id, agent_id)
            upload_response = device_stub.upload(uploadRequest)
            print(upload_response)

if __name__ == '__main__':

    manager = AgentManager()
    try:
        manager._start()
    except Exception as e:
        raise e


    manager._connect("all")

    manager._sync_all()

    devs = manager.dump_devices()

    # manager.remote_serial_reader.start()
    # for dev in devs:
    #     if manager.setup_serial(dev):
    #         time.sleep(1.0)
    #         manager.remote_serial_reader.add_serial_device(dev)

    while True:
        try:
            cmd = input("Enter the command you want to execute >>")
            if cmd == 'download' or cmd == 'Download':
                binary_file_path = input("Enter the Binary file path(full-name) >>")
                if binary_file_path != '' and binary_file_path != " ":
                    manager.upload_device_image(binary_file_path)
                else:
                    print("Invalid Binary file path name")
            time.sleep(1)
        except KeyboardInterrupt as e:
            manager.remote_serial_reader.stop()
            time.sleep(1.0)
            raise e
