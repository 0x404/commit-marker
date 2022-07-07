# Commit Marker
It is a help tool, used to mark the commit message dataset. Given the subject, Message, and changed file of a git commit, mark which category the commit message belongs to:

* Corrective: bug fix
* Perfective: system improvements
* Adaptive: features



## Usage

Use the following command on the command line.

It is recommended to use [VS Code](https://code.visualstudio.com/) or [Windows Terminal](https://github.com/microsoft/terminal), because you can directly click the commit detail link to see detail commit message.

```shell

python3 marker.py -f sampled_commits.csv # CLI, default to mark mode

python3 marker.py -f sampled_commits.csv --review # CLI, review mode, show marked commits

python3 marker.py -f sampled_commits.csv --gui # no supported yet

```



## Feature

* Friendly data display
* stop at any time, continue at any time
* review marked commits
