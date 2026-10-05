---
name: document-release
preamble-tier: 4
version: 1.0.0
description: |
  发布后的文档同步器。按 diff 检查 README、ARCHITECTURE、CONTRIBUTING、
  CHANGELOG、CLAUDE.md、TODOS 等文档是否过期，并尽量自动更新。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /document-release

这是“你刚 ship 完，文档也得跟上”的 skill。

## 核心流程

1. 检测平台与 base branch。
2. `Pre-flight & Diff Analysis`：看这次改了什么。
3. `Per-File Documentation Audit`：逐份文档核对是否漂移。
4. `Apply Auto-Updates`：对明显可自动同步的内容直接改。
5. `Ask About Risky/Questionable Changes`：对不确定内容再问用户。
6. `CHANGELOG Voice Polish`
7. `Cross-Doc Consistency & Discoverability Check`
8. `TODOS.md Cleanup`
9. `VERSION Bump Question`
10. `Commit & Output`

## 适用场景

- 刚跑完 `/ship`
- 功能、命令、架构、运行方式已经变化
- 想避免 README / CONTRIBUTING / CLAUDE.md 慢慢失真

## 关键规则

- 文档更新要以当前事实为准，不写任务过程废话。
- 自动更新不了的地方要明确提问，不要瞎编。
