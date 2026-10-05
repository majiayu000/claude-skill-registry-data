---
name: workflow-cross-platform-delta-triage
description: Use when 已测出同一 benchmark 的双平台差距，需要排除环境漂移、归因并验证优化收益。
---

# Cross Platform Delta Triage Workflow

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| A/B slot | `cinderx-orchestrator` | `cinderx-ab-run-slot` |
| baseline 平台 | `pyperformance-baseline-runner` | `pyperformance-suite-run` / `pyperformance-worker-run` |
| candidate 平台 | `pyperformance-candidate-runner` | `pyperformance-suite-run` / `pyperformance-worker-run` |
| 结果分析 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| 平台归因 | `cinderx-platform-analyst` | `cinderx-isa-microarch-compare` |
| JIT 细节 | `cinderx-jit-analyst` | `cinderx-jit-entry-check`、`cinderx-hir-lir-analyze` |

## Gate

先排环境漂移，再谈 ISA/微架构。输出收益范围、无收益范围和下一阶验证条件。
