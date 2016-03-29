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
from . import quasar
from . import protocol
from . version import __version__  # NOQA


# TODO add default bootstrap nodes


class StorjNet(apigen.Definition):

    def __init__(self,

                 # network options
                 node_key=None, node_port=None, bootstrap=None,
                 networkid="mainnet", rpc_call_timeout=120,

                 # bandwidth limits
                 limit_send_sec=None, limit_receive_sec=None,
                 limit_send_month=None, limit_receive_month=None,

                 # messaging options
                 message_queue_limit=protocol.MESSAGE_QUEUE_LIMIT,

                 # stream options
                 stream_max_count=protocol.STREAM_MAX_COUNT,
                 stream_buffer_limit=protocol.STREAM_BUFFER_LIMIT,

                 # quasar options
                 quasar_queue_limit=quasar.QUEUE_LIMIT,
                 quasar_history_limit=quasar.HISTORY_LIMIT,
                 quasar_size=quasar.SIZE, quasar_depth=quasar.DEPTH,
                 quasar_ttl=quasar.TTL, quasar_freshness=quasar.FRESHNESS,
                 quasar_refresh_time=quasar.REFRESH_TIME,
                 quasar_extra_propagations=quasar.EXTRA_PROPAGATIONS,
                 quasar_pull_filters=quasar.PULL_FILTERS,

                 # logging options
                 log_statistics=False, quiet=False,
                 debug=False, verbose=False, noisy=False):

        # FIXME add host interface for network interface to listen on
        # TODO sanatize input
        # TODO add doc string

        self._log_stats = log_statistics
        self._call_timeout = rpc_call_timeout
        self._setup_node(node_key)
        self._setup_protocol(noisy, message_queue_limit,
                             stream_max_count, stream_buffer_limit)
        self._setup_kademlia(bootstrap, node_port)
        self._setup_quasar(
            quasar_queue_limit, quasar_history_limit, quasar_size,
            quasar_depth, quasar_ttl, quasar_freshness, quasar_refresh_time,
            quasar_extra_propagations, quasar_pull_filters, log_statistics
        )
        # TODO setup streams

    def _setup_node(self, node_key):
        self._btctxstore = btctxstore.BtcTxStore()
        node_key = node_key or self._btctxstore.create_key()
        is_hwif = self._btctxstore.validate_wallet(node_key)
        self._key = self._btctxstore.get_key(node_key) if is_hwif else node_key
        address = self._btctxstore.get_address(self._key)
        self._nodeid = a2b_hashed_base58(address)[1:]

    def _setup_protocol(self, noisy, message_queue_limit,
                        stream_max_count, stream_buffer_limit):
        storage = ForgetfulStorage()
        self._protocol = protocol.Protocol(
            Node(self._nodeid), storage, noisy=noisy,
            message_queue_limit=message_queue_limit,
            stream_max_count=stream_max_count,
            stream_buffer_limit=stream_buffer_limit
        )
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

    def _setup_quasar(self, queue_limit, history_limit, size, depth, ttl,
                      freshness, refresh_time, extra_propagations,
                      pull_filters, log_statistics):
        self._quasar = quasar.Quasar(
            self._protocol, queue_limit=queue_limit,
            history_limit=history_limit, size=size, depth=depth, ttl=ttl,
            freshness=freshness, refresh_time=refresh_time,
            extra_propagations=extra_propagations,
            log_statistics=log_statistics, pull_filters=pull_filters
        )

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
        result = {}
        for streamid, stream in self._protocol.streams.items():
            peer = stream["peer"]
            result[binascii.hexlify(streamid)] = [
                binascii.hexlify(peer.id),
                0  # TODO add buffer size
            ]
        return result

    def stream_open_async(self, hexnodeid):

        def open_remote_buffer(result):
            if result is None:
                return None  # failed to find node

            ip, port = result
            node = Node(binascii.unhexlify(hexnodeid), ip, port)

            def open_local_buffer(result):
                success, streamid = result
                if not success:
                    return None  # failed to open remote buffer

                # open local buffer
                if self._protocol.stream_init(streamid, node) is None:

                    # opening local buffer failed
                    # close remote buffer to be nice, fire and forget
                    self._protocol.callStreamClose(node, streamid)
                    return None
                else:
                    return binascii.hexlify(streamid)

            d = self._protocol.callStreamOpen(node)
            return d.addCallback(open_local_buffer)

        d = self.dht_find_async(hexnodeid)
        d.addCallback(open_remote_buffer)
        return d

    @apigen.command()
    def stream_open(self, hexnodeid):
        """Open a datastream with a node.

        Returns: hexstreamid or None
        """
        # TODO sanatize input

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.stream_open_async(hexnodeid)
        return func()

    def stream_close_async(self, hexstreamid):
        streamid = binascii.unhexlify(hexstreamid)
        if streamid not in self._protocol.streams:
            return False  # already closed

        node = self._protocol.streams[streamid]["peer"]

        # close local buffer
        del self._protocol.streams[streamid]

        # close remote buffer
        return self._protocol.callStreamClose(node, streamid)

    @apigen.command()
    def stream_close(self, hexstreamid):
        """Close a datastream with a node.

        Returns: True if close confirmed on both sides of the connection.
        """
        # TODO sanatize input

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.stream_close_async(hexstreamid)
        return func()

    def stream_read_bin(self, streamid, size=None):
        if streamid not in self._protocol.streams:
            return None
        return self._protocol.streams[streamid]["buffer"].read(size)

    @apigen.command()
    def stream_read(self, hexstreamid, size=None):
        """Read from a datastream with a node."""
        # TODO sanatize input
        streamid = binascii.unhexlify(hexstreamid)
        data = self.stream_read_bin(streamid, size=size)
        if data is None:
            return data
        return binascii.hexlify(data)

    def stream_write_bin_async(self, streamid, data):
        if streamid not in self._protocol.streams:
            return None
        node = self._protocol.streams[streamid]["peer"]
        d = self._protocol.callStreamWrite(node, streamid, data)

        def callback(result):
            success, written = result
            if success:
                return written
            else:
                return None
        d.addCallback(callback)
        return d

    def stream_write_bin(self, streamid, data):

        @crochet.wait_for(timeout=self._call_timeout)
        def func():
            return self.stream_write_bin_async(streamid, data)
        return func()

    @apigen.command()
    def stream_write(self, hexstreamid, hexdata):
        """Write to a datastream with a node."""
        # TODO sanatize input
        streamid = binascii.unhexlify(hexstreamid)
        data = binascii.unhexlify(hexdata)
        return self.stream_write_bin(streamid, data)

    def stats(self):
        if self._log_stats:
            return {
                "quasar": self._quasar.stats()
            }
        return None

    def stop(self):
        # no extra threads/services to stop ... yet
        return self.stats()

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

            # run user rpc interface in own thread
            user_rpc_thread = None
            if start_user_rpc_server:
                user_rpc_thread = threading.Thread(
                    target=storjnet.startserver,
                    kwargs={
                        "hostname": rpc_host,
                        "port": rpc_start_port + i,
                        "handle_sigint": False
                    }
                )
                user_rpc_thread.start()

            nodes.append([storjnet, user_rpc_thread])
        return nodes
    except:
        stop_swarm(nodes)
        raise


def stop_swarm(nodes):
    stats = []
    for storjnet, user_rpc_thread in nodes:
        stats.append(storjnet.stop())
        if user_rpc_thread is not None:
            storjnet.stopserver()
            user_rpc_thread.join()
    return stats


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
