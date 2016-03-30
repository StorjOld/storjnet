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


if __name__ == "__main__":
    run_swarm(size=50, net_start_port=6000,
              rpc_start_port=5000, quasar_depth=1)
