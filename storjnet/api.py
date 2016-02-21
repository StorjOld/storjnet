import apigen
from . version import __version__  # NOQA


class Storjnet(apigen.Definition):

    def __init__(self, key, networkid=None, port=None, bootstrap=None,
                 limit_send_sec=None, limit_receive_sec=None,
                 limit_send_month=None, limit_receive_month=None,
                 quiet=False, debug=False, verbose=False, noisy=False):
        pass

    @apigen.command()
    def dht_put(self, key, value):
        """Store key/value pair in DHT."""
        raise NotImplementedError()  # TODO implement
        # TODO return bool

    @apigen.command()
    def dht_get(self, key):
        """Get value for given key in DHT."""
        raise NotImplementedError()  # TODO implement
        # TODO return value

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
        raise NotImplementedError()  # TODO implement
        # TODO return {nodeid: [message]}

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


if __name__ == "__main__":
    apigen.run(Storjnet)
