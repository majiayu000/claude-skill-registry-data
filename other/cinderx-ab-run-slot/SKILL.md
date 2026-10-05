---
name: cinderx-ab-run-slot
description: Use when 为 CPython/CinderX A/B 实验分配 CPU、容器和结果目录，判断能否并行。
---

# CinderX A/B Run Slot

给 orchestrator 和 pyperformance runners 使用。它只负责 A/B 资源切分，不解释性能结果。

## Slot 内容

- baseline slot：commit、容器线、Python、CPU affinity、结果目录、日志路径。
- candidate slot：commit、容器线、Python、CPU affinity、结果目录、日志路径。
- 互斥资源：CPU set 不重叠，tmux pane 不共享，build dir 不共享，`run.json` 输出不覆盖。

## Baseline Source 门禁

- 先读取 `../using-cpython-optimize/references/baseline-source-contract.md`。
- baseline slot 必须绑定 `baseline_source_verified`：口径 baseline、提交 baseline、source path、commit/ref、`git status --short`、`patchlevel.h`、`SOABI` 和容器 bind mount 都已确认。
- 远程环境、容器线或 tmux pane 可用不等于 baseline 源码可信；不能把远程 workspace 当前源码直接当 baseline。
- 若 baseline ref 不明、dirty 状态未解释、bind mount 指向不明或混入 candidate editable install，返回 `baseline_source_untrusted`，不分配正式 A/B slot。

## 并行前检查

- verifier 已确认环境可复用或已 bootstrap。
- verifier 已确认 baseline source verified；只有执行环境 reusable 不够。
- baseline/candidate 只在目标变量上不同。
- 先读取 `../using-cpython-optimize/references/pyperformance-affinity-guidance.md`，确认 `--affinity` / `taskset` 使用当前可用 CPU，而不是逐字照抄用户命令里的不可用高核号。
- 绑核策略写清，例如 `--affinity=0-7` 与 `--affinity=8-15`，或 `taskset -c 0-7` 与 `taskset -c 8-15`。
- 分配前查 `nproc`、`lscpu`、`taskset -pc $$` 和容器 cpuset；baseline/candidate 的 CPU set 数量尽量一致且不重叠。
- 可用 CPU 不足以并行隔离时，改为串行执行，并让 baseline/candidate 复用同一实际 affinity。
- `cinderx-test` 与 `cpython-baseline` 使用场景明确。

## 反问 Gate

- baseline/candidate 的比较对象或唯一差异轴查证后仍不明确时，询问。
- source 未验证时先补证据；已知 ref 可隔离为干净 worktree，只有 baseline 含义不明或修复会覆盖用户产物时才询问。
- CPU set 无法并行隔离时默认串行，使用同一实际 affinity；若用户明确要求并行或固定核号，说明冲突后询问。
- tmux pane、build dir、结果目录可安全新建时直接隔离；不必询问是否先审计资源。

## 输出

返回两个 run slot、baseline source 状态、原始/实际 affinity、可用 CPU 证据和是否允许并行。无法保证 baseline 可信或资源隔离时，要求修复 baseline 或串行执行。
