---
name: hetzner-vnc-screenshot
description: Take and view screenshots of Hetzner Cloud servers via WebSocket VNC console
---

# Hetzner VNC Screenshot Skill

This skill captures screenshots of Hetzner Cloud servers by connecting to the WebSocket-based VNC console.

## Instructions

When asked to take a screenshot or view the console of a Hetzner Cloud server:

### Option 1: By Server Name (Recommended)

Requires `HCLOUD_TOKEN` environment variable:

```bash
uv run ~/.claude/skills/hetzner-vnc-screenshot/vnc-screenshot.py my-server-name --output /tmp/screenshot.png
```

### Option 2: With Explicit Credentials

If you already have the WebSocket URL and password:

```bash
uv run ~/.claude/skills/hetzner-vnc-screenshot/vnc-screenshot.py --url '<wss_url>' --password '<password>' --output /tmp/screenshot.png
```

### Step 2: View Screenshot

Use the Read tool to view `/tmp/screenshot.png`

## Examples

**Taking screenshot of server "talos-vps-0":**

```bash
# One command (uses HCLOUD_TOKEN from environment)
uv run ~/.claude/skills/hetzner-vnc-screenshot/vnc-screenshot.py talos-vps-0 --output /tmp/talos-vps-0.png
```

Then use Read tool to view `/tmp/talos-vps-0.png`

**With custom API token:**

```bash
uv run ~/.claude/skills/hetzner-vnc-screenshot/vnc-screenshot.py talos-vps-0 --token <api-token> --output /tmp/screenshot.png
```

## CLI Options

```
Arguments:
  server          Server name (requires HCLOUD_TOKEN env var)

Options:
  --url           WebSocket URL (alternative to server name)
  --password      VNC password (required with --url)
  --token         Hetzner API token (default: HCLOUD_TOKEN env)
  --output        Output image path (default: screenshot.png)
```

## Use Cases

- Debugging Talos Linux boot issues
- Viewing console output when network is unreachable
- Checking boot progress, kernel messages
- Diagnosing servers stuck in maintenance mode
- Viewing GRUB menu or BIOS/UEFI screens

## Technical Details

- Connects via secure WebSocket (wss://)
- Uses asyncvnc library for RFB (VNC) protocol
- Supports VNC password authentication
- Captures framebuffer and saves as PNG
- Dependencies auto-installed by uv: asyncvnc, pillow, typer, hcloud, websockets

## Notes

- Requires `hcloud` CLI or `HCLOUD_TOKEN` environment variable
- Console credentials are fetched automatically when using server name
- Works with any Hetzner Cloud server (not just Talos)
- Screen resolution is determined by the server's console settings
