import typing as t


class ReaderProtocol(t.Protocol):
    def read(self, path: str) -> dict[str, str]:
        pass


class FileSystemProtocol(t.Protocol):
    def copy(self, source: str, destination: str) -> None:
        pass

    def move(self, source: str, destination: str) -> None:
        pass

    def delete(self, target: str) -> None:
        pass
