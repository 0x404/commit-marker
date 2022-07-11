import os
from marker.updater import CSVUpdater
from marker.config import *


class UpdaterCLI:
    """Command line interface"""

    def __init__(self):
        self.subject_color = "\x1b[0;30;44m"
        self.message_color = "\x1b[0;30;42m"
        self.detail_color = "\x1b[0;30;46m"
        self.changed_color = "\x1b[0;30;47m"
        self.default_color = "\x1b[0m"
        self.label_color = "\x1b[0;30;41m"
        self.rowno_color = "\x1b[6;32;47m"

    def format_row(self, row: list[str], rowno: int, total: int, mode: str):
        """Format a csv row to a friendly commit message"""
        formated_str = f"{self.rowno_color}[{rowno}/{total}]{self.default_color}\n\n\n"
        formated_str += f"\t{self.subject_color}Subject{self.default_color}: {row.get('Subject')}\n\n"
        formated_str += f"\t{self.message_color}Message{self.default_color}: {row.get('Message')}\n\n"
        formated_str += f"\t{self.changed_color}Changed{self.default_color}: {row.get('changed files | + | -| sum').strip()}\n\n"
        formated_str += f"\t{self.detail_color}Detail{self.default_color}:  https://github.com/rust-lang/rust/commit/{row.get('Hash')}\n\n"
        if mode == "r":
            formated_str += f"\t{self.label_color}Labels{self.default_color}:  {row.get('Labels')}\n\n"
        return formated_str

    def get_label(self):
        """Get label input from user"""
        c2str = {
            "c": CORRECTIVE,
            "p": PERFECTIVE,
            "a": ADAPTIVE,
            "q": None,
            "n": "Next",
        }
        label = input(
            "input label (c for Corrective, p for Perfective, a for Adaptive, q for quit, n for next) >> "
        ).lower()
        while label not in c2str:
            label = input(
                "input label (c for Corrective, p for Perfective, a for Adaptive, q for quit, n for next) >> "
            ).lower()
        return c2str[label]

    def __call__(self, filename: str, *args, mode: str = "m", **kwds):
        """Lauch command line interface.

        Args:
            filename(str): CSV file to be processed.
            mode(str): must be one of "m" or "r", short for "mark" and "review".
        """
        with CSVUpdater(filename, mode=mode) as updater:
            total = updater.totol_raws

            for rowno, row in updater:
                os.system("cls" if os.name == "nt" else "clear")
                print(self.format_row(row, rowno, total, mode=mode))

                label = self.get_label()
                if label in (CORRECTIVE, PERFECTIVE, ADAPTIVE):
                    updater.mark(label)
                elif label == "Next":
                    continue
                else:
                    break

            completed = updater.completed_raws
            completed_ratio = completed / total * 100
            print(
                f"mark finished, has completed {completed} commits(total {total}, {completed_ratio:.2f}%)\n"
            )
