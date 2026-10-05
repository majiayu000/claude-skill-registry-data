---
name: workflow-cinderx-crash-triage
description: Use when 需要串起 CinderX crash 的复现、gdb/JIT 取证与报告；已有 core 的局部分析用 cinderx-gdb-core-triage。
---

# CinderX Crash Triage Workflow

## 定位

Supporting Workflow：crash 异常分支。端到端任务中由主 Workflow 调用，不要作为默认入口。

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| crash 接管 | `cinderx-crash-triager` | `cinderx-gdb-core-triage` |
| worker 复现 | `cinderx-crash-triager` | `pyperformance-worker-run` |
| JIT/HIR 证据 | `cinderx-crash-triager` | `cinderx-hir-dump`、`cinderx-jit-entry-check` |
| 报告 | `cinderx-crash-triager` | `cinderx-optimization-report` |

## Gate

没有真实命令、exit status、`gdb bt full` 或 core 摘要时，不进入根因结论。JIT crash 必须补 HIR/jit.log 或说明不可采集原因。
