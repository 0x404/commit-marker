import os
import csv
import shutil
import argparse
from pathlib import Path

CORRECTIVE : str = "Corrective"
PERFECTIVE : str = "Perfective"
ADAPTIVE : str = "Adaptive"
HEADERS : list = ['\ufeffID', 'Hash', 'Subject', 'Message', 'Num_files', 'LOC', 'changed files | + | -| sum', 'Labels', '']

class CSVUpdater:
    """A simple CSV updater"""

    def __init__(self, filename):
        self.file_path = Path(filename)
        self.rows = []
        self.csv_reader = None
        self.csv_writer = None
        self.csv_file = None
        self.tmp_file = None
        self.totol_raws = 0
    
    @property
    def completed_raws(self):
        assert self.totol_raws > 0
        completed_raws = sum(1 for row in self.rows if len(row["Labels"]) > 0)
        return completed_raws
    
    
    def mark(self, label, rowno=-1):
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
            if len(row["Labels"]) == 0:
                yield (rowno, row)

    def __enter__(self):
        """Open files and readers"""
        if self.csv_reader is not None:
            raise RuntimeError("reader has been created")
        with open(str(self.file_path), mode='r', encoding='UTF-8') as f:
            tmp_reader = csv.DictReader(f)
            self.totol_raws = sum(1 for _ in tmp_reader)

        self.csv_file = open(str(self.file_path), mode='r', encoding='UTF-8')
        self.tmp_file = open(str(self.file_path.parent.joinpath("tmp.csv")), mode='w', encoding='UTF-8')
        self.csv_reader = csv.DictReader(self.csv_file)
        self.csv_writer = csv.DictWriter(self.tmp_file, HEADERS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close files, flush updated rows and copy unchanged rows"""
        self.csv_writer.writeheader()
        self.csv_writer.writerows(self.rows)
        for row in self.csv_reader:
            self.csv_writer.writerow(row)

        self.csv_file.close()
        self.tmp_file.close()

        shutil.move(str(self.file_path.parent.joinpath("tmp.csv")), str(self.file_path))
    
class UpdaterCLI:
    """Command line interface"""

    def __init__(self):
        self.subject_color = "\x1b[0;30;44m"
        self.message_color = "\x1b[0;30;42m"
        self.detail_color = "\x1b[0;30;46m"
        self.changed_color = "\x1b[0;30;47m"
        self.default_color = "\x1b[0m"
        pass
    
    def format_row(self, row):
        """Format a csv row to a friendly commit message"""
        formated_str = f"\t{self.subject_color}Subject{self.default_color}: {row.get('Subject')}\n\n"
        formated_str += f"\t{self.message_color}Message{self.default_color}: {row.get('Message')}\n\n"
        formated_str += f"\t{self.changed_color}Changed{self.default_color}: {row.get('changed files | + | -| sum')}\n\n"
        formated_str += f"\t{self.detail_color}Detail{self.default_color}: https://github.com/rust-lang/rust/commit/{row.get('Hash')}\n\n"
        return formated_str
    
    def get_label(self):
        c2str = {'C' : CORRECTIVE, 'P' : PERFECTIVE, 'A' : ADAPTIVE, 'Q' : None}
        label = input("input label (C for Corrective, P for Perfective, A for Adaptive, Q for quit) >> ")
        while label not in c2str:
            label = input("input label (C for Corrective, P for Perfective, A for Adaptive, Q for quit) >> ")
        return c2str[label]
        
    
    def __call__(self, filename, *args, **kwds):
        with CSVUpdater(filename) as updater:
            for rowno, row in updater:
                print(self.format_row(row))
                label = self.get_label()
                if label is not None:
                    updater.mark(label)
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    break
            completed = updater.completed_raws
            total = updater.totol_raws
            completed_ratio = completed / total
            print(f"mark finished, has completed {completed} commits(total {total}, {completed_ratio:.2f}%)\n")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, required=True)
    parser.add_argument("--gui", action="store_true")
    args = parser.parse_args()
    
    if args.gui:
        print("no supported yet")
    else:
        cli = UpdaterCLI()
        cli(args.file)
