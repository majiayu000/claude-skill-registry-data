---
name: openwebui
description: |
  Open WebUI AI chat interface management via Podman Quadlet. Provides a web UI
  for interacting with Ollama models. Use when users need to configure, start,
  or manage the Open WebUI service.
---

# Open WebUI - AI Chat Interface

## Overview

The `openwebui` command manages the Open WebUI service using Podman Quadlet containers. It provides a web-based chat interface for interacting with Ollama LLM models.

**Key Concept:** Open WebUI connects to Ollama via the `bazzite-ai` network using DNS (`http://ollama:11434`). Ensure Ollama is running before using Open WebUI.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust openwebui config` | Configure instance |
| Start | `ujust openwebui start` | Start service |
| Stop | `ujust openwebui stop` | Stop service |
| Restart | `ujust openwebui restart` | Restart service |
| Logs | `ujust openwebui logs` | View logs |
| Status | `ujust openwebui status` | Show status |
| URL | `ujust openwebui url` | Show access URL |
| List | `ujust openwebui list` | List instances |
| Shell | `ujust openwebui shell` | Container shell |
| Delete | `ujust openwebui delete` | Remove service |

## Named Parameters

All parameters use named syntax (e.g., `PORT=3001`):

| Parameter | Default | Description |
|-----------|---------|-------------|
| `ACTION` | (menu) | Action to perform |
| `PORT` | 3000 | Host port for web UI |
| `IMAGE` | `ghcr.io/open-webui/open-webui:main` | Container image |
| `BIND` | 127.0.0.1 | Bind address (127.0.0.1 or 0.0.0.0) |
| `INSTANCE` | 1 | Instance number or `all` |
| `LINES` | 50 | Log lines to show |
| `CMD` | (empty) | Shell command |

## Configuration

```bash
# Default configuration (port 3000, localhost only)
ujust openwebui config

# Custom port
ujust openwebui config PORT=3001

# Network-wide access (0.0.0.0)
ujust openwebui config BIND=0.0.0.0

# Combine parameters
ujust openwebui config PORT=3001 BIND=0.0.0.0

# GPU-optimized image
ujust openwebui config IMAGE=ghcr.io/open-webui/open-webui:cuda
```

### Update Existing Configuration

Running `config` when already configured updates the existing settings:

```bash
# Change only the bind address
ujust openwebui config BIND=0.0.0.0

# Update port without affecting other settings
ujust openwebui config PORT=3002
```

## Container Images

| Image | Description |
|-------|-------------|
| `ghcr.io/open-webui/open-webui:main` | Standard image (default) |
| `ghcr.io/open-webui/open-webui:cuda` | NVIDIA CUDA optimized |
| `ghcr.io/open-webui/open-webui:ollama` | Bundled with Ollama (not recommended) |

**Note:** GPU is auto-detected and attached regardless of image choice.

## Lifecycle Management

```bash
# Start Open WebUI
ujust openwebui start

# Stop service
ujust openwebui stop

# Restart (apply config changes)
ujust openwebui restart

# View logs (default 50 lines)
ujust openwebui logs

# View more logs
ujust openwebui logs LINES=200

# Check status
ujust openwebui status

# Show access URL
ujust openwebui url
```

## Multi-Instance Support

```bash
# Start all instances
ujust openwebui start INSTANCE=all

# Stop specific instance
ujust openwebui stop INSTANCE=2

# Delete all instances
ujust openwebui delete INSTANCE=all
```

## Shell Access

```bash
# Interactive shell
ujust openwebui shell

# Run specific command
ujust openwebui shell CMD="ls -la /app/backend/data"
ujust openwebui shell CMD="cat /app/backend/data/config.json"
```

## Network Architecture

Open WebUI uses the `bazzite-ai` bridge network for cross-container DNS:

```
+-------------------+     DNS      +-------------------+
|   Open WebUI      | -----------> |      Ollama       |
|   (openwebui)     |              |    (ollama)       |
|   Port 3000       |              |   Port 11434      |
+-------------------+              +-------------------+
         |                                  |
         +------ bazzite-ai network --------+
