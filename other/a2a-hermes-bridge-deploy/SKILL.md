---
name: a2a-hermes-bridge-deploy
description: 部署 Hermes Agent 的 A2A 桥接 — 让两台 Hermes 通过 Google A2A 协议互相对话。涵盖服务端部署、客户端对接、systemd 自启、FRP/SSH 网络穿透。
---

# Hermes A2A 桥接部署经验

用 `a2a-adapter` 把 Hermes Agent 暴露为 A2A 协议服务，让两台 Hermes 互相对话。

## 核心工具

- **a2a-adapter** (`pip install a2a-adapter`) — 3 行代码把 Hermes 变成 A2A Server，内置 `HermesAdapter`
- **a2a-sdk** — Google A2A 协议的 Python SDK
- Hermes Agent 需要可导入 (`PYTHONPATH` 指向源码目录)

## 架构模式

```
Client (WSL) ──SSH Tunnel──▶ Server (Lab)
   client.py                     systemd: a2a-priestess.service
   systemd: a2a-tunnel.service   HermesAdapter :9010
```

**单向委托模式**（服务器在 FRP/NAT 后面时）：客户端通过 SSH 隧道访问服务器，服务器不需要访问客户端。

## 关键决策

### 1. 直接上行 → 选 a2a-adapter
Hermes 自身没有内置 A2A（只有 3 个待实现的 Feature Request），但 `hybroai/a2a-adapter` 提供了开箱即用的 `HermesAdapter`，直接用 `run_agent.AIAgent` + `SessionDB` 封装，和 Hermes gateway 同款模式。

### 2. 非流式模式更稳定
A2A 流式（SSE）在 SSH 隧道下不稳定 → 用 `blocking: true` 的 `message/send` 方法。流式等 FRP 直接端口转发后再启用。

### 3. AgentCard URL 覆盖
AgentCard 里的 `supportedInterfaces` URL 是服务器的 `localhost:9010`，客户端拿到的是不可达地址 → 需要用 protobuf API 覆盖：
```python
card.ClearField("supported_interfaces")
card.supported_interfaces.append(
    AgentInterface(protocol_binding="JSONRPC", url=tunnel_url)
)
```

## FRP/SSH 踩坑

### FRP 限流
- **现象**：连续 SSH 连接被 `Connection closed` 拒绝
- **解决**：每次 SSH 间隔 ≥ 10 秒；合并操作为单次 SSH 执行
- **文件上传**：用 base64 编码后单次 SSH 传输（绕开 SCP 协议干扰）
- **Systemd 保护**：`RestartSec=30` + `StartLimitIntervalSec=300`

### Fish Shell 兼容
远程 shell 是 fish，不支持：
- `<< HEREDOC` → 用 `bash -c` 或 base64 写文件
- `$!` (获取后台 PID) → 用 `bash -c` 或 `%last`
- `2>/dev/null` → 在 fish 中正常可用

### 隧道生命周期
- **开发期**：手动 `ssh -f -L 19010:localhost:9010 -N`
- **生产期**：systemd 用户服务 `a2a-tunnel.service`
- **保活**：`ServerAliveInterval=30` (30s 心跳)

## 部署清单

### Server 端 (Lab)

```bash
# 依赖
pip3 install --break-system-packages a2a-adapter openai

# 服务文件: ~/.config/systemd/user/a2a-priestess.service
# 关键: Environment=PYTHONPATH=%h/.hermes/hermes-agent
#       Linger=yes (无登录也运行)

systemctl --user daemon-reload
systemctl --user enable --now a2a-priestess
```

最小 server.py：
```python
import os,sys
p=os.path.expanduser("~/.hermes/hermes-agent")
if p not in sys.path:sys.path.insert(0,p)
from a2a_adapter import HermesAdapter,serve_agent
a=HermesAdapter(
    model="deepseek/deepseek-v4-flash",
    enabled_toolsets=["terminal","file","web","search"],
    name="女祭司",
    description="..."
)
serve_agent(a,host="0.0.0.0",port=9010)
```

### Client 端 (WSL)

```bash
# 隧道服务: ~/.config/systemd/user/a2a-tunnel.service
# ExecStart: ssh -N -L 19010:localhost:9010 ... -p35043

systemctl --user enable --now a2a-tunnel

# 调用
curl -s -X POST http://localhost:19010/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"message/send",...}'
```

## 故障排查

| 症状 | 检查 |
|------|------|
| Connection closed | FRP 限流，等 15s 再试 |
| 隧道不通 | `systemctl --user status a2a-tunnel` |
| 服务未响应 | Lab: `systemctl --user status a2a-priestess` |
| Agent 无法导入 hermes | `PYTHONPATH` 是否指向正确的 `hermes-agent/` 目录 |
| No module named 'openai' | `pip3 install --break-system-packages openai` |
| 任务超时 | 检查 server log: `~/.local/var/log/a2a-server.log` |
| 服务频繁重启 | FRP 限流触发了重试风暴，加长 `RestartSec` |
