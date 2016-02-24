import apigen
import random
import binascii
import btctxstore
import crochet
from twisted.internet import defer
from storjkademlia.crawling import NodeSpiderCrawl
from collections import defaultdict
from . protocol import Protocol
from pycoin.encoding import a2b_hashed_base58
from storjkademlia.storage import ForgetfulStorage
from storjkademlia.node import Node
from storjkademlia.network import Server
from pyp2p.lib import get_unused_port
from . version import __version__  # NOQA


class StorjNet(apigen.Definition):

    def __init__(self, node_key=None, node_port=None, bootstrap=None,
                 networkid="mainnet", call_timeout=120,
                 limit_send_sec=None, limit_receive_sec=None,
                 limit_send_month=None, limit_receive_month=None,
                 quiet=False, debug=False, verbose=False, noisy=False):

        self._log = None  # TODO get logger
        self._call_timeout = call_timeout
        self._setup_node(node_key)
        self._setup_protocol()
        self._setup_kademlia(bootstrap, node_port)
        # TODO setup quasar
        # TODO setup messaging
        # TODO setup streams

    def _setup_node(self, node_key):
        self._btctxstore = btctxstore.BtcTxStore()
        node_key = node_key or self._btctxstore.create_key()
        is_hwif = self._btctxstore.validate_wallet(node_key)
        self._key = self._btctxstore.get_key(node_key) if is_hwif else node_key
        address = self._btctxstore.get_address(self._key)
        self._nodeid = a2b_hashed_base58(address)[1:]

    def _setup_protocol(self):
        storage = ForgetfulStorage()
        self._protocol = Protocol(Node(self._nodeid), storage, ksize=20,
                                  max_messages=1024)
        # TODO set rpc logger

    def _setup_kademlia(self, bootstrap, node_port):

        # ensure transport address is a tuple
        if bootstrap is not None:
            bootstrap = [(addr[0], addr[1]) for addr in bootstrap]

        self._port = node_port or get_unused_port()
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

    def dht_find_async(self, nodeid):
        nodeid = binascii.unhexlify(nodeid)

        # stun if own id given
        if nodeid == self._nodeid:
            neighbors = self._protocol.get_neighbors()
            neighbor = random.choice(neighbors)
            return self._protocol.stun((neighbor.ip, neighbor.port))

        # crawl to find nearest to target nodeid
        node = Node(nodeid)
        nearest = self._protocol.router.findNeighbors(node)
        if len(nearest) == 0:
            return defer.succeed(None)
        spider = NodeSpiderCrawl(self._protocol, node, nearest,
                                 self._kademlia.ksize, self._kademlia.alpha)
        d = spider.find()

        # filter requested node
        def func(nodes):
            for node in nodes:
                if node.id == nodeid:
                    return [node.ip, node.port]
            return None
        d.addCallback(func)
        return d

    @apigen.command()
    def dht_find(self, nodeid):
        """Get [ip, port] if online, call with own id to stun."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.dht_find_async(nodeid)
        return func()

    @apigen.command()
    def dht_id(self):
        """Get the id of this node."""
        return binascii.hexlify(self._nodeid)

    @apigen.command()
    def dht_peers(self):
        """List neighbors."""
        neighbors = []
        for neighbor in self._protocol.get_neighbors():
            neighbors.append([
                binascii.hexlify(neighbor.id), neighbor.ip, neighbor.port
            ])
        return neighbors

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
        return dict(results)

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

    def stop(self):
        pass  # no extra threads/services to stop ... yet

    def on_shutdown(self):
        self.stop()


if __name__ == "__main__":
    apigen.run(StorjNet)
