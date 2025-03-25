import os
import shutil
from pathlib import Path

from .. import helpers


class SyncError(Exception):
    pass


class SourceNotExists(SyncError):
    pass


class DestinationNotExists(SyncError):
    pass


def sync(source: str, destination: str) -> None:
    if not os.path.exists(source):
        raise SourceNotExists()

    if not os.path.exists(destination):
        raise DestinationNotExists()

    source_data: dict[str, str] = {}

    for folder, _, files in os.walk(source):
        for fn in files:
            with (Path(folder) / fn).open("rb") as f:
                source_data[helpers.hash_buffer(f)] = fn

    already_presents: set[str] = set()

    for folder, _, files in os.walk(destination):
        for fn in files:
            dest_path = (Path(folder) / fn).resolve()
            with dest_path.open("rb") as f:
                dest_hash = helpers.hash_buffer(f)
            already_presents.add(dest_hash)

            if dest_hash not in source_data:
                os.remove(dest_path)
            elif dest_hash in source_data and fn != source_data[dest_hash]:
                shutil.move(dest_path, Path(folder) / source_data[dest_hash])

    for src_hash, fn in source_data.items():
        if src_hash not in already_presents:
            shutil.copy(Path(source) / fn, Path(destination) / fn)

    return None
