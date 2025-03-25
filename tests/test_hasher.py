import io
import tempfile
from pathlib import Path

from pysync.helpers import hash_buffer


def test_hash_buffer():
    buffer = io.BytesIO(b"blablalba")
    result = hash_buffer(buffer)
    assert result == "e64b9663c98b58514312b14555dbb266c17a80e3"


def test_hash_file() -> None:
    source = tempfile.mkdtemp()

    source_path = Path(source) / "source-filename"
    source_path.write_text("This is awesome text")

    with source_path.open("rb") as f:
        result = hash_buffer(f)
    assert result == "912305f803c64035459c33cf74de8ff5395aa7f1"
