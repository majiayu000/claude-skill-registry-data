---
name: priestess-a2a
description: 调用实验室服务器上的女祭司（Hermes A2A Agent）。通过 A2A 协议实现本地 魔术师 ↔ Lab 女祭司 的 Agent-to-Agent 通信。用于 GPU 监控、服务器管理、ComfyUI 任务委托等。
---

# 女祭司 A2A 调用

通过 A2A（Agent-to-Agent）协议调用实验室服务器（4×A10, Ubuntu 24）上的 Hermes Agent「女祭司」。

## 架构

```
WSL (魔术师)                              Lab (女祭司)
a2a-tunnel.service                       a2a-priestess.service
  ssh -L :19010→:9010  ──FRP──▶           python3 a2a-server.py :9010
  (systemd, enabled)                       (systemd, enabled, linger=yes)
```

两端均为 systemd 用户服务，开机自启。

## 隧道管理

隧道通过 WSL 端 systemd 服务管理，开机自启：

```bash
# 状态
systemctl --user status a2a-tunnel

# 重启
systemctl --user restart a2a-tunnel

# 快速连通性检查
nc -z localhost 19010 && echo 通
```

## 调用女祭司

### Python client（推荐）
```bash
PRIESTESS_URL=http://localhost:19010 python3 ~/projects/hermes-a2a/client.py "<消息>"
```

### curl 直接调用
client.py 内部使用的模式。关键参数：`blocking: true`（非流式），`message/send` 方法。

```bash
curl -s -X POST http://localhost:19010/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"message/send","params":{
    "message":{"messageId":"msg-1","role":"user",
      "parts":[{"kind":"text","text":"<消息>"}],
      "contextId":"任意ID","kind":"message"},
    "configuration":{"acceptedOutputModes":["text"],"blocking":true}},
    "id":"1"}'
```

## 适用场景

| 场景 | 示例 |
|------|------|
| GPU 监控 | "帮我看 nvidia-smi" |
| 服务检查 | "ComfyUI 在运行吗" |
| 系统信息 | "磁盘空间、内存使用" |
| 任务委托 | "帮我下载这个数据集到 ~/datasets/" |
| **SSH 断连应急** | SSH 挂了但 A2A 还能通 → 通过女祭司诊断修复 SSH，详见 `references/emergency-ssh-recovery.md` |

## 服务端管理

女祭司运行在 Lab 的 systemd 用户服务中。SSH 进 Lab 后：

```bash
systemctl --user status a2a-priestess   # 状态
systemctl --user restart a2a-priestess  # 重启（Hermes 更新后）
tail -50 ~/.local/var/log/a2a-server.log  # 日志
```

## 故障排查

| 症状 | 排查 |
|------|------|
| 隧道不通 | `systemctl --user status a2a-tunnel`，FRP 可能限流，等 30s 自动重试 |
| Agent 报错 | 看 Lab 日志 `~/.local/var/log/a2a-server.log` |
| 响应超时 | 确认用的是 blocking 模式，非 streaming（SSE 在隧道下不可靠） |
| "Method not found" | 确认用的是 `message/send` 而非 `tasks/send` |
| Agent Card URL 不对 | Agent Card 里写的是 localhost:9010，客户端必须 override 为隧道地址 |
| **SSH 断连但 A2A 通** | A2A 是独立于 SSH 的后门。优先用 A2A 让女祭司诊断（`systemctl status sshd`、`ls -la ~/.ssh/`、`grep ListenAddress /etc/ssh/sshd_config`）。常见根因：`/home` 迁移后 `.ssh/authorized_keys` 丢失 + `PasswordAuthentication no` → 死锁。修复：从本地读取公钥，通过 A2A 写入服务器 `~/.ssh/authorized_keys`。详细流程见 `references/emergency-ssh-recovery.md` |

## 常见坑

- **FRP 限流**：FRP 隧道有连接频率限制。systemd RestartSec=30s 已处理。手动 SSH 到 Lab 需间隔 5-10s。
- **Fish shell**：Lab 用 fish，不支持 bash heredoc（`<<`）。传文件用 base64 编码。
- **Fish shell + SSH 命令执行**：`ssh user@host "command"` 时远程 fish 会解析命令，导致 bash 语法（引号、变量、管道）报错。绕行：`ssh user@host /bin/bash << 'SSHEOF' ... SSHEOF`（heredoc 在本地 bash 展开，远程用 bash 执行，不受 fish 影响）。
- **SCP 不可用**：fastfetch 欢迎横幅破坏 SCP 协议。用 `echo $B64 \| base64 -d > file` 代替。
- **Streaming 不可靠**：A2A SDK 的 SSE 流式模式在 FRP/SSH 隧道下不稳定，用 blocking 模式。
- **A2A 超时**：复杂任务可能超过 30s。超时后等 30s（FRP 限流间隔）再重试，或直接用 SSH 执行（如 SSH 已恢复）。
- **Bind mount 残留**：如果 `/home` 曾经是 bind mount（`/data/home/po` → `/home/po`），`mv /home /home.old` 会把挂载点也带过去。直接 `rm -rf /home.old` 会失败（挂载点无法删除）。必须 `umount` 后再删。检查：`mount | grep home.old`。
- **Bind mount 数据隐藏**：bind mount 会遮蔽底层目录的原有内容。`umount` 后底层内容重新可见，但若已在挂载状态下删除了目录，底层数据也随之丢失。恢复前先用 `mount` + `lsblk` 理解挂载拓扑。
- **从 /proc 抢救已删除文件**：如果进程还在运行但磁盘文件已被删除，可从 `/proc/PID/exe` 恢复二进制（`cp /proc/$PID/exe /target`），从 `/proc/PID/fd/` 恢复仍打开的数据文件。注意：Python 源码模块不在 fd 中，只能恢复二进制和数据文件。
- **WSL fish 配置不可直接移植到服务器**：WSL 的 `config.fish` 包含 oh-my-posh、npm、hermes CLI、openclaw completions 等桌面工具命令，服务器上不存在。移植时需精简为只保留 `fastfetch` 和 `fish_greeting`。
- **全栈灾难恢复**：当 hermes-agent 源码、skills、服务文件、a2a-server.py 全部丢失时（如 `/home` bind mount 迁移误删），需执行完整重建流程。详见 `references/full-agent-recovery.md`。
- **⚠️ 写配置文件必须先验证语法**：禁止凭记忆猜测选项。`tmux -f config new -d -s _test` 验证通过再写入。不确定的选项查 `man` 或文档，不要编造（`default-path` 在 tmux 1.9 已移除）。

## 参考文件

- `references/deployment.md` — 完整部署记录（systemd 服务文件、安装步骤、踩坑记录）
- `references/full-agent-recovery.md` — 全栈灾难恢复（hermes-agent 源码+skills+服务文件全部丢失时的重建流程）
- `references/emergency-ssh-recovery.md` — SSH 断连应急恢复流程（A2A 后门诊断 → 修复密钥 → 恢复访问）
- `templates/server.py` — 女祭司 A2A 服务脚本模板
- `templates/a2a-priestess.service` — systemd 服务文件模板
- `templates/a2a-tunnel.service` — WSL 隧道 systemd 服务文件模板
