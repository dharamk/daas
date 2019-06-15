#!/bin/python3
import sys
import time

sys.path.append("..")

GRPC_PROTOBUF_PATH = "../../grpc"
sys.path.append(GRPC_PROTOBUF_PATH)

import agent_main as agent

if __name__ == "__main__":
    import hashlib
    default_port = 12121
    agent_id = hashlib.sha1(b"test").hexdigest()
    print(agent_id)

    ag = agent.AgentService('localhost', default_port, agent_id)
    ag.start()
    print(ag.get_device_list())
    while True:
        try:
            time.sleep(10000)
        except KeyboardInterrupt:
            print('[Server] Keyboard interrupted')
            ag.stop()
            break;