```

**Environment Variables (injected automatically):**

```
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_HOST=http://ollama:11434
JUPYTER_HOST=http://jupyter:8888
COMFYUI_HOST=http://comfyui:8188
```

## Network Binding

| Bind Address | Access | Use Case |
|--------------|--------|----------|
| `127.0.0.1` | Localhost only | Default, secure |
| `0.0.0.0` | All interfaces | Network access, Tailscale |

**Security Note:** Using `BIND=0.0.0.0` exposes the service to your network. Consider using Tailscale for secure remote access:

```bash
# Expose via Tailscale (secure)
ujust tailscale serve openwebui
```

## Data Persistence

| Path | Description |
|------|-------------|
| `~/.config/openwebui/<INSTANCE>/data` | Users, chats, settings |

Data persists across container restarts. Each instance has isolated data.

## Common Workflows

### Initial Setup

```bash
# 1. Ensure Ollama is running
ujust ollama start

# 2. Configure Open WebUI
ujust openwebui config

# 3. Start the service
ujust openwebui start

# 4. Access the web UI
ujust openwebui url
# Output: http://127.0.0.1:3000
```

### Remote Access Setup

```bash
# Configure for network access
ujust openwebui config BIND=0.0.0.0

# Start the service
ujust openwebui start

# Or use Tailscale for secure access
ujust tailscale serve openwebui
```

### Upgrade Container Image

```bash
# Stop service
ujust openwebui stop

# Update to new image
ujust openwebui config IMAGE=ghcr.io/open-webui/open-webui:main

# Restart
ujust openwebui start
```

## GPU Support

GPU is automatically detected and attached:

| GPU Type | Detection | Quadlet Config |
|----------|-----------|----------------|
| NVIDIA | `nvidia-smi` | `AddDevice=nvidia.com/gpu=all` |
| AMD | lspci | `AddDevice=/dev/dri` |
| Intel | lspci | `AddDevice=/dev/dri` |

Check GPU status:

```bash
ujust openwebui shell CMD="nvidia-smi"
```

## Troubleshooting

### Service Won't Start

```bash
# Check status
ujust openwebui status

# View logs
ujust openwebui logs LINES=100

# Check if Ollama is running
ujust ollama status
```

**Common causes:**

- Port 3000 already in use
- Ollama not running
- Container image not pulled

### Can't Connect to Ollama

**Symptom:** "No models available" in web UI

**Check:**

```bash
# Verify Ollama is running
ujust ollama status

# Test Ollama connection from Open WebUI container
ujust openwebui shell CMD="curl http://ollama:11434/api/tags"
```

**Fix:**

```bash
# Start Ollama first
ujust ollama start

# Restart Open WebUI
ujust openwebui restart
```

### Web UI Not Accessible

**Symptom:** Browser can't connect to `http://localhost:3000`

**Check:**

```bash
ujust openwebui status
ujust openwebui url
```

**Fix:**

```bash
# If using wrong bind address
ujust openwebui config BIND=127.0.0.1
ujust openwebui restart
```

### Clear Data and Start Fresh

```bash
# Delete everything
ujust openwebui delete INSTANCE=all

# Reconfigure
ujust openwebui config
ujust openwebui start
```

## Cross-References

- **Required:** `ollama` (Ollama must be running for models)
- **Related:** `jupyter` (ML development), `comfyui` (image generation)
- **Network:** Uses `bazzite-ai` network (shared with ollama, jupyter, comfyui)
- **Docs:** [Open WebUI GitHub](https://github.com/open-webui/open-webui)

## When to Use This Skill

Use when the user asks about:

- "install open webui", "setup chat interface", "web ui for ollama"
- "configure openwebui", "change port", "network access"
- "open webui not working", "can't see models", "connection error"
- "open webui logs", "debug open webui"
- "delete open webui", "uninstall"
