import os, sys, subprocess
import argparse
import getpass
import atexit

from utils import alice_receiver as ar
from commander import Commander, Dummy

# Version Control Constants
APPLICATION_NAME = "Alice"
APPLICATION_RELEASE = 0
APPLICATION_REVISION = 136

VERBOSITY = 0
should_listen = False

alice = None

def log(s, tolerance=1):
    global VERBOSITY

    if VERBOSITY >= tolerance:
        print(s)

def main():
    global use_voice, alice

    if use_voice:
        recognize = ar.AliceReceiver(str(raw_input("Alice login: ")),
                str(getpass.getpass()), alice.parse_query, debug=False)
        print("Alice is listening on Facebook!")
        recognize.listen()
    else:
        while True:
            query = str(raw_input("alice > "))
            alice.parse_query(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alice - Linux Virtual Assistant")
    parser.add_argument("--use-voice", "-V", action="store_true")
    parser.add_argument("--test", "-T", action="store_true")
    parser.add_argument("--monitors", "-m", action="store_true")
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version="%s %d.%d" %
            (APPLICATION_NAME, APPLICATION_RELEASE, APPLICATION_REVISION))

    args = parser.parse_args()

    use_voice = args.use_voice
    VERBOSITY = args.verbose

    actuator = Dummy if args.test else Commander

    config = {
        "monitors" : args.monitors,
    }

    alice = actuator(config=config, log_func=log)
    atexit.register(alice.stop_monitors)

    main()

