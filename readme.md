# Commit Marker
It is a help tool, used to mark the commit message dataset. 

Given the subject, message, and changed files of a git commit, mark which category the commit message belongs to:

* Corrective: bug fix
* Perfective: system improvements
* Adaptive: features

<img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/marker1.png" />



## Usage

It is recommended to use [VS Code](https://code.visualstudio.com/) or [Windows Terminal](https://github.com/microsoft/terminal), because you can directly click the commit detail link to see detail commit message.

use the following command on the command line.

```shell

python3 marker.py -f sampled_commits.csv # CLI, default to mark mode

python3 marker.py -f sampled_commits.csv --review # CLI, review mode, show marked commits

python3 marker.py -f sampled_commits.csv --gui # no supported yet

```



## Feature

* Friendly data display
* stop at any time, continue at any time
* review marked commits
