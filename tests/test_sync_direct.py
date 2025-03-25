import shutil
import tempfile
from pathlib import Path

from pysync.sync_direct.service_direct import sync


def test_exists_source_not_exists_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        content = "Я — очень полезный файл"
        (Path(source) / "my-file").write_text(content)
        sync(source, dest)
        expected_path = Path(dest) / "my-file"
        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_file_renamed():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        content = "Я — файл, который переименовали"
        source_path = Path(source) / "source-filename"
        old_dest_path = Path(dest) / "dest-filename"
        expected_dest_path = Path(dest) / "source-filename"
        source_path.write_text(content)
        old_dest_path.write_text(content)
        sync(source, dest)
        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
