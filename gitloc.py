from dataclasses import dataclass
import re
from datetime import datetime
import subprocess


@dataclass
class Commit:
    date: datetime
    adds: int
    deletes: int


def parse_commit(commit_str: str) -> Commit:
    date = None
    adds = 0
    deletes = 0
    for line in commit_str.splitlines():
        if line.startswith("Date"):
            date = datetime.fromisoformat(line[8:])
        if line.startswith("+") and not line.startswith("+++"):
            adds += 1
        if line.startswith("-") and not line.startswith("---"):
            deletes += 1
    return Commit(date, adds, deletes)


def get_commits(target_folder=""):
    gitopts = ""
    if target_folder:
        gitopts += "--git-dir=" + target_folder + "/.git"
    gitlogopts = "--no-color --date-order --reverse --date=iso-strict -p"
    gitcmd = "git " + gitopts + " log " + gitlogopts

    git_log = subprocess.check_output(gitcmd, shell=True).decode()

    commit_strs = re.split("commit [0-9a-z]{40}\n", git_log)

    commits = []

    for commit_str in commit_strs:
        commits.append(parse_commit(commit_str))

    return commits
