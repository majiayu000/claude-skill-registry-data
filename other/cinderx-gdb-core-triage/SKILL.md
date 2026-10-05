---
name: cinderx-gdb-core-triage
description: Use when CPython/CinderX native crash 需要真实命令、core 和 gdb 栈取证。
---

# CinderX GDB/Core Triage

日志不能替代 native crash 证据。必须优先保留同一真实命令、`gdb bt full`、core dump 和寄存器信息。

如果容器内缺少 `gdb` 或相关取证工具，先读取 `../using-cpython-optimize/references/container-tooling-guidance.md`。允许补装 `gdb`、`ripgrep` / `rg`、`strace`、`perf`、`binutils`；补装前探测包管理器、DNS、代理、镜像源和 cache，网络慢时及时反馈。不要因为缺 `gdb` 就改用反复加日志替代 native 取证。

## 触发

- `SIGSEGV`
- `exit 139`
- `core dump`
- `SIGABRT`
- native assertion failure

## 最小证据

- 同一真实命令和关键环境变量
- stdout/stderr、exit status、日志路径
- `command -v gdb`；缺失时记录工具补装探测、安装命令、耗时和 exit status
- `gdb --args ...` 下的 `bt full`
- `info registers`
- 已有 core 时：`gdb <python> <core>`
- JIT 相关时补 `cinderx-hir-dump`

## 反问 Gate

- 真实命令、core 与 Python binary 先从日志、路径、时间和构建信息匹配；仍无法确定时询问缺失事实。
- 已授权复现/修复时可在隔离环境重跑并定向取证，保留原 core 与日志。
- 缺工具按 tooling 指南探测与补装；只有需额外权限、改变指定网络方案或超过预算时才询问。
- attach 会暂停其他任务或操作会破坏唯一现场时，确认具体动作的授权；离线分析继续。

## 输出

crash 签名、栈、关键 frame、寄存器、core 摘要、最强根因假设和下一步验证命令。
