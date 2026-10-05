---
name: mcp-remote-desktop
description: |-
  Control a remote VM desktop through MCP servers — connect Hermes to
  Whonix, Ubuntu, or any Linux/Windows VM via SSH-tunneled MCP stdio
  or HTTP transports. Full desktop control: screenshots, mouse, keyboard,
  window management, clipboard, file access.
version: 1.0.0
author: the operator
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [mcp, remote-desktop, vm, whonix, ssh-tunnel, desktop-automation]
    category: mcp
    triggers: [whonix, vm control, remote desktop mcp, ssh mcp tunnel, mcp server desktop, virtual machine automation, remote gui control, xdotool mcp]
    related_skills: [native-mcp, building-mcp-servers, computer-use]
---

# MCP Remote Desktop — Control a VM through MCP

Connect Hermes to a remote virtual machine and give it full desktop
control — screenshots, mouse clicks, keyboard input, window management,
clipboard, and file access — via an MCP server tunneled over SSH or
HTTP.

This is distinct from the built-in `computer_use` tool (which drives
the **local** desktop). This skill covers connecting to a **remote** VM
(Whonix, Ubuntu, Windows Server, any reachable machine).

## When to Use

- You need to give Hermes control of a **Whonix** or other VM
- You want the agent to interact with a remote desktop's GUI apps
- You need automated testing on a headless VM with Xvfb/Xfce
- You want to isolate the agent's desktop actions from your host

## Architecture

```
Hermes (your machine)
  │
  ├─ config.yaml: mcp_servers → command: "ssh" args: [...]
  │     OR
  │  config.yaml: mcp_servers → url: "http://vm-ip:8000/mcp"
  │
  ▼
SSH tunnel / HTTP ──────────► VM (Whonix / Ubuntu / Windows)
                                  │
                                  ▼
                            MCP Server process
                            (Python / Node / Go)
                                  │
                                  ▼
                            Desktop automation stack
                            (xdotool, scrot, PyAutoGUI,
                             UIA, nut.js, …)
```

## Approach 1: SSH stdio tunnel (recommended for Linux VMs)

The cleanest approach — Hermes runs a command that SSHes into the VM,
launches an MCP server process there, and pipes stdio over the SSH
connection. No open ports, no extra daemons, built-in encryption.

### On the VM (setup once)

Install the Linux desktop automation stack:

```bash
sudo apt update
sudo apt install -y xdotool scrot wmctrl xclip x11-utils xautomation python3-pip
pip install mcp pillow
```

Write a lightweight MCP server using the `mcp` Python SDK that exposes
tools using `xdotool`, `scrot`, and `wmctrl` under the hood. See
`references/linux-desktop-mcp-server.py` for a complete example.

### On the host (Hermes config.yaml)

```yaml
mcp_servers:
  my-vm:
    command: "ssh"
    args:
      - "-i"
      - "/path/to/ssh_key"
      - "-o"
      - "StrictHostKeyChecking=no"
      - "user@vm-ip"
      - "python3 /home/user/mcp-server.py"
    timeout: 120
    connect_timeout: 30
```

After restart, Hermes auto-discovers the MCP tools as
`mcp_my_vm_click`, `mcp_my_vm_screenshot`, etc.

### Whonix-specific notes

- Whonix Workstation internal IP: `10.152.152.11` (reachable from the
  host, routes through the Gateway for Tor)
- Whonix Gateway internal IP: `10.152.152.10`
- SSH is already running on the Workstation — enable it via:
  ```bash
  sudo systemctl enable --now ssh
  ```
- Default user credentials are set during first-boot setup
- X11 forwarding is NOT needed — the MCP server runs directly on the
  Workstation's X server

## Approach 2: HTTP/S StreamableHTTP (when SSH is unavailable)

Run the MCP server on the VM as a web service, then point Hermes at it.

```bash
# On the VM
python3 mcp-server.py --transport sse --host 0.0.0.0 --port 8000
```

```yaml
# Hermes config.yaml
mcp_servers:
  my-vm:
    url: "http://vm-ip:8000/mcp"
    timeout: 120
```

**Security:** Add `--auth-key` and TLS if the VM is reachable over a
non-trusted network.

## MCP Servers You Can Deploy (ready-made)

### Linux / X11 (Whonix, Ubuntu, Debian)

| Server | Stars | Stack | Notes |
|--------|-------|-------|-------|
| `computer-control-mcp` (AB498) | 148⭐ | PyAutoGUI, OCR | Cross-platform, `uvx computer-control-mcp@latest` |
| `kwin-mcp` (isac322) | 29⭐ | KWin/Wayland, AT-SPI2 | KDE Plasma 6 only, 30 tools, virtual sessions |
| `taw-computer` (the-agents-work) | 8⭐ | Docker + Xfce + VNC | Full Ubuntu sandbox, browser, 30+ tools |
| Custom xdotool server | — | xdotool + scrot + Python | Simplest, most flexible, ~100 LOC |

### Windows (host or Windows VM)

| Server | Stars | Stack | Notes |
|--------|-------|-------|-------|
| `Windows-MCP` (CursorTouch) | 6.2K⭐ | UIAutomation, native | Most mature. 17 tools. `uvx windows-mcp serve` |
| `computer-control-mcp` (AB498) | 148⭐ | PyAutoGUI | Cross-platform, OCR built-in |
| `clawdcursor` (AmrDab) | 386⭐ | AX tree + OCR fusion | Semantic element targeting |
| `nutjs-windows-control` | — | nut.js, Node | `npx @nutjs/windows-control-mcp` |

