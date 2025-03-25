import os
import shutil
from pathlib import Path
from typing import Any, Generator, Literal

from .. import helpers


class SyncError(Exception):
    pass


class SourceNotExists(SyncError):
    pass


class DestinationNotExists(SyncError):
    pass


def read_and_compute_hashes(p: str) -> dict[str, str]:
    hashes_data: dict[str, str] = {}

    for folder, _, files in os.walk(p):
        for fn in files:
            path = Path(folder) / fn
            with path.open("rb") as f:
                hashes_data[helpers.hash_buffer(f)] = fn
    return hashes_data


def compute_diff(
    source_hashes: dict[str, str], destination_hashed: dict[str, str], source_path: str, destination_path: str
) -> Generator[
    tuple[Literal["copy"], Path, Path] | tuple[Literal["move"], Path, Path] | tuple[Literal["delete"], Path], Any, None
]:
    for src_hash, file_name in source_hashes.items():
        if src_hash not in destination_hashed:
            yield "copy", (Path(source_path) / file_name), (Path(destination_path) / file_name)
        elif destination_hashed[src_hash] != file_name:
            yield "move", Path(destination_path) / destination_hashed[src_hash], Path(destination_path) / file_name

    for dst_hash, _ in destination_hashed.items():
        if dst_hash not in source_hashes:
            yield "delete", Path(destination_path) / destination_hashed[dst_hash]


def sync(source: str, destination: str) -> None:
    if not os.path.exists(source):
        raise SourceNotExists()

    if not os.path.exists(destination):
        raise DestinationNotExists()

    source_data: dict[str, str] = {}

    source_data = read_and_compute_hashes(source)
    destination_data = read_and_compute_hashes(destination)

    for action, *paths in compute_diff(source_data, destination_data, source, destination):
        if action == "copy":
            shutil.copy(str(paths[0]), str(paths[1]))
        elif action == "move":
            shutil.move(str(paths[0]), str(paths[1]))
        if action == "delete":
            os.remove(str(paths[0]))
