from io import BytesIO


# Source: http://stackoverflow.com/a/10917767/90351


class FifoBuffer(object):

    def __init__(self, buffer_limit=None):
        self.buffer_limit = buffer_limit
        self.buf = BytesIO()
        self.available = 0    # Bytes available for reading
        self.size = 0
        self.write_fp = 0

    def read(self, size=None):
        """Reads size bytes from buffer"""
        if size is None or size > self.available:
            size = self.available
        size = max(size, 0)

        result = self.buf.read(size)
        self.available -= size

        if len(result) < size:
            self.buf.seek(0)
            result += self.buf.read(size - len(result))

        return result

    def write(self, data):
        """Appends data to buffer"""
        available_before = self.available

        # trim data if limit expected
        has_limit = self.buffer_limit is not None
        if has_limit and ((len(data) + self.available) > self.buffer_limit):
            data = data[:self.buffer_limit - self.available]

        if self.size < self.available + len(data):
            # Expand buffer
            new_buf = BytesIO()
            new_buf.write(self.read())
            self.write_fp = self.available = new_buf.tell()
            read_fp = 0
            while self.size <= self.available + len(data):
                self.size = max(self.size, 1024) * 2
            new_buf.write('0' * (self.size - self.write_fp))
            self.buf = new_buf
        else:
            read_fp = self.buf.tell()

        self.buf.seek(self.write_fp)
        written = self.size - self.write_fp
        self.buf.write(data[:written])
        self.write_fp += len(data)
        self.available += len(data)
        if written < len(data):
            self.write_fp -= self.size
            self.buf.seek(0)
            self.buf.write(data[written:])
        self.buf.seek(read_fp)

        return self.available - available_before
