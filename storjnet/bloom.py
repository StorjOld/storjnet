import json
from pybloom import BloomFilter
from base64 import b64encode, b64decode
from bitarray import bitarray
from struct import unpack, pack


def _bitarray_serialize(ba):
    return [ba.endian(), b64encode(ba.tobytes()), len(ba)]


def _bitarray_deserialize(data):
    ba = bitarray(endian=data[0])
    ba.frombytes(b64decode(data[1]))
    return ba[:data[2]]


def _bloomfilter_serialize(bf):
    return [
        b64encode(pack(bf.FILE_FMT, bf.error_rate, bf.num_slices,
                       bf.bits_per_slice, bf.capacity, bf.count)),
        _bitarray_serialize(bf.bitarray)
    ]


def _bloomfilter_deserialize(data):
    bf = BloomFilter(1)  # Bogus instantiation, we will `_setup'.
    bf._setup(*unpack(BloomFilter.FILE_FMT, b64decode(data[0])))
    bf.bitarray = _bitarray_deserialize(data[1])
    return bf


def abf_empty(size, depth):
    """Create empty attenuated bloom filter."""
    return [BloomFilter(capacity=size, error_rate=0.001) for i in range(depth)]


def abf_serialize(filters):
    """Serialize an attenuated bloom filter."""
    return json.dumps([_bloomfilter_serialize(bf) for bf in filters])


def abf_deserialize(serialized_filters):
    """Deserialize an attenuated bloom filter."""
    return [
        _bloomfilter_deserialize(bf) for bf in json.loads(serialized_filters)
    ]
