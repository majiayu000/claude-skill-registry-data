---
name: anti-lie
version: 0.1.0-rev13
description: Use when audited OpenClaw conversations or outgoing Feishu/Slack/channel messages contain concrete business numbers such as revenue, percentages, stock prices, contract values, costs, market share, or funding and need evidence checks plus red/yellow/green audit stamps after sends.
author: openclaw-community
license: Apache-2.0
platforms: [linux, macos]
homepage: https://github.com/lc198707/anti-lie
---

# Anti-Lie V0.1.0-rev13 Skill

Installs the Anti-Lie verifier, OpenClaw hook, and shadow worker so outbound channel messages with concrete business claims are checked for evidence and stamped with PASS/WARN/BLOCK-style audit tails.

## 何时使用本 Skill

Activate this skill when the user or workspace mentions:

- anti-lie, anti lie, audit stamp, 红黄绿审计, 小尾巴, anti-lie verify
- outgoing OpenClaw channel messages to Feishu, Slack, Discord, Telegram, or similar need evidence review
- concrete business numbers need receipts before sending: revenue, 营收, costs, percentages, growth rates, stock prices, contract values, funding, market share
- installing, verifying, repairing, rolling back, or uninstalling the anti-lie V4.4-rev5 hook/service on Linux or macOS nodes

Do not use it for general fact checking without OpenClaw outbound-message audit needs.

## 一键安装（顶层 install.sh）

From this skill directory:

```bash
bash install.sh
```

Useful options:

```bash
bash install.sh --dry-run
bash install.sh --port=17600
bash install.sh --workspace="$HOME/.openclaw/workspace"
bash install.sh --python=/path/to/python3
```

The wrapper checks Python >=3.10, OpenClaw config, backs up current hooks to `~/.openclaw/.anti-lie-backup-<timestamp>/`, dispatches to `package/_install-linux.sh` on Linux or `package/_install-macos.sh` on macOS, then runs `verify.sh`.

## 自检（verify.sh）

```bash
bash verify.sh
bash verify.sh --port=17600
```

`verify.sh` checks package structure, Python/Node/OpenClaw prerequisites, service health for the host OS, `/healthz`, a neutral `/verify` call, and the bundled 13-case acceptance suite when the service is running.

Expected installed-state result: `13/13 acceptance PASS` from the packaged verifier plus an overall success line.

## 卸载（uninstall.sh）

```bash
bash uninstall.sh
```

This stops Linux systemd user units or macOS launchd agents, kills the shadow worker/server processes, removes the installed anti-lie hook, and restores the newest `~/.openclaw/.anti-lie-backup-*` hooks backup when present.

## 配置

Environment variables used by the installer/runtime:

| Variable | Purpose | Default / Example |
|---|---|---|
| `ANTI_LIE_PORT` | verifier service port | `17600` |
| `ANTI_LIE_VERIFY_URL` | hook/worker verifier URL | `http://127.0.0.1:17600/verify` |
| `ANTI_LIE_SENTINEL_TARGET` | target for audit-tail delivery | node/channel specific |
| `ANTI_LIE_TAIL_FALLBACK_MS` | fallback wait before tail delivery | `30000` |
| `FEISHU_APP_ID` | Feishu app ID for tail delivery | node specific |
| `FEISHU_APP_SECRET` | Feishu app secret | node specific |
| `FEISHU_OPEN_ID` | Feishu recipient open_id | node specific |
| `FEISHU_CHAT_ID` | Feishu recipient chat_id | node specific |

See `docs/INSTALL-GUIDE.md` for the full node-by-node manual and troubleshooting commands.

## 故障排查

### Q1: Python <3.10 fails

Install Python 3.10+ first. macOS usually uses `brew install python@3.11`; Linux depends on the distribution package manager. Then rerun with `--python=/path/to/python3` if needed.

### Q2: Port 17600 is occupied

Use another port consistently:

```bash
ANTI_LIE_PORT=17600 bash install.sh --port=17600
bash verify.sh --port=17600
```

### Q3: Service starts but health check fails

Linux: inspect `systemctl --user status anti-lie-verify.service --no-pager` and `/tmp/verify_server-systemd.log`.
macOS: inspect `launchctl print gui/$(id -u)/ai.openclaw.anti-lie-verify` and `~/Library/Logs/anti-lie/verify-server.log`.

### Q4: Outgoing messages get no audit tail

Check the shadow worker and logs:

```bash
pgrep -af anti-lie-shadow-worker.js
tail -n 50 /tmp/anti-lie-audit.log
tail -n 50 /tmp/anti-lie-shadow.log
```

### Q5: Inbound user messages are audited

That indicates an old hook is still active. Reinstall this rev5 skill and confirm the active handler matches the package under `hooks/anti-lie-verify/handler.js`.
