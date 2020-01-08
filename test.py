import sys
import json
from Toolkit.commands import *


def run_test():
    # TODO: Check if file exists. If not exit with error.

    data = json.load(open("configuration.json"))

    steps = [
        ssh(
            data["ssh"]["user"], 
            "date", #  TODO: Trigger propper command remotely.
            port=data["ssh"]["port"], 
            host=data["ssh"]["host"]
        )
    ]

    run(steps)


if __name__ == '__main__':
    run_test()