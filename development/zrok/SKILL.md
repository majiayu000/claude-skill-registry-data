---
name: zrok
description: Share local services publicly or privately via secure tunnels. Use when needing to expose localhost ports, share dev servers, create public URLs for local services, or set up secure tunnels between machines.
---

# zrok - Secure Sharing

Share local services via secure tunnels using a self-hosted zrok instance.

## Quick Reference

| Command | Description |
|---------|-------------|
| `zrok share public http://localhost:PORT` | Share publicly, get https URL |
| `zrok share private http://localhost:PORT` | Share privately, get token |
| `zrok access private TOKEN` | Connect to private share |
| `zrok status` | Check current configuration |
| `zrok reserve public --unique-name NAME` | Reserve persistent subdomain |

## Public Sharing

Expose a local service with a public HTTPS URL:

```bash
# Share a web server
zrok share public http://localhost:3000
# Returns: https://xyz123.z.spamt.net

# Share a directory as file server
zrok share public --backend-mode web /path/to/files

# Share with reserved name (persistent URL)
zrok reserve public http://localhost:3000 --unique-name myapp
zrok share reserved myapp
# Always: https://myapp.z.spamt.net
```

## Private Sharing

Share only with other zrok users (end-to-end encrypted):

```bash
# Machine A - share
zrok share private http://localhost:3000
# Returns token: abc123xyz

# Machine B - access  
zrok access private abc123xyz
# Creates: http://127.0.0.1:9191 -> Machine A's localhost:3000
```

## Setup New Machine

```bash
# Install (macOS)
brew install zrok

# Install (Linux)
curl -sSLf https://get.openziti.io/install.bash | sudo bash -s zrok

# Configure endpoint (one-time)
zrok config set apiEndpoint https://z.spamt.net

# Enable with account token (one-time per machine)
# Get token from admin or web console
zrok enable <token>
```

## Web Console

https://z.spamt.net - View active shares, manage account, get enable tokens

## Troubleshooting

```bash
# Check if enabled
zrok status

# Re-enable if issues
zrok disable
zrok enable <token>

# Verify connectivity
curl https://z.spamt.net/api/v1/version
```
