import hashlib
import io

BLOCKSIZE = 65536

# Helpers


def hash_buffer(buff: io.BufferedReader) -> str:
    hasher = hashlib.sha1()
    buf = buff.read(BLOCKSIZE)
    while buf:
        hasher.update(buf)
        buf = buff.read(BLOCKSIZE)
    return hasher.hexdigest()
