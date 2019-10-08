#!/bin/python3

import base_server

# class DaasCmdLineServer(DaaSServer):
#     def __init__(self):
#         pass


class DaasCmdLineServerHandler:
    def __init__(self, obj):
        self.daas_instance = obj
        pass


def find_device_handler(*args):
    print("Looking up for device")
    pass


def connect_handler(*args):
    pass


def disconnect_handler(*args):
    pass


def enable_serial_handler(*args):
    pass


def disable_serial_handler(*args):
    pass


def download_handler(*args):

    # binary_file_path = input("Enter the Binary file path(full-name) >>")
    #             if binary_file_path != '' and binary_file_path != " ":
    #                 manager.upload_device_image(binary_file_path)
    #             else:
    #                 print("Invalid Binary file path name")
    pass


def list_handler(*args):
    pass


def list_device_handler(*args):
    pass


def list_agents_handler(*args):
    pass


def help_handler(*args):
    print("list [devices | agents]")
    print("find           <device_id>")
    print("connect        <device_id>")
    print("disconnect     <device_id>")
    print("enable_serial  <device_id>")
    print("disable_serial <device_id>")
    print("download       <device_id>  <image_path>")


command_handlers = {
    "find": find_device_handler,
    "connect": connect_handler,
    "disconnect": disconnect_handler,
    "enable_serial": enable_serial_handler,
    "disable_serial": disable_serial_handler,
    "download": download_handler,
    "list": list_handler,
    "help": help_handler
}

"""
Server will start
i. while (wait for command)
"""
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='Commandline Server Argument Parser')

    parser.add_argument(
        'subcommand',
        help="Sub-Command to execute",
        type=str,
        default=None)

    parser.add_argument(
        'device_id',
        type=str,
        nargs='?',
        help='<Device-ID>',
        default=None)

    parser.add_argument(
        'image_path',
        nargs='?',
        help='<Image path to download>',
        default=None)

    server = base_server.EmwebedServer.get_server()
    if not server:
        server = base_server.EmwebedServer()
        base_server.DaaSServer.set_server(server)

    while (True):
        try:
            raw_line = input("cmd >>")
            raw_line.rstrip("\r\n")
            if not raw_line:
                continue

            split_line = raw_line.split()

            args = parser.parse_args(split_line)

            if args.subcommand in command_handlers:
                command_handlers[args.subcommand](args.device_id, args.image_path)
            else:
                print("Invalid command - Enter 'help' for details")
            # time.sleep(1)
        except KeyboardInterrupt as e:
            # manager.remote_serial_reader.stop()
            # time.sleep(1.0)
            raise e
        # wait for the commands/requests on console
