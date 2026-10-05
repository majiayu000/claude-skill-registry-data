---
name: workflow-platform-differential-discovery
description: Use when 尚未选定用例，需要从 CPython/CinderX 平台差异中筛选优化候选。
---

# Platform Differential Discovery Workflow

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| 平台建模 | `cinderx-platform-analyst` | `cinderx-isa-microarch-compare` |
| 覆盖数据 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| JIT 细节 | `cinderx-jit-analyst` | `cinderx-jit-entry-check`、`cinderx-hir-lir-analyze` |
| 报告 | `cinderx-platform-analyst` | `cinderx-optimization-report` |

## Gate

先建立 ISA、微架构、perf、benchmark 覆盖矩阵，再进入具体 HIR/LIR。

## 输出契约

产物是候选用例清单，供深钻 `workflow-platform-differential-discovery-deepdive` 的阶段 0 选例使用（推荐输入，非强制）。每个候选至少带：

- 用例名
- 双平台 wall clock 差距
- 热度信号
- 为何值得深钻（一句话）

清单回答"先钻哪个用例"，不回答"这个用例怎么优化"——后者交给深钻 workflow 的证据表。不要默认跑三小时全量。
