---
name: remote-mac
description: >-
  Runs and checks things on a remote Mac over Tailscale or SSH: non-interactive commands, tmux
  sessions, and service checks. Use when work must happen on another Mac you are not sitting at.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# Remote Mac

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use when you need to run or check something on a remote Mac over Tailscale or SSH.

## Discovery

1. Start with `tailscale status` and pick the matching host.
2. If Tailscale is down or SSH times out, try LAN discovery:

```bash
dns-sd -B _ssh._tcp local
arp -a
```

3. Try mDNS names such as `HOST.local` when visible.

## SSH Rules

Use non-interactive SSH by default:

```bash
ssh -o RequestTTY=no -o RemoteCommand=none HOST 'COMMAND'
```

For long-running or interactive remote work, use tmux on the remote host:

```bash
ssh HOST 'tmux new-session -d -s work "long-command"'
ssh HOST 'tmux attach -t work'
```

## Login Shell for PATH

Use login shells on remote Macs so Homebrew and other tools are on PATH:

```bash
ssh -o RequestTTY=no -o RemoteCommand=none HOST 'zsh -lc "command"'
```

## Service Health Check Pattern

```bash
# Check launchd service
ssh HOST 'launchctl list | grep service-name'

# Check process
ssh HOST 'pgrep -af "process-name"'

# Check port listener
ssh HOST 'lsof -nP -iTCP:8080 -sTCP:LISTEN'

# Check tmux sessions
ssh HOST 'tmux list-sessions'
```

## Safety

- Do not assume host identity from a stale IP; verify hostname/user when possible.
- Do not print secrets from remote files or shells.
- If a host is unavailable after Tailscale + LAN fallback, say what was tried.
- Do not install/start/stop services unless explicitly asked.
