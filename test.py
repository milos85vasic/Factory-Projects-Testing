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

websetup_script = "websetup.py"
echo_python_cmd_script = "echo_python_cmd.sh"
configuration_file = "configuration.json"
toolkit_directory = "Toolkit"
toolkit_repo_raw_access = "https://raw.githubusercontent.com/milos85vasic/Apache-Factory-Toolkit/master/"

def get_installation_commands(type):
    switcher = {
        key_application_mail_server_factory: 
            [
                curl_to(toolkit_repo_raw_access + echo_python_cmd_script, echo_python_cmd_script),
                curl_to(toolkit_repo_raw_access + websetup_script, websetup_script),
                "`sh " + echo_python_cmd_script + "` " + websetup_script + " " + key_application_mail_server_factory,
            ]
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")

def get_shutdown_commands(type):
    switcher = {
        key_application_mail_server_factory: 
            [
                rm(echo_python_cmd_script)
            ]
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")


def get_cleanup_commands(type):
    switcher = {
        key_application_mail_server_factory: 
            [
                rm(toolkit_directory),
                rm(websetup_script),
                rm(echo_python_cmd_script)
            ]
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")


def append_command(steps, ssh_access, command):
    to_execute = ssh(
            ssh_access[key_user], 
            "'" + command + "'",
            port=ssh_access[key_port], 
            host=ssh_access[key_host]
    )
    steps.append(to_execute)
    print("Will execute: ", to_execute)


def run_test():
    if not path.exists(configuration_file):
        sys.exit("Configuration file is not available.")
        return

    data = json.load(open(configuration_file))
    ssh_access = data[key_ssh]

    steps = []
    for test in data[key_tests]:
        print("Executing test:", test[key_test_name])
        for command in get_cleanup_commands(test[key_test_type]):
            append_command(steps, ssh_access, command)

        for command in get_installation_commands(test[key_test_type]):
            append_command(steps, ssh_access, command)

        for command in get_shutdown_commands(test[key_test_type]):
            append_command(steps, ssh_access, command)
        
        run(steps)
        print("Test executed:", test[key_test_name])


if __name__ == '__main__':
    run_test()