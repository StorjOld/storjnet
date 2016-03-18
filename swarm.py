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
from storjnet.api import run_swarm  # NOQA
from crochet import setup  # NOQA
from twisted.python import log  # NOQA


# start twisted via crochet and remove twisted handler
setup()
signal.signal(signal.SIGINT, signal.default_int_handler)


# log.startLogging(sys.stdout)


SWARM_SIZE = 50
NET_START_PORT = 6000
RPC_START_PORT = 5000


if __name__ == "__main__":
    run_swarm(size=SWARM_SIZE,
              net_start_port=NET_START_PORT,
              rpc_start_port=RPC_START_PORT)
