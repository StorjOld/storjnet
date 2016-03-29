import time
import copy
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
from twisted.internet import defer
from . import bloom


# Implementation of the Quasar Publish/Subscribe system.
# http://www.cs.toronto.edu/iptps2008/final/70.pdf


# TODO make sure all calls are always run in the twisted reactor


QUEUE_LIMIT = 8192
HISTORY_LIMIT = 65536
SIZE = 512
DEPTH = 3
TTL = 64
FRESHNESS = 660
REFRESH_TIME = 600
EXTRA_PROPAGATIONS = 300
PULL_FILTERS = False


class Quasar(object):

    def __init__(self, protocol, queue_limit=QUEUE_LIMIT,
                 history_limit=HISTORY_LIMIT, size=SIZE, depth=DEPTH, ttl=TTL,
                 freshness=FRESHNESS, refresh_time=REFRESH_TIME,
                 extra_propagations=EXTRA_PROPAGATIONS,
                 log_statistics=False):
        """
        Args:
            protocol: RPC object to make remote calls
            queue_limit: Received event limit per topic.
            history_limit: History limit, used to prevent duplicate events.
            size:  Bloom filter size.
            depth:  Attenuated bloom filter depth.
            ttl:
            freshness:  Time after unupdated peer filters become stale.
            refresh_time:  Interval when own filters are rebuilt
            extra_propagations:  Rebuilds allowed between refreshes.
        """

        # quasar setup
        self.size = size
        self.depth = depth
        self.ttl = ttl
        self.freshness = freshness
        self.refresh_time = refresh_time
        self.extra_propagations = extra_propagations

        # setup stats logging
        self._stats_log = log_statistics
        self._stats_lock = threading.RLock()
        self._stats_data = {
            "setup": {
                "size": self.size, "depth": self.depth, "ttl": self.ttl,
                "freshness": self.freshness, "refresh_time": self.refresh_time,
                "extra_propagations": self.extra_propagations
            },
            "update": {
                "called": 0, "successful": 0, "redundant": 0, "spam": 0,
            }
        }

        # link protocol interdependencie
        self._protocol = protocol
        self._protocol.quasar = self

        # quasar state
        self._remaining_propagations = self.extra_propagations
        self._subscriptions = set()
        self._filters = bloom.abf_empty(self.size, self.depth)
        self._peers = defaultdict(
            lambda: {
                "timestamp": 0,
                "filters": bloom.abf_empty(self.size, self.depth),
            }
        )

        # event queue per topic and history setup
        self._history = []
        self._history_limit = history_limit
        self._events = defaultdict(lambda: Queue(maxsize=queue_limit))

        # setup refresh loop
        self._refresh_loop = LoopingCall(self._refresh).start(refresh_time)

    def _stats_increment(self, call, effect):
        if self._stats_log:
            with self._stats_lock:
                self._stats_data[call][effect] += 1

    def stats(self):
        if self._stats_log:
            with self._stats_lock:
                return copy.deepcopy(self._stats_data)
        return None

    def subscribe(self, topic):
        self._subscriptions.add(topic)
        return self._rebuild()

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
        updated = self._rebuild(is_refresh=True)
        self._cull()
        return updated

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
        self._filters = bloom.abf_empty(self.size, self.depth)

        # create home attenuated bloom filter from own subscriptions
        for subscription in self._subscriptions:
            try:
                self._filters[0].add(subscription)
            except IndexError:
                pass  # BloomFilter is at capacity

        # join peer filters
        for peer in self._protocol.get_neighbors():
            peer_timestamp = self._peers[peer.id]["timestamp"]
            if peer_timestamp < time.time() - self.freshness:
                continue  # ignore stale peer filters
            peer_abf = self._peers[peer.id]["filters"]
            for i in range(1, self.depth):
                self._filters[i] = self._filters[i].union(peer_abf[i-1])

        serialized_filters = bloom.abf_serialize(self._filters)
        filters_updated = serialized_filters != serialized_before

        # reset remaining propagations and propagate if not pull filters
        if is_refresh:
            self._propagate_filters(serialized_filters)
            self._remaining_propagations = self.extra_propagations

        # send updated filter to peers if updated and remaining propagations
        elif self._remaining_propagations > 0 and filters_updated:
            self._propagate_filters(serialized_filters)
            self._remaining_propagations -= 1

        return filters_updated

    def _propagate_filters(self, serialized_filters):
        for peer in self._protocol.get_neighbors():
            self._protocol.callQuasarUpdate(peer, serialized_filters)

    def update(self, peer, serialized_filters, is_refresh=False):
        """Update attenuated bloom filters for peer.

        Returns:
            True if filters updated.
        """
        self._stats_increment("update", "called")
        peerids = [p.id for p in self._protocol.get_neighbors()]
        if peer.id in peerids:
            filters = bloom.abf_deserialize(serialized_filters)
            self._peers[peer.id]["timestamp"] = time.time()
            self._peers[peer.id]["filters"] = filters
            updated = self._rebuild(is_refresh=is_refresh)
            if updated:
                self._stats_increment("update", "successful")
            else:
                self._stats_increment("update", "redundant")
            return updated
        else:
            self._stats_increment("update", "spam")
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
        ttl = ttl or self.ttl
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
        for i in range(self.depth):
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
