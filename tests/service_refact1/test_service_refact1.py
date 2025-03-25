from pathlib import Path

from pysync.service_refactor.service_refact1 import compute_diff


def test_compute_diff_move_action():
    src_hashes = {"hash1": "fn1"}
    dst_hashes = {"hash1": "fn2"}
    actions = compute_diff(src_hashes, dst_hashes, "/src", "/dst")
    assert list(actions) == [("move", Path("/dst/fn2"), Path("/dst/fn1"))]


def test_compute_diff_copy_action():
    src_hashes = {"hash1": "fn1"}
    dst_hashes = {}
    actions = compute_diff(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("copy", Path("/src/fn1"), Path("/dst/fn1"))]


def test_compute_diff_delete_action():
    src_hashes = {}
    dst_hashes = {"hash1": "fn1"}
    actions = compute_diff(src_hashes, dst_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("delete", Path("/dst/fn1"))]
