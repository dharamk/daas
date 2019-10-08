#!/bin/python3

"""
A function for Manager to get all hosts names/ports etc.

Returns:
List of HostAgent objects
"""

GET_AGENT_LIST_METHOD = 1 # static list

class Agent:
    def __init__(self, agent_id, url=None, address=None, port=None):
        if not agent_id:
            raise ValueError
        self.agent_id = agent_id
        self.url = url
        self.address = address
        self.port = port

    def get_url(self):
        if self.url:
            return self.url
        elif self.address and self.port:
            self.url = self.address + str(':' + str(self.port))

        return self.url


def get_agent_list_static():
    agent_list = list()
    host1 = Agent(agent_id='0001', url='localhost:12121')
    agent_list.append(host1)

    host2 = Agent(agent_id='0002', url='localhost:12122')
    agent_list.append(host2)

    host3 = Agent(agent_id='0003', url='localhost:12123')
    agent_list.append(host3)

    return agent_list


def get_agent_list_hashlib():
    import hashlib
    default_port = 12121
    agent_id = hashlib.sha1(b"test").hexdigest()
    agent_list = list()
    agent = Agent(agent_id, url=None, address="localhost", port=default_port)
    # print(agent.get_url())
    agent_list.append(agent)
    return agent_list


def get_agent_list():

    if GET_AGENT_LIST_METHOD == 1:
        print("getting agents static list")
        # return get_agent_list_static()
        return get_agent_list_hashlib()
    else:
        return None

