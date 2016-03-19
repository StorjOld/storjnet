import os
import time
import apigen
import threading
import random
import binascii
import btctxstore
import crochet
from twisted.internet import defer
from storjkademlia.crawling import NodeSpiderCrawl
from collections import defaultdict
from pycoin.encoding import a2b_hashed_base58
from storjkademlia.storage import ForgetfulStorage
from storjkademlia.node import Node
from storjkademlia.network import Server
from pyp2p.lib import get_unused_port
from . quasar import Quasar
from . protocol import Protocol
from . version import __version__  # NOQA


# TODO add default bootstrap nodes


class StorjNet(apigen.Definition):

    def __init__(self, node_key=None, node_port=None, bootstrap=None,
                 networkid="mainnet", call_timeout=120,
                 limit_send_sec=None, limit_receive_sec=None,
                 limit_send_month=None, limit_receive_month=None,
                 queue_limit=8192, history_limit=65536,
                 quiet=False, debug=False, verbose=False, noisy=False):
        # FIXME add host interface to listen
        # TODO sanatize input
        # TODO add doc string

        self._log = None  # TODO get logger
        self._call_timeout = call_timeout
        self._setup_node(node_key)
        self._setup_protocol(noisy, queue_limit)
        self._setup_kademlia(bootstrap, node_port)
        self._setup_quasar(queue_limit, history_limit)
        # TODO setup streams

    def _setup_node(self, node_key):
        self._btctxstore = btctxstore.BtcTxStore()
        node_key = node_key or self._btctxstore.create_key()
        is_hwif = self._btctxstore.validate_wallet(node_key)
        self._key = self._btctxstore.get_key(node_key) if is_hwif else node_key
        address = self._btctxstore.get_address(self._key)
        self._nodeid = a2b_hashed_base58(address)[1:]

    def _setup_protocol(self, noisy, queue_limit):
        storage = ForgetfulStorage()
        self._protocol = Protocol(Node(self._nodeid), storage, noisy=noisy,
                                  queue_limit=queue_limit)
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

    def _setup_quasar(self, queue_limit, history_limit):
        self._quasar = Quasar(self._protocol, queue_limit=queue_limit,
                              history_limit=history_limit)

    def dht_put_async(self, key, value):
        """Store key/value pair in DHT."""
        # TODO sanatize input
        return self._kademlia.set(key, value)

    @apigen.command()
    def dht_put(self, key, value):
        """Store key/value pair in DHT."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.dht_put_async(key, value)
        return func()

    def dht_get_async(self, key):
        """Get value for given key in DHT."""
        # TODO sanatize input
        return self._kademlia.get(key)

    @apigen.command()
    def dht_get(self, key):
        """Get value for given key in DHT."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.dht_get_async(key)
        return func()

    def dht_stun_async(self):
        """Stun random neighbor to see own wan ip/port."""
        # TODO cache result
        hexid, ip, port = random.choice(self.dht_peers())
        d = self._protocol.stun((ip, port))

        def func(result):
            if result[0]:
                return result[1]
            return None
        d.addCallback(func)
        return d

    @apigen.command()
    def dht_stun(self):
        """Stun random neighbor to see own wan ip/port."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.dht_stun_async()
        return func()

    def dht_find_async(self, hexnodeid):
        """Get [ip, port] if online, call with own id to stun."""
        # TODO cache results
        # TODO sanatize input
        nodeid = binascii.unhexlify(hexnodeid)

        # stun if own id given
        if nodeid == self._nodeid:
            return self.dht_stun_async()

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
    def dht_find(self, hexnodeid):
        """Get [ip, port] if online, call with own id to stun."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.dht_find_async(hexnodeid)
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
        # TODO sanatize input
        # TODO use envelope { timestamp, sender, body, signature } ?
        self._quasar.publish(topic, event)

    @apigen.command()
    def pubsub_subscribe(self, topic):
        """Subscribe to events for given topic."""
        # TODO sanatize input
        self._quasar.subscribe(topic)

    @apigen.command()
    def pubsub_subscriptions(self):
        """List current subscriptions."""
        return list(self._quasar.subscriptions())

    @apigen.command()
    def pubsub_unsubscribe(self, topic):
        """Unsubscribe from events for given topic."""
        # TODO sanatize input
        self._quasar.unsubscribe(topic)

    @apigen.command()
    def pubsub_events(self, topic):
        """Events received for topic since last called."""
        # TODO sanatize input
        return self._quasar.events(topic)

    def message_send_async(self, hexnodeid, message):
        """Send a direct message to a known node."""
        # TODO sanatize input
        d = self.dht_find_async(hexnodeid)

        def func(result):
            if result is None:
                return False
            ip, port = result
            node = Node(binascii.unhexlify(hexnodeid), ip, port)
            return self._protocol.callMessageNotify(node, message)
        d.addCallback(func)
        return d

    @apigen.command()
    def message_send(self, hexnodeid, message):
        """Send a direct message to a known node."""

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.message_send_async(hexnodeid, message)
        return func()

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
    def stream_open(self, hexnodeid):
        """Open a datastream with a node."""
        # TODO sanatize input
        raise NotImplementedError()  # TODO implement
        # TODO return streamid

    @apigen.command()
    def stream_close(self, streamid):
        """Close a datastream with a node."""
        # TODO sanatize input
        raise NotImplementedError()  # TODO implement

    @apigen.command()
    def stream_read(self, streamid, size):
        """Read from a datastream with a node."""
        # TODO sanatize input
        raise NotImplementedError()  # TODO implement
        # TODO return data

    @apigen.command()
    def stream_write(self, streamid, data):
        """Write to a datastream with a node."""
        # TODO sanatize input
        raise NotImplementedError()  # TODO implement

    def stop(self):
        pass  # no extra threads/services to stop ... yet

    def on_shutdown(self):
        self.stop()


def start_swarm(size=64, isolate=True, start_user_rpc_server=True,
                net_host="127.0.0.1", rpc_host="127.0.0.1",
                net_start_port=20000, rpc_start_port=30000,
                **kwargs):
    nodes = []
    try:

        # setup bootstrap nodes
        if isolate:
            networkid = binascii.hexlify(os.urandom(32))
            bootstrap = [[net_host, net_start_port + i] for i in range(size)]

        for i in range(size):

            # create storjnet node
            node_kwargs = kwargs.copy()
            node_kwargs["node_key"] = None  # always generate
            node_kwargs["node_port"] = net_start_port + i
            if isolate:
                node_kwargs["bootstrap"] = bootstrap
                node_kwargs["networkid"] = networkid

            storjnet = StorjNet(**node_kwargs)

            # run in own thread
            thread = None
            if start_user_rpc_server:
                thread = threading.Thread(
                    target=storjnet.startserver,
                    kwargs={
                        "hostname": rpc_host,
                        "port": rpc_start_port + i,
                        "handle_sigint": False
                    }
                )
                thread.start()

            nodes.append([storjnet, thread])
        return nodes
    except:
        stop_swarm(nodes)
        raise


def stop_swarm(nodes):
    for storjnet, thread in nodes:
        storjnet.stop()
        if thread is not None:
            storjnet.stopserver()
            thread.join()


def run_swarm(**kwargs):
    swarm = start_swarm(**kwargs)

    # server until killed
    try:
        while True:
            time.sleep(1)

    # expected exit mode
    except KeyboardInterrupt:
        pass

    finally:
        stop_swarm(swarm)


if __name__ == "__main__":
    apigen.run(StorjNet)