### macOS (macOS VM)

| Server | Stars | Notes |
|--------|-------|-------|
| `macuse-mcp` (macuse-app) | 34⭐ | Calendar, Mail, Notes, any Mac app via AX |
| `desktop-pilot-mcp` (VersoXBT) | 10⭐ | 30-100x faster than screenshot-based |

## Privacy & Anonymity Model (Whonix Priority)

When controlling a Whonix VM — or any privacy-focused setup — the
architecture MUST guarantee these properties:

1. **No outbound connections from the MCP server.** The server only
   reads stdin and writes stdout (stdio) or responds to HTTP requests.
   It never phones home, sends telemetry, or makes callbacks.
2. **Torified by default.** Every network call made through the server's
   `shell()` or `run_command()` tools inherits Whonix's full Tor routing
   — no DNS leaks, no IP exposure, no WebRTC leaks. Include a
   `check_tor()` tool that verifies this at the start of every session.
3. **No persistent storage.** Screenshots go to `/tmp` and are deleted
   immediately after transfer. The server has no database, no log files,
   no state files. Every session starts clean.
4. **Isolated network.** The SSH tunnel runs over VirtualBox's Host-Only
   network (Whonix: 10.152.152.0/24). There is no route from this
   network to the internet — the Whonix Gateway enforces this.
5. **No agent-side network.** The AI agent itself never makes direct
   network calls to the VM's destination. All network activity for the
   agent's task happens inside Whonix, behind Tor.

### Verifying the privacy model (post-setup checklist)

```bash
# 1. Check Tor is active (run inside Whonix VM)
curl -s https://check.torproject.org/ | grep -q Congratulations && echo "TOR OK"

# 2. Verify no listening ports on the MCP server
ss -tlnp | grep -E '(python|mcp)' || echo "NO LISTENING PORTS — clean"

# 3. Confirm SSH tunnel is the only path
#    (From host: try reaching the MCP server directly, should fail)
nc -zv 10.152.152.11 8000 2>&1 | grep -q refused && echo "PORT NOT OPEN — tunnel-only access"

# 4. Test that a shell command actually routes through Tor
python3 -c "
import urllib.request, json
ip = json.loads(urllib.request.urlopen('https://httpbin.org/ip').read())['origin']
print(f'Exit IP: {ip} — should NOT be your real IP')
"
```

If any check fails, stop and diagnose before connecting the agent.
the operator's rule: **if anonymity can't be confirmed, the agent stays
disconnected.**

### Canonical implementation: whonix-mcp

The `pmb2/whonix-mcp` repo (private) is the complete production-grade
implementation of this pattern. Compared to the minimal script in
`scripts/linux-desktop-mcp-server.py`, it adds:

- **25 tools** vs 17 — full mouse/keyboard/window/clipboard/app/filesystem
- **FastMCP** — uses the modern FastMCP API instead of raw MCP SDK
- **Systemd service** — `setup.sh` installs and enables auto-start
- **check_tor() tool** — verifies Tor routing is active at runtime
- **Shell tool** — arbitrary commands inherit Whonix Tor
- **Screenshot as data URI** — returned as `data:image/png;base64,...`
- **Detailed privacy architecture** documented in README

```bash
# Deploy from this repo:
git clone https://github.com/pmb2/whonix-mcp
# Copy to Whonix VM, then:
sudo ./setup.sh                  # installs deps + systemd service

# Add to Hermes config.yaml:
mcp_servers:
  whonix-desktop:
    command: ssh
    args: ["-T", "-i", "~/.ssh/whonix_key", "user@10.152.152.11",
           "/opt/whonix-mcp/venv/bin/python",
           "/opt/whonix-mcp/server.py"]
    timeout: 300
    connect_timeout: 30
```

## Pitfalls

- **X11 vs Wayland:** Whonix/Kicksecure uses Xfce (X11). `xdotool`
  works perfectly. Wayland desktops need different tools (`ydotool`,
  `wtype`, `grim` for screenshots) or the `kwin-mcp` server.
- **SSH key auth:** Password auth with `sshpass` works but is fragile.
  Use SSH keys and set `StrictHostKeyChecking=no` or pre-add the
  host key.
- **VM firewall:** Whonix's firewall is restrictive. For HTTP transport,
  you may need to open a port. For stdio over SSH, no port changes
  needed — it tunnels through the existing SSH connection.
- **Multiple displays:** Some screenshot tools capture the first
  display only. Use `DISPLAY=:0 scrot` or specify `display=0` in
  tool args.
- **Environment filtering:** Hermes filters env vars when spawning
  MCP server subprocesses. If the server needs API keys, pass them
  in the `env:` config block — don't rely on the parent env.
- **Screenshot persistence:** Screenshots written to `/tmp` are
  automatically cleaned by the OS on reboot and by the MCP server
  after transfer. Never save screenshots to persistent storage
  unless explicitly asked — doing so violates the privacy model.
- **First-run dependency download:** `uvx`-based servers download
  70MB+ of deps on first run. Always pre-warm in a terminal before
  connecting to avoid MCP client timeout. Run `uvx computer-control-mcp@latest --help`
  or `pip install ..` before wiring to Hermes.

## Related

- `native-mcp` skill — how Hermes discovers and registers MCP tools
- `building-mcp-servers` skill — how to author MCP servers from scratch
- `computer-use` skill — controls the **local** desktop (cua-driver)
- `references/` directory in this skill — detailed session findings
