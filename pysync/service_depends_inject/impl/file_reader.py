import os
from pathlib import Path

from pysync import helpers


class FileReader:
    def read(self, path: str) -> dict[str, str]:
        hashes_data: dict[str, str] = {}

        for folder, _, files in os.walk(path):
            for fn in files:
                file_path = Path(folder) / fn
                with file_path.open("rb") as f:
                    hashes_data[helpers.hash_buffer(f)] = fn
        return hashes_data
