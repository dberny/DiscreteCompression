import abc
import math


class Encoding(abc.ABC):

    @abc.abstractmethod
    def encode(self, content: bytes):
        pass

    @abc.abstractmethod
    def decode(self, content: bytes):
        pass


def test_encoding(encoding: Encoding, content: bytes):
    """Assert that a """
    enc = encoding.encode(content)
    dec = encoding.decode(enc)
    msg = f"Encode-Decode failed:\n\tOriginal: {content!r}\n\tEncoded: {enc!r}\n\tDecoded: {dec!r}"
    assert content == dec, msg
    return enc, dec


class RLEncoding(Encoding):
    """Run-Length Encoding
    >>> RLEncoding().encode(b'bbbbbb')
    b'6b'
    >>> RLEncoding().encode(b'a')
    b'a'
    >>> RLEncoding().encode(b'1')
    b'\\\\1'
    >>> RLEncoding().encode(b'\\\\')
    b'\\\\\\\\'
    >>> b'\\\\\\\\' == br'\\\\'
    True
    >>> rle = RLEncoding(b'a')
    >>> rle.encode(b'1')
    b'a1'
    >>> rle.encode(b'122333')
    b'a12a23a3'
    >>> rle.decode(b'a12a23a3')
    b'122333'
    """

    def __init__(self, escape: bytes = b"\\"):
        self.escape = escape

    def _escape_rule(self, char: int):
        return char == ord(self.escape) or (char >= ord(b'0') and char <= ord(b'9'))

    def _encode_gen(self, content: bytes):

        def escape_char(char: int):
            if char == ord(self.escape) or (char >= ord(b'0') and char <= ord(b'9')):
                yield ord(self.escape)
            yield char

        def num_to_bytes(num: int):
            if num >= 10:
                for c in num_to_bytes(num // 10):
                    yield c
            yield ord(b'0') + num % 10

        def yield_seq(char: int, length: int):
            if length <= 0:
                return
            if length > 1:
                for c in num_to_bytes(length):
                        yield c
            if self._escape_rule(char):
                for c in escape_char(char):
                    yield c
            else:
                yield char

        if len(content) == 0:
            return
        if len(content) == 1:
            for c in escape_char(content[0]):
                yield c
            return

        run = content[0]
        length = 1
        for char in content[1:]:
            if char != run:
                for c in yield_seq(run, length):
                    yield c
                run = char  # reset run
                length = 1
            else:
                length += 1
        for c in yield_seq(char, length):
            yield c

    def encode(self, content: bytes):
        return bytes(self._encode_gen(content))

    def _decode_gen(self, content: bytes):
        count = 0
        escaped = False
        for char in content:
            if not escaped:
                if char == ord(self.escape):
                    escaped = True
                    continue
                if char >= ord(b'0') and char <= ord(b'9'):
                    count = count*10 + (char - ord(b'0'))
                    continue
            if count > 0:
                for _ in range(count - 1):
                    yield char
                    continue
            if escaped and not self._escape_rule(char):
                raise ValueError("Unknown escaped character {!r}".format(chr(char)))
            yield char
            escaped = False
            count = 0
        if escaped:
            raise ValueError("Single escape character at end of sequence")
        if count > 0:
            raise ValueError("Length with no run at end of sequence")

    def decode(self, content: bytes):
        return bytes(self._decode_gen(content))
