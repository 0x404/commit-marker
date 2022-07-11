import csv
import shutil
from pathlib import Path
from marker.config import *


class CSVUpdater:
    """A simple CSV updater"""

    def __init__(self, filename: str, mode: str = "m"):
        self.file_path = Path(filename)
        self.rows = []
        self.csv_reader = None
        self.csv_writer = None
        self.csv_file = None
        self.tmp_file = None
        self.totol_raws = 0
        self.mode = mode

    @property
    def completed_raws(self):
        """FIXME: only can be accessed when quit updater"""
        assert self.totol_raws > 0
        for row in self.csv_reader:
            self.rows.append(row)
        completed_raws = sum(1 for row in self.rows if len(row["Labels"]) > 0)
        return completed_raws

    def mark(self, label: str, rowno: int = -1):
        """Mark a specified commit message with label.

        Args:
            label(str): must be one of `Corrective`, `Perfective`, `Adaptive`
            rowno(int): specify commit message line, default -1 (the latest one).
        """
        assert label in (CORRECTIVE, PERFECTIVE, ADAPTIVE)
        assert -1 <= rowno < len(self.rows), "index out of range"
        self.rows[rowno]["Labels"] = label

    def __iter__(self):
        """Generator which iters commit message without `Labels` filed."""
        assert self.csv_reader is not None, "I/O in unopened file"
        assert self.csv_writer is not None, "I/O in unopened file"
        for rowno, row in enumerate(self.csv_reader):
            self.rows.append(row)
            if len(row["Labels"]) != 0 and self.mode == "m":
                continue
            yield (rowno, row)

    def __enter__(self):
        """Open files and readers"""
        if self.csv_reader is not None:
            raise RuntimeError("reader has been created")
        with open(str(self.file_path), mode="r", encoding="UTF-8") as f:
            tmp_reader = csv.DictReader(f)
            self.totol_raws = sum(1 for _ in tmp_reader)

        self.csv_file = open(str(self.file_path), mode="r", encoding="UTF-8")
        self.tmp_file = open(
            str(self.file_path.parent.joinpath("tmp.csv")), mode="w", encoding="UTF-8"
        )
        self.csv_reader = csv.DictReader(self.csv_file)
        self.csv_writer = csv.DictWriter(self.tmp_file, HEADERS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close files, flush updated rows and copy unchanged rows"""
        self.csv_writer.writeheader()
        for row in self.csv_reader:
            self.rows.append(row)
        self.csv_writer.writerows(self.rows)

        self.csv_file.close()
        self.tmp_file.close()

        shutil.move(str(self.file_path.parent.joinpath("tmp.csv")), str(self.file_path))
