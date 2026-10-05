---
name: orca-deploy
description: "Orca WSL headless server, systemd unit, pairing extraction."
---

# Orca Deploy

Orca 的部署运维参考。

## WSL Headless Server + Windows GUI

WSL 跑 `orca serve`（headless），Windows Orca 桌面端做 UI，通过 localhost 自动转发连接。

### systemd user unit

`~/.config/systemd/user/orca-serve.service`：

```ini
[Unit]
Description=Orca headless serve (WSL)
After=network-online.target

[Service]
Environment="PATH=/home/po/.local/bin:/home/po/.npm-global/bin:/home/po/.cargo/bin:/opt/miniforge/condabin:/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin"
ExecStart=/home/po/.local/bin/orca-ide serve --port 6768 --json
StandardOutput=append:/home/po/.orca/serve.log
StandardError=append:/home/po/.orca/serve.log
Restart=on-failure
RestartSec=5
ProtectSystem=false
ProtectHome=false
PrivateTmp=true

[Install]
WantedBy=default.target
```

三坑（同 OmniRoute）：
1. 完整绝对 PATH — systemd user PATH 是空的。
2. `ProtectHome=false` — Orca 写 `~/.orca/`、`~/.config/orca/`。
3. `PrivateTmp=true` 没问题（Orca 不用 /tmp 持久化）。

```bash
systemctl --user daemon-reload
systemctl --user enable --now orca-serve.service
```

### 配对码提取

`orca serve --json` 输出完整配对 URL 到 stdout。但终端显示会打码 base64 段（`***`），`cat` 和 `read_file` 同样被截断。

**正确做法：Python json.loads() 解析日志行。**

```python
import json
with open("/home/po/.orca/serve.log") as f:
    for line in f:
        if "orca_server_ready" in line:
            data = json.loads(line[line.index('{'):line.rindex('}')+1])
            print(data["pairing"]["url"])  # 完整 URL
            break
```

### Windows 客户端连接

1. 装 Orca 桌面端 https://www.onorca.dev
2. Settings → Remote Orca Servers → Add Server
3. 粘贴配对 URL

WSL2 `localhostForwarding` 默认开启，Windows `127.0.0.1:PORT` 自动路由到 WSL。

### 健康检查

```bash
systemctl --user is-active orca-serve.service
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:39514/
orca-ide status --json
```

## Agent 发现

Orca 只自动检测已知 CLI：claude、codex、gemini、cursor、grok 等。**Hermes 不在内置列表。**

变通：创建 worktree 时 agent 类型选 "Command"，命令填 `hermes --tui`。

## 端口冲突

6768 被占时 `orca serve` 自动 fallback 到 OS 分配端口。日志里会有 `EADDRINUSE` 和 `boundEndpoint`。

## 参考文档

- [Remote Orca Servers](https://www.onorca.dev/docs/remote-servers)
- [Ways to run Orca](https://www.onorca.dev/docs/ways-to-run)
- `references/wsl-headless-transcript.md` — 完整部署命令记录
