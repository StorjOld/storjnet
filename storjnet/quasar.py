import time
try:
    from Queue import Queue, Full  # py2
except ImportError:
    from queue import Queue, Full  # py3
import binascii
from io import BytesIO
from pybloom import BloomFilter
from collections import defaultdict
from twisted.internet.task import LoopingCall


# defaults from quasar paper section 4, first paragraph
SIZE = 512
DEPTH = 3
FRESHNESS = 60
# TODO add limited propagations when filters updated


class Quasar(object):

    def __init__(self, protocol):
        self._protocol = protocol
        self._subscriptions = set()
        self._filters = self._empty_filters()
        self._peers = defaultdict(
            lambda: {
                "timestamp": 0,
                "filters": self._empty_filters(),
            }
        )
        self.quasar_events = defaultdict(
            lambda: Queue(maxsize=self.max_queue_size)
        )
        self._refresh_loop = LoopingCall(self._refresh).start(FRESHNESS / 3)

    def subscribe(self, topic):
        self._subscriptions.add(topic)

    def unsubscribe(self, topic):
        self._subscriptions.remove(topic)

    def subscriptions(self):
        return self._subscriptions.copy()

    def _refresh(self):
        self._rebuild(self)
        self._cull(self)

    def _empty_filters(self):
        """Create empty attenuated bloom filter."""
        return [BloomFilter(capacity=SIZE) for i in range(DEPTH)]

    def _serialize_filters(self, filters):
        bin_filters = []
        for abf in filters:
            bio = BytesIO()
            abf.tofile(bio)
            bio.seek(0)
            bin_filters.append(binascii.hexlify(bio.read()))
        return bin_filters

    def _deserialize_filters(self, bin_filters):
        filters = []
        for bin_abf in bin_filters:
            bio = BytesIO()
            bio.write(binascii.unhexlify(bin_abf))
            bio.seek(0)
            filters.append(BloomFilter.fromfile(bio))
        return filters

    def _cull(self):
        """Remove quasar peers that are no longer overlay neighbors."""
        neighbors = [peer.id for peer in self._protocol.get_neighbors()]
        for peerid in self._peers.keys():
            if peerid not in neighbors:
                del self._peers[peerid]

    def _rebuild(self):
        """ Algorithm 1 from the quasar paper."""
        t = self._protocol.quasar_freshness
        self._filters = self._empty_filters(SIZE, DEPTH)

        # create home attenuated bloom filter from own subscriptions
        for subscription in self._subscriptions:
            self._filters[0].add(subscription)

        # join peer filters
        for peer in self._protocol.get_neighbors():
            if self._peers[peer.id]["timestamp"] < time.time() - t:
                continue  # ignore stale peer filters
            peer_abf = self._peers[peer.id]["filters"]
            for i in range(1, DEPTH):
                self._filters[i] = self._filters[i].union(peer_abf[i-1])

        # send updated filter to peers
        hexfilters = self.serialize_filters(self._filters)
        for peer in self._protocol.get_neighbors():
            self._protocol.callQuasarUpdate(peer, hexfilters)

    def update(self, peer, hexfilters):
        """Update attenuated bloom filters for peer."""
        if peer in self._protocol.get_neighbors():
            filters = self.deserialize_filters(hexfilters)
            self._peers[peer.id]["timestamp"] = time.time()
            self._peers[peer.id]["filters"] = filters
            return True
        return False
