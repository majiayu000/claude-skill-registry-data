---
name: orca-server-deploy
description: "Headless Orca serve via systemd, pairing, WSL to Windows."
---

# Orca Headless Server 部署

`orca serve` 把 Orca 当无界面服务器跑。

## systemd user unit

模板 `templates/orca-serve.service`。三坑：完整 PATH、ProtectHome=false、PrivateTmp=true。

```bash
cp templates/orca-serve.service ~/.config/systemd/user/orca-serve.service
systemctl --user daemon-reload
systemctl --user enable --now orca-serve.service
```

## WSL → Windows 连接

WSL localhost 自动映射 Windows。`ws://127.0.0.1:PORT` 直达，不用 Tailscale/SSH。
Windows Orca → Settings → Remote Orca Servers → Add Server → 粘贴配对 URL。

## 配对 URL 提取

`orca serve` 输出截断配对码（`...`），但 `orca_server_ready` JSON 含完整 URL。
从 `~/.orca/serve.log` 提取：

```bash
grep orca_server_ready ~/.orca/serve.log | python3 -c "
import sys,json
d=json.loads(sys.stdin.read().split('{',1)[1])
print(d['pairing']['url'])
" > ~/.orca/pairing-url.txt
```

## 端口

默认 6768。被占自动 fallback。`--port` 强制指定。无害警告：D-Bus/Fontconfig/Codex ENOENT。
