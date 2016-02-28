import time
import hashlib
import umsgpack
import random
try:
    from Queue import Queue, Full  # py2
except ImportError:
    from queue import Queue, Full  # py3
from pybloof import StringBloomFilter
from collections import defaultdict
from twisted.internet.task import LoopingCall


SIZE = 512  # default from quasar paper section 4, first paragraph
DEPTH = 3  # default from quasar paper section 4, first paragraph
TTL = 64
FRESHNESS = 30


# TODO Add limited propagations when own filters updated
#      (by subscribe/unscribe or peer filter update).
#      Only x updates per refresh cycle to prevent flooding,
#      this should prevent flooding while remaining responsive.


def abf_empty():
    """Create empty attenuated bloom filter."""
    return [StringBloomFilter(size=SIZE, hashes=1) for i in range(DEPTH)]


def abf_serialize(filters):
    """Serialize an attenuated bloom filter."""
    return [bf.to_base64() for bf in filters]


def abf_deserialize(self, b64_filters):
    """Deserialize an attenuated bloom filter."""
    return [StringBloomFilter.from_base64(b64_bf) for b64_bf in b64_filters]


class Quasar(object):

    def __init__(self, protocol, queue_limit=8192, history_limit=65536):
        self._protocol = protocol
        self._protocol.quasar = self
        self._subscriptions = set()
        self._filters = abf_empty()
        self._peers = defaultdict(
            lambda: {
                "timestamp": 0,
                "filters": abf_empty(),
            }
        )
        self._history = []
        self._history_limit = history_limit
        self._events = defaultdict(lambda: Queue(maxsize=queue_limit))
        self._refresh_loop = LoopingCall(self._refresh).start(FRESHNESS / 3)

    def subscribe(self, topic):
        self._subscriptions.add(topic)

    def unsubscribe(self, topic):
        self._subscriptions.remove(topic)

    def subscriptions(self):
        return self._subscriptions.copy()

    def events(self, topic):
        results = []
        while not self._events[topic].empty():
            results.append(self._events[topic].get())
        return results

    def _refresh(self):
        self._rebuild()
        self._cull()

    def _cull(self):
        """Remove quasar peers that are no longer overlay neighbors."""
        neighbors = [peer.id for peer in self._protocol.get_neighbors()]
        for peerid in self._peers.keys():
            if peerid not in neighbors:
                del self._peers[peerid]

    def _rebuild(self):
        """Algorithm 1 from the quasar paper."""
        t = self._protocol.quasar_freshness
        self._filters = abf_empty()

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
        b64_filters = abf_serialize(self._filters)
        for peer in self._protocol.get_neighbors():
            self._protocol.callQuasarUpdate(peer, b64_filters)

    def update(self, peer, b64_filters):
        """Update attenuated bloom filters for peer."""
        if peer in self._protocol.get_neighbors():
            filters = abf_deserialize(b64_filters)
            self._peers[peer.id]["timestamp"] = time.time()
            self._peers[peer.id]["filters"] = filters
            return True
        return False

    def _deliver(self, topic, event):
        try:
            self._events[topic].put_nowait(event)
            return True
        except Full:
            return False

    def _is_duplicate(self, event):
        digest = hashlib.sha256(umsgpack.packb(event)).digest()

        # check if event in history
        duplicate = digest in self._history

        # add to history if needed
        if not duplicate:
            self._history.append(digest)

        # cull history
        while len(self._history) > self._history_limit:
            self._history.pop(0)  # remove oldest first

        return duplicate

    def publish(self, topic, event, publishers=None, ttl=TTL):
        """Algorithm 2 from the quasar paper."""
        publishers = [] if publishers is None else publishers

        if self._is_duplicate(event):
            return
        nodeid = self._protocol.sourceNode.id
        if topic in self._subscriptions:
            self._deliver(topic, event)
            publishers.append(nodeid)
            for peer in self._protocol.get_neighbors():
                self._protocol.callQuasarNotify(peer, topic, event,
                                                publishers, ttl)
            return
        ttl -= 1
        if ttl == 0:
            return
        for i in range(DEPTH):
            for peer in self._protocol.get_neighbors():
                peer_abf = self._peers[peer.id]["filters"]
                if topic in peer_abf[i]:
                    negrt = False
                    for publisher in publishers:
                        if publisher in peer_abf[i]:
                            negrt = True
                    if not negrt:
                        self._protocol.callQuasarNotify(peer, topic, event,
                                                        publishers, ttl)
                        return
        peer = random.choice(self._protocol.get_neighbors())
        self._protocol.callQuasarNotify(peer, topic, event, publishers, ttl)
