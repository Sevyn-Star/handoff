#!/usr/bin/env python3
"""收工交接：收集 git 事实，读写交接文件。叙述仍由代理来写。"""

import datetime
import subprocess
import sys
from pathlib import Path

HANDOFF_DIR = Path.home() / ".cursor" / "handoffs"


def project_key(cwd: Path) -> str:
    return "-".join(part for part in cwd.resolve().parts if part not in ("/", ""))


def handoff_path(cwd: Path) -> Path:
    return HANDOFF_DIR / f"{project_key(cwd)}.md"


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    except FileNotFoundError:
        return 127, ""
    text = result.stdout.strip() or result.stderr.strip()
    return result.returncode, text


def is_git(cwd: Path) -> bool:
    code, text = run(["git", "rev-parse", "--is-inside-work-tree"], cwd)
    return code == 0 and text == "true"


def collect(cwd: Path) -> int:
    path = handoff_path(cwd)
    print(f"日期：{datetime.date.today().isoformat()}")
    print(f"项目：{cwd.resolve()}")
    print(f"交接文件：{path}")
    if not is_git(cwd):
        print("git：不是 git 仓库")
        return 0
    print("git：是 git 仓库")
    commands = [
        ("status", ["git", "status", "-sb"]),
        ("diff_stat", ["git", "diff", "--stat"]),
        ("cached_stat", ["git", "diff", "--cached", "--stat"]),
        ("log", ["git", "log", "-8", "--oneline"]),
    ]
    for label, cmd in commands:
        _, text = run(cmd, cwd)
        print(f"\n## {label}")
        print(text or "（空）")
    return 0


def show(cwd: Path) -> int:
    path = handoff_path(cwd)
    if not path.is_file():
        print("没有上次交接")
        return 1
    sys.stdout.write(path.read_text())
    return 0


def save(cwd: Path) -> int:
    body = sys.stdin.read()
    if not body.strip():
        print("没有内容可写", file=sys.stderr)
        return 1
    path = handoff_path(cwd)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not body.endswith("\n"):
        body += "\n"
    path.write_text(body)
    print(path)
    return 0


def main() -> int:
    commands = {"collect": collect, "show": show, "save": save}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        names = " | ".join(commands)
        print(f"用法: handoff.py {names}", file=sys.stderr)
        return 2
    return commands[sys.argv[1]](Path.cwd())


if __name__ == "__main__":
    sys.exit(main())
