---
name: cinderx-hir-dump
description: Use when 在真实 pyperformance worker 上采集 CinderX HIR 或 jit.log。
---

# CinderX HIR Dump

HIR dump 必须贴近真实 worker 命令，不另造失真的简化命令。

## 规则

- 以 `pyperformance-worker-run` 返回的真实 worker 命令为基线。
- 先读取 `../using-cpython-optimize/references/pyperformance-env-contract.md`，确认 debug 变量只是在真实 worker 环境契约上增量叠加，并保留 `.pth`、worker venv 和 `cinderx.is_initialized()` 证据。
- 只增减 `PYTHONJITDUMPFINALHIR`、`PYTHONJITLOGFILE`、`PYTHONJITDUMPSTATS` 等 debug 变量。
- 保存 HIR dump、jit.log、stdout/stderr、exit status。
- 正式性能数据不能使用开启大量 dump 的结果。

## 输出

真实 worker 命令、debug 变量差异、HIR 路径、jit.log 路径、最后编译函数和无法采集原因。
