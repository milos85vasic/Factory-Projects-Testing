from Toolkit.commands import *

from .test import test_user_prefix

def cleanup_test_users():
    command = ""
    users = get_users_list()
    for i, user in enumerate(users):
        if test_user_prefix in user:
            command += userdel(user)
            if i < users.__len__ - 1:
                command += ";"
            print("User del. command: " + command)
    return command


def cleanup_special_groups():
    #  TODO:        
    return ""


if __name__ == '__main__':
    steps = []
    steps.append(cleanup_test_users())
    steps.append("rm -f " + os.path.basename(__file__))
    run(steps)

