---
name: commit-message
description: 从代码变更生成规范的 git 提交信息。当用户要求写 commit message、提交代码、或提到"帮我把这些改动提交一下"时使用。
---

# 提交信息生成

## 收集变更

用 TERMINAL 执行 `git status` 与 `git diff`（暂存区用 `git diff --cached`）获取实际变更；diff 很大时先看 `git diff --stat` 抓重点文件。

## 生成规则

- 第一行：`type(scope): 摘要`，不超过 50 字符，用祈使句或动宾短语。
  - type 从变更内容判断：`feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `perf`
  - 参考 `git log --oneline -10` 匹配本仓库已有的语言与格式习惯（本项目提交信息中英混用，以近期风格为准）。
- 空一行后写正文：说明"为什么改"而不只是"改了什么"；有多个独立变更点时用 `-` 列表。
- 不要编造 diff 里不存在的改动；不确定意图时先问用户。

## 提交

用户明确要求提交时，先展示完整 commit message 征求确认，再用 TERMINAL 执行 `git add <具体文件>` 与 `git commit -m "<title>" -m "<body>"`。不要使用 `git add .` 或 `git add -A`，除非用户明确要求。
