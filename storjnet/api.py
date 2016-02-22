import apigen
import binascii
import btctxstore
import crochet
from collections import defaultdict
from . protocol import Protocol
from pycoin.encoding import a2b_hashed_base58
from storjkademlia.storage import ForgetfulStorage
from storjkademlia.node import Node
from storjkademlia.network import Server
from pyp2p.lib import get_unused_port
from . version import __version__  # NOQA


class Storjnet(apigen.Definition):

    def __init__(self, key=None, port=None, bootstrap=None,
                 networkid="mainnet", call_timeout=120,
                 limit_send_sec=None, limit_receive_sec=None,
                 limit_send_month=None, limit_receive_month=None,
                 quiet=False, debug=False, verbose=False, noisy=False):

        self._log = None  # TODO get logger
        self._call_timeout = call_timeout
        self._setup_node(key)
        self._setup_protocol()
        self._setup_kademlia(bootstrap, port)
        # TODO setup quasar
        # TODO setup messaging
        # TODO setup streams
        # TODO wait until overlay stable

    def _setup_node(self, key):
        self._btctxstore = btctxstore.BtcTxStore()
        key = key or self._btctxstore.create_key()
        is_hwif = self._btctxstore.validate_wallet(key)
        self._key = self._btctxstore.get_key(key) if is_hwif else key
        address = self._btctxstore.get_address(self._key)
        self._nodeid = a2b_hashed_base58(address)[1:]

    def _setup_protocol(self):
        storage = ForgetfulStorage()
        self._protocol = Protocol(Node(self._nodeid), storage, ksize=20,
                                  max_messages=1024)
        # TODO set rpc logger

    def _setup_kademlia(self, bootstrap, port):
        self._port = port or get_unused_port()
        self._kademlia = Server(id=self._nodeid, protocol=self._protocol)
        self._kademlia.bootstrap(bootstrap or [])
        self._kademlia.listen(self._port)
        # TODO set kademlia logger

    @apigen.command()
    def dht_put(self, key, value):
        """Store key/value pair in DHT."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self._kademlia.set(key, value)
        return func()

    @apigen.command()
    def dht_get(self, key):
        """Get value for given key in DHT."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self._kademlia.get(key)
        return func()

    @apigen.command()
    def pubsub_publish(self, topic, event):
        """Publish an event on the network for a given topic."""
        raise NotImplementedError()  # TODO implement

    @apigen.command()
    def pubsub_subscribe(self, topic):
        """Subscribe to events for given topic."""
        raise NotImplementedError()  # TODO implement

    @apigen.command()
    def pubsub_subscriptions(self):
        """List current subscriptions."""
        raise NotImplementedError()  # TODO implement
        # TODO return topics

    @apigen.command()
    def pubsub_unsubscribe(self, topic):
        """Unsubscribe from events for given topic."""
        raise NotImplementedError()  # TODO implement

    @apigen.command()
    def pubsub_events(self, topic):
        """Events received for topic since last called."""
        raise NotImplementedError()  # TODO implement
        # TODO return events

    @apigen.command()
    def message_send(self, nodeid, message):
        """Send a direct message to a known node."""
        raise NotImplementedError()  # TODO implement
        # TODO return bool

    @apigen.command()
    def message_list(self):
        """Messages received since last called (in order)."""
        results = defaultdict(lambda: [])
        while not self._protocol.messages.empty():
            nodeid, message = self._protocol.messages.get()
            results[binascii.hexlify(nodeid)].append(message)
        return results

    @apigen.command()
    def stream_list(self):
        """List currently open streams and unread bytes."""
        raise NotImplementedError()  # TODO implement
        # TODO return {streamid: buf_len}

    @apigen.command()
    def stream_open(self, nodeid):
        """Open a datastream with a node."""
        raise NotImplementedError()  # TODO implement
        # TODO return streamid

    @apigen.command()
    def stream_close(self, streamid):
        """Close a datastream with a node."""
        raise NotImplementedError()  # TODO implement

    @apigen.command()
    def stream_read(self, streamid, size):
        """Read from a datastream with a node."""
        raise NotImplementedError()  # TODO implement
        # TODO return data

    @apigen.command()
    def stream_write(self, streamid, data):
        """Write to a datastream with a node."""
        raise NotImplementedError()  # TODO implement

#    def stop(self):
#        raise NotImplementedError()  # TODO implement
#
#    def on_shutdown(self):
#        self.stop()


if __name__ == "__main__":
    apigen.run(Storjnet)
