from Toolkit.commands import *

from test import test_user_prefix

def cleanup_test_users():
    command = ""
    users = get_users_list()
    for user in users:
        if test_user_prefix in user:
            command += userdel(user) + ";"
    return command


def cleanup_special_groups():
    #  TODO:        
    return ""


if __name__ == '__main__':
    steps = []
    steps.append(cleanup_test_users())
    steps.append("rm -f " + os.path.basename(__file__))
    run(steps)

