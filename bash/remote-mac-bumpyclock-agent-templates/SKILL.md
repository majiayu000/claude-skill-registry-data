---
name: remote-mac
description: "Remote Macs: MacBook, Mac Studio, clawmac, Tailscale, SSH, OpenClaw."
---

# Remote Mac

Use when user says `MacBook`, `Mac Studio`, `framed`, Tailscale, or asks to run/check something on Aditya's Macs.

## Aditya's Devices

- Primary: MacBook Pro. Tailscale `adityas-macbook-pro-1`.
- Workhorse: Mac Studio. Local `adityas-macstudio` / `adityas-macstudio.local`; Tailscale `adityas-mac-studio`; prefer `adityasharma@adityas-macstudio.local`.
- Framed: arch linux, not `moltymac` when healthy. tmux session, details in `~/sysadmin` on that machine.

Manager repo truth: `/Users/adityasharma/Projects/manager/computers.yaml`, `agents.yaml`.

## Discovery

1. `tailscale status` → pick matching host.
2. Tailscale down / SSH timeout → LAN fallback:

```bash
dns-sd -B _ssh._tcp local
arp -a
```

3. Try mDNS `HOST.local`.
4. Mac Studio: prefer `steipete-macstudio.local` when Tailscale SSH times out.

## SSH Rules

Default non-interactive:

```bash
ssh -o RequestTTY=no -o RemoteCommand=none HOST 'COMMAND'
```

Local alias `adityas-mac-studio` auto-attaches tmux. For one-shot commands, use flags above.

Long-running/interactive → tmux on remote, obvious session name.

## OpenClaw Checks

Login shells for Homebrew/pnpm PATH:

```bash
ssh -o RequestTTY=no -o RemoteCommand=none steipete@steipete-macstudio.local \
  'zsh -lc "openclaw gateway status --json; openclaw channels status --json"'
```

Mac Studio / Molty healthy shape:

- `tmux list-sessions` includes `openclaw-gateway-watch-main`
- `ps axww` includes `pnpm gateway:watch --benchmark`
- `lsof -nP -iTCP:18789 -sTCP:LISTEN` shows listener `*:18789`
- `openclaw channels status --json` shows Discord `Molty`, Slack, Telegram connected

## Safety

- Don't assume host identity from stale IP; verify hostname/user.
- Don't print secrets from remote files/shells.
- Host unavailable after Tailscale + LAN fallback → report what was tried.
- OpenClaw on Peter's machines: follow repo docs/AGENTS; don't install/start/stop services unless asked.
