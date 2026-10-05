---
name: workflow-remote-cinderx-lab-setup
description: Use when 远程 CPython/CinderX lab 需要串起环境审计、修复或初始化与 smoke。
---

# Remote CinderX Lab Setup Workflow

## 定位

Supporting Workflow：环境准备子流程。不要作为端到端优化任务的默认入口；由主 Workflow 调用。

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境三态 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| 新环境 | `cinderx-environment-verifier` | `cinderx-env-bootstrap`、`cinderx-remote-lab-ops` |
| 被破坏环境 | `cinderx-environment-verifier` | `cinderx-env-clean`、`cinderx-env-bootstrap` |
| smoke | `cinderx-environment-verifier` | `cinderx-smoke-check` |

## Gate

返回 `reusable`、`needs_bootstrap` 或 `needs_clean_bootstrap`，并记录 host、workspace、container line、Python、`SOABI`、`patchlevel.h`、CinderX commit 和 pyperformance 版本。
