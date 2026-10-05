---
name: workflow-jit-optimization-analysis
description: Use when 从单个 CinderX benchmark 开始，判定 JIT/解释执行路径并定位优化点。
---

# JIT / Interpreter Case Analysis Workflow

## 定位

Supporting Workflow：单 benchmark 用例分析分支。端到端任务中由主 Workflow 在 L2 阶段调用，先判定 JIT / 非 JIT，再分流。

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-smoke-check` |
| worker 运行 | `cinderx-jit-analyst` | `pyperformance-worker-run` |
| 进入 JIT 判定 | `cinderx-jit-analyst` | `cinderx-jit-entry-check` |
| JIT 用例 | `cinderx-jit-analyst` | `cinderx-hir-dump`、`cinderx-hir-lir-analyze` |
| 解释执行用例 / 非 JIT | `cinderx-jit-analyst` | `cinderx-interpreter-case-analyze` |
| 报告 | `cinderx-jit-analyst` | `cinderx-optimization-report` |

## Gate

未证明 benchmark 本体进入 CinderX JIT，不进入 HIR/LIR 优化结论。必须先由 `cinderx-jit-entry-check` 分流：

- `entered_cinderx_jit=true`：进入 JIT 用例路径，查看 HIR、排查 deopt、分析 LIR / uop / 机器码和平台差异。
- `entered_cinderx_jit=false` 或目标热函数不进入 gate：进入解释执行用例路径，使用 `cinderx-interpreter-case-analyze` 输出穿刺证据、分阶段平铺表、函数形状表和 gate 策略。

进入 JIT 和 HIR dump 前必须复用 `../using-cpython-optimize/references/pyperformance-env-contract.md`，确认真实 worker 继承了目标 `PYTHONPATH`、JIT flags、hook 和非 debug/diagnostic 口径，并提供 `.pth`、`pyvenv.cfg` / `include-system-site-packages`、`cinderx.is_initialized()` 等 worker 内 CinderX JIT 证据。
