import sys
import json
import time

from os import path
from Toolkit.commands import *
from Toolkit.configuration import *

key_sshs = "sshs"
key_user = "user"
key_port = "port"
key_host = "host"
key_tests = "tests"
key_test_name = "name"
key_test_type = "type"
key_test_configuration = "configuration"
key_test_configuration_account = "account"
key_test_configuration_password = "password"
key_application_mail_server_factory = "Mail-Server-Factory"

test_user_prefix = "test_factoy_user_"
websetup_script = "websetup.py"
remove_test_users_script = "remove_test_users.py"
echo_python_cmd_script = "echo_python_cmd.sh"
configuration_file = "configuration.json"
toolkit_directory = "Toolkit"
toolkit_repo = "https://github.com/milos85vasic/Apache-Factory-Toolkit.git"
toolkit_repo_raw_access = "https://raw.githubusercontent.com/milos85vasic/Apache-Factory-Toolkit/master/"
factory_testing_repo_raw_access = "https://raw.githubusercontent.com/milos85vasic/Factory-Projects-Testing/master/"

def get_init_commands():
    millis = int(round(time.time() * 1000))
    url_millis = "?_=" + str(millis)
    self_script = os.path.basename(__file__)
    steps = [
                rm(toolkit_directory),
                "mkdir " + toolkit_directory,
                "git clone --recurse-submodules " + toolkit_repo + " ./" + toolkit_directory,
                curl_to(toolkit_repo_raw_access + echo_python_cmd_script + url_millis, echo_python_cmd_script),
                curl_to(toolkit_repo_raw_access + websetup_script + url_millis, websetup_script),
                curl_to(factory_testing_repo_raw_access + self_script + url_millis, self_script),
                curl_to(factory_testing_repo_raw_access + remove_test_users_script + url_millis, remove_test_users_script),
                "`sh " + echo_python_cmd_script + "` " + remove_test_users_script
    ]
    return steps


def get_shutdown_commands():
    self_script = os.path.basename(__file__)
    steps = [
        rm(echo_python_cmd_script),
        rm(toolkit_directory),
        rm(websetup_script),
        rm(echo_python_cmd_script),
        rm(remove_test_users_script),
        rm(self_script),
        rm("__pycache__")
    ]
    return steps


def get_installation_commands(type):
    switcher = {
        key_application_mail_server_factory: 
            [
                "`sh " + echo_python_cmd_script + "` " + websetup_script + " " + key_application_mail_server_factory,
            ]
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")


def get_cleanup_commands(type):
    switcher = {
        key_application_mail_server_factory: 
            [
                rm(key_application_mail_server_factory),
                groupdel(mail_server_factory_group),
                rm(mail_server_factory_configuration_dir)
            ]
    }
    return switcher.get(type, "echo 'Unsupported application type: " + type + "'")


def get_start_commands(type, configuration):
    millis = int(round(time.time() * 1000))
    if key_test_configuration_account in configuration:
        account = configuration[key_test_configuration_account]
    else:
        account = test_user_prefix + str(millis)
    password_argument = ""
    if key_test_configuration_password in configuration:
        password_argument = " " + configuration[key_test_configuration_password]
    switcher = {
        key_application_mail_server_factory: 
            [
                concatenate(
                    cd(key_application_mail_server_factory),
                    "`sh " + toolkit_directory + "/" + echo_python_cmd_script + "` " + " add_account.py " + account + password_argument
                )
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
    ssh_accesses = data[key_sshs]

    for ssh_access in ssh_accesses:
        steps = []
        for command in get_init_commands():
            append_command(steps, ssh_access, command)
        run(steps)
        
        for test in data[key_tests]:
            print("Executing test:", test[key_test_name])
            for command in get_cleanup_commands(test[key_test_type]):
                append_command(steps, ssh_access, command)

            for command in get_installation_commands(test[key_test_type]):
                append_command(steps, ssh_access, command)

            for command in get_start_commands(test[key_test_type], test[key_test_configuration]):
                append_command(steps, ssh_access, command)

            run(steps)
            print("Test executed:", test[key_test_name])
        
        steps = []
        for command in get_shutdown_commands():
            append_command(steps, ssh_access, command)
        run(steps)


if __name__ == '__main__':
    run_test()