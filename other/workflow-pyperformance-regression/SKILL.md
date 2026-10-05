---
name: workflow-pyperformance-regression
description: Use when 编排正式 CPython/CinderX A/B 回归的环境、双侧运行和结果分析；已有数据直接用结果比较技能。
---

# pyperformance Regression Workflow

## 定位

Supporting Workflow：正式性能验证分支。由主 Workflow 在 L3/L4 阶段调用。

## Agent 分派

下表按当前证据选择所需阶段，已有匹配产物可复用；Agent 列是职责，可由主 Agent 顺序承担，仅在宿主允许且有独立工作时委派。

| 阶段 | Agent | 技能 |
|------|-------|------|
| 环境确认 | `cinderx-environment-verifier` | `cinderx-env-validate` |
| A/B slot | `cinderx-orchestrator` | `cinderx-ab-run-slot` |
| baseline | `pyperformance-baseline-runner` | `pyperformance-suite-run` |
| candidate | `pyperformance-candidate-runner` | `pyperformance-suite-run` |
| 分析 | `pyperformance-benchmark-analyst` | `pyperformance-result-compare` |
| 报告 | `pyperformance-benchmark-analyst` | `cinderx-optimization-report` |

## Gate

baseline/candidate 必须说明口径 baseline 和提交 baseline。并行前 CPU set、绑核、结果目录、容器线不冲突。

正式 A/B 前必须引用 `../using-cpython-optimize/references/baseline-source-contract.md`，确认 baseline source 是 `baseline_source_verified`。远程环境或容器可用只能证明执行环境可跑，不能自动把远程 workspace 当前源码当 baseline；若返回 `baseline_source_untrusted`，先查证；已知 ref 可在隔离 worktree 修复并复验，含义不明时再询问。

正式运行前必须让 baseline/candidate runner 共同引用 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md`，确认用户命令里的 `--affinity` 已按当前 `nproc` / `lscpu` / `taskset -pc $$` / 容器 cpuset 映射到可用 CPU；不能逐字照抄不可用高核号。

正式运行前必须让 baseline/candidate runner 共同引用 `../using-cpython-optimize/references/pyperformance-env-contract.md`，确认 `--inherit-environ`、driver/worker env、helper 变量和唯一差异轴一致；CinderX JIT 口径还要确认 worker 可见的 `.pth`、`pyvenv.cfg` / `include-system-site-packages`、`cinderx.is_initialized()` 等证据。环境契约缺失时不能进入正式 `pyperf compare_to` 结论。
