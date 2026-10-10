---
name: handoff
description: >-
  Writes or reads a short personal handoff for the current project so the next
  session can resume: what was done, what is stuck, and the single next action.
  Use when the user says 交接, 收工, 交给明天, 给明天的自己, handoff, 接着昨天,
  昨天做到哪, or 继续上次.
---

# 收工交接

给明天的自己留一段能接着干的记录。只记事实和下一步，不写周报，不写复盘。

路径、git 事实、文件读写都交给脚本，不要自己拼路径或改格式。脚本在本 skill 目录：

```bash
python3 scripts/handoff.py collect   # 日期、项目路径、git 状态
python3 scripts/handoff.py show      # 读上次交接；没有则退出码 1
python3 scripts/handoff.py save      # 从标准输入覆盖写入
```

在该 skill 目录下执行。交接文件由脚本算好，写在个人目录，不进项目仓库。

## 收工

用户说「交接」「收工」「交给明天」时走这里。不要改项目代码。

1. 执行 `python3 scripts/handoff.py collect`。
2. 再对照当前对话里已经做过的事，写成下面的格式。没做过的不要编。
3. 把全文从标准输入传给 `python3 scripts/handoff.py save`。
4. 用同一段内容回复。路径用脚本打印的那一行。

### 文件格式

每条一两句。没有内容就写「无」。

```markdown
# 交接

日期：YYYY-MM-DD
项目：<工作区绝对路径>

## 做到哪
- ...

## 卡在哪
- ...

## 明天第一件
一件事。具体到打开哪个文件，或跑哪条命令。

## 别动
明天不要重做、不要顺手改的东西。
```

- 用中文。
- 只写这次会话和当前工作区里能核实的事。没做过的不要编。
- 「明天第一件」只能有一件，写下一步动作，不写目标。
- 不提建议清单，不加「可以考虑」。
- 有未提交改动时，在「做到哪」里点出哪些文件还没提交。

## 开工

用户说「接着昨天」「昨天做到哪」「继续上次」时走这里。

1. 执行 `python3 scripts/handoff.py show`。输出是「没有上次交接」就照说，然后停。
2. 用四行复述：日期、做到哪、卡在哪、明天第一件。
3. 问要不要直接做那一件。用户没同意之前不要改代码。
