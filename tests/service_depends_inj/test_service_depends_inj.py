from operator import itemgetter

from pysync.service_depends_inject.service import sync


class FakeFileSystem:
    def __init__(self):
        self.operations = []

    def copy(self, source: str, destination: str) -> None:
        self.operations.append(("copy", source, destination))

    def move(self, source: str, destination: str) -> None:
        self.operations.append(("move", source, destination))

    def delete(self, target: str) -> None:
        self.operations.append(("delete", target))


class FakeReader:
    def __init__(self, fake_data: dict[str, dict[str, str]]) -> None:
        self.fake_data: dict[str, dict[str, str]] = fake_data

    def read(self, path: str) -> dict[str, str]:
        return self.fake_data[path]


def test_run_sync_data_all_operations():
    source_path = "/src"
    destination_path = "/dst"

    fake_file_system = FakeFileSystem()
    fake_reader = FakeReader(
        {
            source_path: {
                "985a2142-49d6-4f5b-8544-41aec831a8b8": "file_text.txt",  # To rename
                "470b7e1f-789f-4d71-8b2d-996ad773c537": "file_log.log",  # To create
            },
            destination_path: {
                "985a2142-49d6-4f5b-8544-41aec831a8b8": "file_text.back",  # To rename
                "07562976-ff4a-4f5a-a3f1-52acf8588f9f": "undefined.ter",  # To delete
            },
        }
    )

    source_path = "/src"
    destination_path = "/dst"

    assert sync(fake_reader, fake_file_system, source_path, destination_path) is None
    assert sorted(fake_file_system.operations, key=itemgetter(0, 1)) == [
        (
            "copy",
            "/src/file_log.log",
            "/dst/file_log.log",
        ),
        (
            "delete",
            "/dst/undefined.ter",
        ),
        (
            "move",
            "/dst/file_text.back",
            "/dst/file_text.txt",
        ),
    ]
