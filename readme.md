# Commit Marker
It is a help tool, used to mark the commit message dataset. 

Given the subject, message, and changed files of a git commit, mark which category the commit message belongs to:

* Corrective: bug fix
* Perfective: system improvements
* Adaptive: features

<img src="http://image-hosting-404.oss-cn-beijing.aliyuncs.com/img/marker1.png" />



## Usage

It is recommended to use [VS Code](https://code.visualstudio.com/) or [Windows Terminal](https://github.com/microsoft/terminal), because you can directly click the commit detail link to see detail commit message.

First, please install the dependent third-party libraries

```shell

pip3 install -r requirements.txt

```

If you want to mark data, you should use the following command, this will start from the first unlabeled data:

```shell

python3 launch.py --mark --file sampled_commits.csv

```

If you want to review data, you should use the following command.

This will start with the first data and display the data labels, which you can modify during the review process:

```shell

python3 launch.py --review --file sampled_commits.csv

```

If you want to have some insights into dataset, you should use the following command.

```shell

python3 launch.py --insight --file sampled_commits.csv

```

If you want to compare two data files, you should use the following command.

This will display commits with different label, you can decide which label to use while viewing:

**warning: the result of the comparison will be saved to compare_result.csv in the current folder, so please make sure there is no compare_result.csv in the current folder**

```shell

python3 launch.py --compare --file yourfile1.csv --cfile yourfile2.csv

```


## Feature

* friendly data display
* stop at any time, continue at any time
* review marked commits
