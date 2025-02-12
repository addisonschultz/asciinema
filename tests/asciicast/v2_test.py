import json
import tempfile

from asciinema.asciicast import v2

from ..test_helper import Test


class TestWriter(Test):
    @staticmethod
    def test_writing() -> None:
        _file, path = tempfile.mkstemp()

        with v2.writer(path, width=80, height=24) as w:
            w.write_stdout(1, "x")  # ensure it supports both str and bytes
            w.write_stdout(2, bytes.fromhex("78 c5 bc c3 b3 c5"))
            w.write_stdout(3, bytes.fromhex("82 c4 87"))
            w.write_stdout(4, bytes.fromhex("78 78"))

        with open(path, "rt", encoding="utf_8") as f:
            lines = list(map(json.loads, f.read().strip().split("\n")))
            assert lines == [
                {"version": 2, "width": 80, "height": 24},
                [1, "o", "x"],
                [2, "o", "xżó"],
                [3, "o", "łć"],
                [4, "o", "xx"],
            ], f"got:\n\n{lines}"
