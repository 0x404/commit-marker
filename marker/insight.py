from collections import defaultdict
from itertools import count
from typing import Counter
from prettytable import PrettyTable
from marker.config import *
from marker.updater import CSVUpdater


class Insighter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def show_count_table(filename):
        count_table = PrettyTable()
        count_table.field_names = ["Labeled", "UN-Labeled", "Total"]
        with CSVUpdater(filename, mode="r") as updater:
            total = updater.totol_raws
            completed = updater.completed_raws
        count_table.add_row([completed, total - completed, total])
        print(count_table, end="\n\n")

    @staticmethod
    def show_label_table(filename):
        label_table = PrettyTable()
        label_table.field_names = [
            "Category",
            "Count",
            "Keyword-Related",
            "Keyword-NotRelated",
        ]
        counts, relates = defaultdict(int), defaultdict(int)

        def contains(sentence, words):
            sentence = sentence.lower()
            return any(sentence.find(word) != -1 for word in words)

        with CSVUpdater(filename, mode="r") as updater:
            for _, row in updater:
                label = row["Labels"]
                subject = row["Subject"]
                message = row["Message"]

                counts[label] += 1
                if contains(subject, keywords[label]) or contains(
                    message, keywords[label]
                ):
                    relates[label] += 1
        label_table.add_row(
            [
                CORRECTIVE,
                counts[CORRECTIVE],
                relates[CORRECTIVE],
                counts[CORRECTIVE] - relates[CORRECTIVE],
            ]
        )
        label_table.add_row(
            [
                PERFECTIVE,
                counts[PERFECTIVE],
                relates[PERFECTIVE],
                counts[PERFECTIVE] - relates[PERFECTIVE],
            ]
        )
        label_table.add_row(
            [
                ADAPTIVE,
                counts[ADAPTIVE],
                relates[ADAPTIVE],
                counts[ADAPTIVE] - relates[ADAPTIVE],
            ]
        )
        print(label_table, end="\n\n")

    def __call__(self, filename, *args, **kwds):
        self.show_count_table(filename)
        self.show_label_table(filename)
