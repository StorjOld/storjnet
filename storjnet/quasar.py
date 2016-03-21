import os
import time
import hashlib
import umsgpack
import random
import threading
try:
    from Queue import Queue, Full  # py2
except ImportError:
    from queue import Queue, Full  # py3
from collections import defaultdict
from twisted.internet.task import LoopingCall
from . import bloom


# Implementation of the Quasar Publish/Subscribe system.
# http://www.cs.toronto.edu/iptps2008/final/70.pdf


# TODO make sure all calls are always run in the twisted reactor


SIZE = 512  # default from quasar paper section 4, first paragraph
DEPTH = 3  # default from quasar paper section 4, first paragraph
TTL = 64
FRESHNESS = 660  # time after unupdated peer filters become stale (11min)
REFRESH_TIME = 600  # interval when own filters are propagated to peers (10min)
EXTRA_PROPAGATIONS = 300  # number of propagation allowed between refreshes


_STATS_LOG = bool(os.environ.get("STORJNET_QUASAR_LOG_STATS", False))
_STATS_DATA = {
    "update_called": 0,
    "update_successful": 0,
    "update_redundant": 0,
    "update_spam": 0,
}
_STATS_LOCK = threading.RLock()


def _stats_increment(key):
    if _STATS_LOG:
        with _STATS_LOCK:
            _STATS_DATA[key] = _STATS_DATA[key] + 1


def _stats_log_constants():
    if _STATS_LOG:
        with _STATS_LOCK:
            _STATS_DATA["constants"] = {
                "size": SIZE, "depth": DEPTH, "ttl": TTL,
                "freshness": FRESHNESS, "refresh_time": REFRESH_TIME,
                "extra_propagations": EXTRA_PROPAGATIONS
            }


class Quasar(object):

    def __init__(self, protocol, queue_limit=8192, history_limit=65536):
        _stats_log_constants()
        self._protocol = protocol
        self._protocol.quasar = self
        self._extra_propagations = EXTRA_PROPAGATIONS
        self._subscriptions = set()
        self._filters = bloom.abf_empty(SIZE, DEPTH)
        self._peers = defaultdict(
            lambda: {"timestamp": 0, "filters": bloom.abf_empty(SIZE, DEPTH)}
        )
        self._history = []  # TODO use pypi.python.org/pypi/fuggetaboutit ?
        self._history_limit = history_limit
        self._events = defaultdict(lambda: Queue(maxsize=queue_limit))
        self._refresh_loop = LoopingCall(self._refresh).start(REFRESH_TIME)

    def subscribe(self, topic):
        self._subscriptions.add(topic)
        self._rebuild()

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
        self._rebuild(is_refresh=True)
        self._cull()

    def _cull(self):
        """Remove quasar peers that are no longer overlay neighbors."""
        neighbors = [peer.id for peer in self._protocol.get_neighbors()]
        for peerid in self._peers.keys():
            if peerid not in neighbors:
                del self._peers[peerid]

    def _rebuild(self, is_refresh=False):
        """Algorithm 1 from the quasar paper.

        Args:
            is_refresh: Force propagate and reset extra propagations.

        Returns:
            True if filters updated.
        """
        serialized_before = bloom.abf_serialize(self._filters)
        self._filters = bloom.abf_empty(SIZE, DEPTH)

        # create home attenuated bloom filter from own subscriptions
        for subscription in self._subscriptions:
            self._filters[0].add(subscription)
            # TODO break spect and add to all filters, prevent cascade?

        # join peer filters
        for peer in self._protocol.get_neighbors():
            if self._peers[peer.id]["timestamp"] < time.time() - FRESHNESS:
                continue  # ignore stale peer filters
            peer_abf = self._peers[peer.id]["filters"]
            for i in range(1, DEPTH):
                self._filters[i] = self._filters[i].union(peer_abf[i-1])

        # send updated filter to peers if changed or forced propagate
        serialized_filters = bloom.abf_serialize(self._filters)
        filters_updated = serialized_filters != serialized_before
        if is_refresh or (self._extra_propagations > 0 and filters_updated):
            for peer in self._protocol.get_neighbors():
                self._protocol.callQuasarUpdate(peer, serialized_filters)
            if is_refresh:
                self._extra_propagations = EXTRA_PROPAGATIONS
            else:
                self._extra_propagations -= 1
        return filters_updated

    def update(self, peer, serialized_filters):
        """Update attenuated bloom filters for peer.

        Returns:
            True if filters updated.
        """
        _stats_increment("update_called")
        peerids = [p.id for p in self._protocol.get_neighbors()]
        if peer.id in peerids:
            filters = bloom.abf_deserialize(serialized_filters)
            self._peers[peer.id]["timestamp"] = time.time()
            self._peers[peer.id]["filters"] = filters
            updated = self._rebuild()
            if updated:
                _stats_increment("update_successful")
            else:
                _stats_increment("update_redundant")
            return updated
        else:
            _stats_increment("update_spam")
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

    def publish(self, topic, event, publishers=None, ttl=None):
        """Algorithm 2 from the quasar paper."""
        ttl = ttl or TTL
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
