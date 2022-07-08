# Commit Marker
It is a help tool, used to mark the commit message dataset. 

Given the subject, Message, and changed file of a git commit, mark which category the commit message belongs to:

* Corrective: bug fix
* Perfective: system improvements
* Adaptive: features

<img src=".\images\CLI.png" style="zoom:67%;" />



## Usage

It is recommended to use [VS Code](https://code.visualstudio.com/) or [Windows Terminal](https://github.com/microsoft/terminal), because you can directly click the commit detail link to see detail commit message.

If you are a Linux user, the code of the master branch cannot be applied, please switch to the [linux branch](https://github.com/0x404/commit-marker/tree/linux)

If you are a Windows user or a MacOS user (not tested), you need to use the following command to install the dependent modules.

```shell

pip3 install -r requirements.txt # install requirement modules

```

After that, use the following command on the command line.

```shell

python3 marker.py -f sampled_commits.csv # CLI, default to mark mode

python3 marker.py -f sampled_commits.csv --review # CLI, review mode, show marked commits

python3 marker.py -f sampled_commits.csv --gui # no supported yet

```



## Feature

* Friendly data display
* stop at any time, continue at any time
* review marked commits
