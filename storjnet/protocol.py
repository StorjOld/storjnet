try:
    from Queue import Queue, Full  # py2
except ImportError:
    from queue import Queue, Full  # py3
from storjkademlia.node import Node
from storjkademlia.protocol import KademliaProtocol


class Protocol(KademliaProtocol):

    def __init__(self, *args, **kwargs):

        # pop storjnet protocol args
        self.noisy = kwargs.pop("noisy", False)
        queue_limit = kwargs.pop("queue_limit", 8192)

        # cant use super due to introspection?
        KademliaProtocol.__init__(self, *args, **kwargs)

        self.messages = Queue(maxsize=queue_limit)
        self.quasar = None

    def get_neighbors(self):
        return self.router.findNeighbors(self.router.node,
                                         exclude=self.router.node)

    def rpc_quasar_filters(self, sender, nodeid):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        assert(self.quasar is not None)
        return self.quasar.filters()

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
        return self.quasar.publish(topic, event, publishers=publishers, ttl=ttl)

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

    def rpc_stream_open(self, sender, nodeid):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        # TODO implement
        return None  # TODO return streamid

    def rpc_stream_close(self, sender, nodeid, streamid):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        # TODO implement
        return True

    def rpc_stream_write(self, sender, nodeid, streamid, data):
        # TODO sanatize input
        source = Node(nodeid, sender[0], sender[1])
        self.welcomeIfNewNode(source)
        # TODO implement
        return 0  # TODO return bytes written

    def callQuasarFilters(self, nodeToAsk):
        address = (nodeToAsk.ip, nodeToAsk.port)
        d = self.quasar_filters(address, self.sourceNode.id)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d

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
        d = self.stream_close(address, self.sourceNode.id, streamid, data)
        d.addCallback(self.handleCallResponse, nodeToAsk)
        d.addErrback(self.onError)
        return d
