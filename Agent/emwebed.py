#!/bin/python3
"""
Main Agent application
- starts an Agent Client
- Does the initial Handshake with Server
> python emwebed.py start_agent

"""
import os
import sys
import subprocess
import pathlib
import time

EMWEBED_AGENT_ROOT_DIR = pathlib.Path.cwd()
sys.path.append(str(EMWEBED_AGENT_ROOT_DIR))
COMMON_LIBS_PATH = EMWEBED_AGENT_ROOT_DIR / 'common'
GRPC_PROTOBUF_PATH = EMWEBED_AGENT_ROOT_DIR / 'grpc_proto'
print(COMMON_LIBS_PATH)
print(GRPC_PROTOBUF_PATH)
sys.path.append(str(GRPC_PROTOBUF_PATH))
sys.path.append(str(COMMON_LIBS_PATH))

from agent_settings import *
import agent_auth
import agent_client


def random_port_in_range(max_val, min_val, prohibited=None):
    import random
    r = random.randint(max_val, min_val)
    avoid = set(prohibited)
    if len(avoid) == (max_val - min_val):
        raise ValueError

    while r in avoid:
        r = random.randint(max_val, min_val)

    return r


def get_port():
    """
    Use system command 'lsof -i | grep <port_number>' to see if
    the port is in use locally or not. lsof -i combined with a grep
    throws an exit error code of 1 when it  is not able to found a port
    the search patter. This can be simplified but for now, it should
    do the trick.
    """
    default_port = EMWEBED_AGENT_PORT_MIN
    return default_port
    available_port = None
    prohibited = []
    print("Probing known ports...")
    while not available_port:
        # i.e the port is already in use.
        if not default_port:
            default_port = random_port_in_range(EMWEBED_AGENT_PORT_MIN,
                                                EMWEBED_AGENT_PORT_MAX, prohibited)
        p = f"lsof -i | grep {default_port}"
        exitcode, output = subprocess.getstatusoutput(p)
        if not exitcode:
            prohibited.append(default_port)
            default_port = None
            # port is already in-use
            # continue probing with another random port.
        else:
            # print(f"Looking for port: {default_port} returned exit-code {exit}")
            if not output:
                # Port is not in-use and exit-code is non-zero(miscellaneous error)
                # This could be it...
                available_port = default_port
            else:
                raise OSError

    return available_port


def get_ip_address():
    """
    Run system command 'hostname -I' to fetch primary IP address of the Host
    Returns first IP-Address to the caller
    """
    # default utf-8 decoding as check_output() returns byte-string
    ip_address_string = subprocess.check_output(["hostname", "-I"]).decode()
    # print(ip_address_string)
    first_ip = ip_address_string.split()
    # print(first_ip[0])
    return first_ip[0]


if __name__ == "__main__":
    default_cmd = 'start_agent'
    app_config = None
    # 1. load the settings
    # 2. Log-in to the server with agent
    # 3. Update Connection details and fetch any details
    #    which server might have to share.
    print("Fetching Account details...")
    auth = agent_auth.AgentAuthentication()

    # do the authentication
    try:
        auth.sign_in_email_password(EMWEBED_AGENT_APP_USERID,
                                    EMWEBED_AGENT_APP_PASSPHRASE,
                                    EMWEBED_AGENT_FIREBASE_APP_SETTINGS["apiKey"],
                                    EMWEBED_AGENT_APP_SETTINGS)
    except Exception as e:
        print(e)
        raise(e)

    if not auth.is_authenticated:
        raise Exception('Authentication failed.')

    # instantiate this Agent object - irrespective of authentication status
    ip_address = get_ip_address()

    # get a port to run grpc service - on which Server can establish
    # a grpc connection to the Agent
    try:
        port = get_port()
    except Exception as e:
        raise e

    service = agent_client.AgentService(ip_address, port,
                                        EMWEBED_AGENT_APP_SETTINGS['aid'],
                                        EMWEBED_AGENT_APP_SETTINGS['name'], auth)
    service.start()

    # update connection-status
    service.http_post_connection_status()

    while True:

        try:
            time.sleep(10000)
        except KeyboardInterrupt:
            print('[Server] Keyboard interrupted')
            service.stop()
            break
