---
name: cinderx-remote-lab-ops
description: Use when 通过 SSH/tmux/rsync/docker compose 操作远程 CPython/CinderX lab，或诊断远端卡顿。
---

# CinderX Remote Lab Ops

远端操作必须服务于 CPython/CinderX lab，不是通用 SSH 技巧。

## 标准对象

- workspace：当前 Agent 独立宿主机目录。
- tmux：按任务固定 session/window/pane。
- docker compose：只操作 `cinderx-test` / `cpython-baseline`。
- logs：每个构建、安装、测试、benchmark 都有日志路径。

## 输出契约

每条远程命令第一次运行就记录真实命令、stdout/stderr、exit status、日志路径和 tmux pane。长任务必须有 `timeout` 或进度检查策略。

```bash
set -o pipefail
<command> 2>&1 | tee logs/<task>.log
status=${PIPESTATUS[0]}
printf '\n[exit status=%s]\n' "$status"
exit "$status"
```

## 异常处理

- 无输出：查进程、tmux capture-pane、日志、CPU/IO/磁盘。
- 网络慢：查 DNS、代理、pip mirror、git 连接和 cache。
- 容器内缺少 `gdb`、`rg` / `ripgrep`、`strace`、`perf`、`binutils` 等排障工具时，先读取 `../using-cpython-optimize/references/container-tooling-guidance.md`，探测网络、包管理器、镜像源和 cache，再决定补装；不要直接绕开关键取证路径。
- 在原预算内执行有界诊断和恢复；只有新的资源或权限取舍无法确定时询问用户。

不要为了补输出盲目重复构建、安装或 benchmark。

## 反问 Gate

- 正常推进的任务沿用已知预算和 timeout/进度策略；没有新证据时不重复启动。
- 卡顿先查进程、tmux、日志、exit status、DNS/代理/镜像源/cache，并尝试授权范围内可逆恢复。
- 只有需改变明确指定的网络方案、超出预算、终止其他任务、覆盖日志或执行未授权的有副作用重跑时才询问。
- 恢复失败时报告已查证的阻塞点、可用产物和最小下一步；继续独立的只读工作。
