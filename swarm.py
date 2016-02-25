#!/usr/bin/env python
# coding: utf-8


# always use faster native code
import os
os.environ["PYCOIN_NATIVE"] = "openssl"


import sys # NOQA
import time # NOQA
import threading  # NOQA
import binascii  # NOQA
import signal  # NOQA
from storjnet.api import StorjNet  # NOQA
from crochet import setup  # NOQA
from twisted.python import log  # NOQA


# start twisted via crochet and remove twisted handler
setup()
signal.signal(signal.SIGINT, signal.default_int_handler)


# log.startLogging(sys.stdout)


SWARMSIZE = 5
START_NET_PORT = 6000
START_USER_PORT = 5000


if __name__ == "__main__":
    bootstrap_nodes = [["127.0.0.1", START_NET_PORT + i] for i in range(SWARMSIZE)]
    nodes = []
    try:
        # setup swarm
        for i in range(SWARMSIZE):
            netid = binascii.hexlify(os.urandom(32))  # isolate
            api = StorjNet(node_port=START_NET_PORT + i,
                           bootstrap=bootstrap_nodes, networkid=netid)
            thread = threading.Thread(
                target=api.startserver,
                kwargs={
                    "hostname": "127.0.0.1",
                    "port": START_USER_PORT + i,
                    "handle_sigint": False
                }
            )
            thread.start()
            nodes.append([api, thread])

        # server until killed
        while True:
            time.sleep(1)

    # expected exit mode
    except KeyboardInterrupt:
        pass

    # shutdown swarm
    finally:
        for api, thread in nodes:
            api.stopserver()
            thread.join()
