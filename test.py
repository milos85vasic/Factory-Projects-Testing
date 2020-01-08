import sys
import json

from os import path
from Toolkit.commands import *

key_ssh = "ssh"
key_user = "user"
key_port = "port"
key_host = "host"
configuration_file = "configuration.json"

def run_test():
    if not path.exists(configuration_file):
        sys.exit("Configuration file is not available.")
        return

    data = json.load(open(configuration_file))

    steps = [
        ssh(
            data[key_ssh][key_user], 
            "date", #  TODO: Trigger propper command remotely.
            port=data[key_ssh][key_port], 
            host=data[key_ssh][key_host]
        )
    ]

    run(steps)


if __name__ == '__main__':
    run_test()