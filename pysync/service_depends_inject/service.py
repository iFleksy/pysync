from pathlib import Path

from . import types


def sync(reader: types.ReaderProtocol, file_system: types.FileSystemProtocol, source: str, destination: str) -> None:
    source_hashes = reader.read(source)
    destination_hashes = reader.read(destination)

    for dst_hash, _ in destination_hashes.items():
        if dst_hash not in source_hashes:
            file_system.delete(str(Path(destination) / destination_hashes[dst_hash]))

    for src_hash, file_name in source_hashes.items():
        if src_hash not in destination_hashes:
            file_system.copy(str(Path(source) / file_name), str(Path(destination) / file_name))

        elif destination_hashes[src_hash] != file_name:
            file_system.move(str(Path(destination) / destination_hashes[src_hash]), str(Path(destination) / file_name))
