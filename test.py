import sys
from Toolkit.commands import *


def run_test():
    steps = [
        ssh("root", "date", port=22, host="127.0.0.1")
    ]

    run(steps)


if __name__ == '__main__':
    run_test()