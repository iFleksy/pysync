import os
import shutil


class FileSystem:
    def copy(self, source: str, destination: str) -> None:
        shutil.copy(source, destination)

    def move(self, source: str, destination: str) -> None:
        shutil.move(source, destination)

    def delete(self, target: str) -> None:
        os.remove(target)
