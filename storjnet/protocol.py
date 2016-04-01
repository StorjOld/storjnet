try:
    from Queue import Queue, Full  # py2
except ImportError:
    from queue import Queue, Full  # py3
import os
from fifobuffer import FifoBuffer
from storjkademlia.node import Node
from storjkademlia.protocol import KademliaProtocol


MESSAGE_QUEUE_LIMIT = 8192
STREAM_MAX_COUNT = 512
STREAM_BUFFER_LIMIT = 1024 ** 2


class Protocol(KademliaProtocol):

    def __init__(self, *args, **kwargs):

        # pop storjnet protocol args
        self.noisy = kwargs.pop("noisy", False)
        self.message_queue_limit = kwargs.pop("message_queue_limit",
                                              MESSAGE_QUEUE_LIMIT)
        self.stream_max_count = kwargs.pop("stream_max_count",
                                           STREAM_MAX_COUNT)
        self.stream_buffer_limit = kwargs.pop("stream_buffer_limit",
                                              STREAM_BUFFER_LIMIT)

        # cant use super due to introspection?
        KademliaProtocol.__init__(self, *args, **kwargs)

        # FIXME use defaultdict with queue per nodeid
        self.messages = Queue(maxsize=self.message_queue_limit)

        # local streams
        self.streams = {}  # {streamid: {"peer": Node, "buffer": FifoBuffer}}

        self.quasar = None

    def get_neighbors(self):
        return self.router.findNeighbors(self.router.node,
                                         exclude=self.router.node)

    def rpc_quasar_update(self, sender, nodeid, filters):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        assert(self.quasar is not None)
        return self.quasar.update(source, filters)

    def rpc_quasar_notify(self, sender, nodeid, topic, event, publishers, ttl):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        assert(self.quasar is not None)
        return self.quasar.publish(topic, event,
                                   publishers=publishers, ttl=ttl)

    def rpc_message_notify(self, sender, nodeid, message):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        try:
            self.messages.put_nowait((nodeid, message))
            return True
        except Full:
            msg = "Message queue full, dropping message from %s"
            self.log.warning(msg % source)
            return False

    def stream_init(self, streamid, peer):

        # max open streams reached
        if len(self.streams) >= self.stream_max_count:
            return None

        # init buffer
        self.streams[streamid] = {
            "peer": peer,
            "buffer": FifoBuffer(buffer_limit=self.stream_buffer_limit)
        }
        return streamid

    def rpc_stream_open(self, sender, nodeid):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        streamid = os.urandom(32)
        return self.stream_init(streamid, source)

    def _can_manipulate_stream(self, streamid, source):

        # stream is not open
        if streamid not in self.streams:
            return False

        # is stream peer
        peer = self.streams[streamid]["peer"]
        return (
            peer.id == source.id and
            peer.port == source.port and
            peer.ip == source.ip
        )

    def rpc_stream_close(self, sender, nodeid, streamid):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        if not self._can_manipulate_stream(streamid, source):
            return False

        # close stream
        del self.streams[streamid]
        return True

    def rpc_stream_write(self, sender, nodeid, streamid, data):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        if not self._can_manipulate_stream(streamid, source):
            return None

        # write to buffer
        return self.streams[streamid]["buffer"].write(data)

    def callQuasarUpdate(self, nodeToAsk, b64_filters):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.quasar_update(address, self.sourceNode.id, b64_filters)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

    def callQuasarNotify(self, nodeToAsk, topic, event, publishers, ttl):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.quasar_notify(address, self.sourceNode.id,
                               topic, event, publishers, ttl)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

    def callMessageNotify(self, nodeToAsk, message):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.message_notify(address, self.sourceNode.id, message)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

    def callStreamOpen(self, nodeToAsk):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.stream_open(address, self.sourceNode.id)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

    def callStreamClose(self, nodeToAsk, streamid):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.stream_close(address, self.sourceNode.id, streamid)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

    def callStreamWrite(self, nodeToAsk, streamid, data):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.stream_write(address, self.sourceNode.id, streamid, data)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d
