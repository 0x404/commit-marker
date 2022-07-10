import argparse
import sys
from marker import UpdaterCLI, Insighter

class Config:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--mark", action="store_true", default=False)
        self.parser.add_argument("--review", action="store_true", default=False)
        self.parser.add_argument("--insight", action="store_true", default=False)
        self.parser.add_argument("--compare", action="store_true", default=False)
        self.parser.add_argument("-f", "--file", type=str, required=True)
        self.parser.add_argument("-c", "--cfile", type=str)
        self.args = self.parser.parse_args()
    
    @property
    def ready(self):
        return self.__check_args()

    def __check_args(self):
        func_count = self.args.mark + self.args.review + self.args.insight + self.args.compare
        if func_count > 1:
            print("Only one of these four functions can be selected (mark, review, insight, compare)")
            return False
        if func_count < 1:
            print("One of these four functions must be selected (mark, review, insight, compare)")
            return False
        if self.args.compare and self.args.cfile is None:
            print("compare function needs to specify `cfile`")
            print("usage: python3 launch.py --compare --file yourfile1.csv --cfile yourfile2.csv")
            return False
        if not self.args.compare and self.args.cfile is not None:
            print("warning: we will only operate on `file`, not `cfile`")
        return True


if __name__ == "__main__":
    cfg = Config()
    if not cfg.ready:
       sys.exit()
    cfg = cfg.args

    if cfg.mark:
        cli = UpdaterCLI()
        cli(cfg.file, mode='m')
    elif cfg.review:
        cli = UpdaterCLI()
        cli(cfg.file, mode='r')
    elif cfg.insight:
        ins = Insighter()
        ins(cfg.file)
    elif cfg.compare:
        print("no supportd yet")
        pass


