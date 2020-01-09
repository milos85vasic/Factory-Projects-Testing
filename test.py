import sys
import json

from os import path
from Toolkit.commands import *

key_ssh = "ssh"
key_user = "user"
key_port = "port"
key_host = "host"
key_tests = "tests"
key_test_name = "name"
key_test_type = "type"
key_application_mail_server_factory = "Mail-Server-Factory"

configuration_file = "configuration.json"

def get_installation_command(type):
    switcher = {
        key_application_mail_server_factory: 
            curl(https://raw.githubusercontent.com/milos85vasic/Apache-Factory-Toolkit/master/websetup.py) + 
            " > websetup.py; " + get_python_cmd() + " websetup.py Mail-Server-Factory"
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")


def cleanup_test():
    #  Do cleanup the test.
    return


def run_test():
    cleanup_test()

    if not path.exists(configuration_file):
        sys.exit("Configuration file is not available.")
        return

    data = json.load(open(configuration_file))

    for test in data[key_tests]:
        steps = [
            ssh(
                data[key_ssh][key_user], 
                "'" + get_installation_command(test[key_test_type]) + "'",
                port=data[key_ssh][key_port], 
                host=data[key_ssh][key_host]
            )
        ]

        print("Executing:", test[key_test_name])
        run(steps)
        print("Executed:", test[key_test_name])


if __name__ == '__main__':
    run_test()