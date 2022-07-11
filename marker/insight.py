from collections import defaultdict
from prettytable import PrettyTable
from marker.config import *
from marker.updater import CSVUpdater


class Insighter:
    @staticmethod
    def show_count_table(filename: str) -> None:
        with CSVUpdater(filename, mode="r") as updater:
            total = updater.totol_raws
            completed = updater.completed_raws

        count_table = PrettyTable()
        count_table.field_names = ["Labeled", "UN-Labeled", "Total"]
        count_table.add_row([completed, total - completed, total])
        print(count_table, end="\n\n")

    @staticmethod
    def show_label_table(filename: str) -> None:
        """Show label detail info.
        Count the total number of a label, and how much belongs to keyword related.

        Args:
            filename(str): CSV filename.
        """

        def contains(sentence: str, words: list[str]) -> bool:
            """check whther sentence contains any one of words"""
            sentence = sentence.lower()
            return any(sentence.find(word) != -1 for word in words)

        counts, relates = defaultdict(int), defaultdict(int)
        with CSVUpdater(filename, mode="r") as updater:
            for _, row in updater:
                label = row["Labels"]
                subject = row["Subject"]
                message = row["Message"]
                counts[label] += 1
                if any(contains(s, keywords[label]) for s in (subject, message)):
                    relates[label] += 1

        def makerow(key):
            return [key, counts[key], relates[key], counts[key] - relates[key]]

        label_table = PrettyTable()
        label_table.field_names = [
            "Category",
            "Count",
            "Keyword-Related",
            "Keyword-NotRelated",
        ]
        label_table.add_row(makerow(CORRECTIVE))
        label_table.add_row(makerow(ADAPTIVE))
        label_table.add_row(makerow(ADAPTIVE))
        print(label_table, end="\n\n")

    def __call__(self, filename: str, *args, **kwds) -> None:
        self.show_count_table(filename)
        self.show_label_table(filename)
