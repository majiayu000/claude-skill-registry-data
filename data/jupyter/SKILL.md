---
name: jupyter
description: |
  JupyterLab ML/AI development environment management via Podman Quadlet.
  Supports multi-instance deployment, GPU acceleration (NVIDIA/AMD/Intel),
  token authentication, and per-instance configuration. Use when users need
  to configure, start, stop, or manage JupyterLab containers for ML development.
---

# Jupyter - ML/AI Development Environment

## Overview

The `jupyter` command manages JupyterLab instances for ML/AI development using Podman Quadlet containers. Each instance runs as a systemd user service with optional GPU acceleration.

**Key Concept:** Multi-instance support allows running multiple isolated JupyterLab environments simultaneously, each on different ports with different GPU configurations.

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Config | `ujust jupyter config [--instance=N] [--port=...] [--gpu-type=...]` | Configure instance N |
| Start | `ujust jupyter start [--instance=N\|all]` | Start instance(s) |
| Stop | `ujust jupyter stop [--instance=N\|all]` | Stop instance(s) |
| Restart | `ujust jupyter restart [--instance=N\|all]` | Restart instance(s) |
| Logs | `ujust jupyter logs [--instance=N] [--lines=...]` | View logs |
| Status | `ujust jupyter status [--instance=N]` | Show instance status |
| URL | `ujust jupyter url [--instance=N]` | Show access URL |
| Shell | `ujust jupyter shell [--instance=N] [-- CMD...]` | Open shell in container |
| Token enable | `ujust jupyter token-enable [--instance=N]` | Enable token auth |
| Token show | `ujust jupyter token-show [--instance=N]` | Show token |
| Token disable | `ujust jupyter token-disable [--instance=N]` | Disable token auth |
| Token regenerate | `ujust jupyter token-regenerate [--instance=N]` | Generate new token |
| Delete | `ujust jupyter delete [--instance=N\|all]` | Remove instance(s) and images |

## Parameters

| Parameter | Long Flag | Short | Default | Description |
|-----------|-----------|-------|---------|-------------|
| Instance | `--instance` | `-n` | `1` | Instance number (1, 2, 3...) |
| Port | `--port` | `-p` | `8888` | Web UI port |
| GPU Type | `--gpu-type` | `-g` | `auto` | GPU type: `nvidia`, `amd`, `intel`, `none`, `auto` |
| Image | `--image` | `-i` | (default image) | Container image |
| Tag | `--tag` | `-t` | `stable` | Image tag |
| Workspace | `--workspace-dir` | `-w` | (empty) | Mount to /workspace |
| Bind | `--bind` | `-b` | `127.0.0.1` | Bind address |
| Lines | `--lines` | `-l` | `50` | Log lines to show |

### Instance Numbering

- Instance 1: Port 8888 (default)
- Instance 2: Port 8889
- Instance N: Port 8887+N

## Configuration Examples

```bash
# Default: Instance 1, port 8888, auto-detect GPU
ujust jupyter config

# Instance 2 with custom port and NVIDIA GPU (long form)
ujust jupyter config --instance=2 --port=8889 --gpu-type=nvidia

# Instance 2 with custom port and NVIDIA GPU (short form)
ujust jupyter config -n 2 -p 8889 -g nvidia

# Instance 3 with AMD GPU
ujust jupyter config -n 3 -p 8890 -g amd

# No GPU acceleration
ujust jupyter config --gpu-type=none

# With workspace mount
ujust jupyter config --gpu-type=nvidia --workspace-dir=/home/user/projects

# Network-wide access
ujust jupyter config --bind=0.0.0.0

# Combine multiple options
ujust jupyter config -n 2 -p 8889 -g nvidia -b 0.0.0.0 -w /home/user/projects
```

### Update Existing Configuration

Running `config` when already configured will update the existing configuration, preserving values not explicitly changed.

### Shell Access

```bash
# Interactive bash shell
ujust jupyter shell

# Run specific command (use -- separator)
ujust jupyter shell -- pip list

# Shell in specific instance
ujust jupyter shell --instance=2 -- nvidia-smi

# Short form
ujust jupyter shell -n 2 -- nvidia-smi
```

## Lifecycle Commands

### Start/Stop/Restart

```bash
# Single instance (long form)
ujust jupyter start --instance=1
ujust jupyter stop --instance=1
ujust jupyter restart --instance=1

# Single instance (short form)
ujust jupyter start -n 1
ujust jupyter stop -n 1
ujust jupyter restart -n 1

# All instances
ujust jupyter start --instance=all
ujust jupyter stop --instance=all
ujust jupyter restart --instance=all
```

### View Logs

```bash
# Follow logs (instance 1 default)
ujust jupyter logs

# Specific instance
ujust jupyter logs --instance=1

# Last N lines (long form)
ujust jupyter logs --lines=100

# Last N lines (short form)
ujust jupyter logs -l 100 -n 2
```

### Get Access URL

```bash
ujust jupyter url
# Output: http://localhost:8888

# Specific instance
ujust jupyter url --instance=2
```

## Token Authentication

By default, JupyterLab requires no token for local development. Enable token auth for remote access or shared environments.

```bash
# Enable token (generates random token) - instance 1 default
ujust jupyter token-enable

# Enable token for specific instance
ujust jupyter token-enable --instance=2

# Show current token
ujust jupyter token-show --instance=1

# Disable token (password-less access)
ujust jupyter token-disable

# Generate new token
ujust jupyter token-regenerate --instance=1
```

## Configuration Files

| File | Purpose | Location |
|------|---------|----------|
| Quadlet unit | Service definition | `~/.config/containers/systemd/jupyter-1.container` |
| Instance config | Per-instance settings | `~/.config/jupyter/instance-1.env` |

## Volume Mounts

| Container Path | Host Path | Purpose |
|----------------|-----------|---------|
| `/workspace` | `$HOME` | User home directory |
| `/home/jovyan/.jupyter` | `~/.jupyter` | Jupyter config |

## Common Workflows

### Initial Setup

```bash
# 1. Configure JupyterLab with GPU support
ujust jupyter config --gpu-type=nvidia

# 2. Start the instance
ujust jupyter start

# 3. Get the URL
ujust jupyter url

# 4. Open in browser
# http://localhost:8888
```

### Multiple Environments

```bash
# PyTorch environment (instance 1)
ujust jupyter config --instance=1 --gpu-type=nvidia

# TensorFlow environment (instance 2)
ujust jupyter config -n 2 -p 8889 -g nvidia

# CPU-only data science (instance 3)
ujust jupyter config -n 3 -p 8890 -g none

# Start all
ujust jupyter start --instance=all

# List all
ujust jupyter list
```

### Remote Access

```bash
# Enable token for security
ujust jupyter token-enable

# Get token
ujust jupyter token-show
# Use: http://your-ip:8888/?token=<token>
```

## GPU Support

### Automatic Detection

```bash
ujust jupyter config  # Auto-detects GPU type
```

### Manual Selection

| GPU Type | Flag Value | Requirements |
|----------|------------|--------------|
| NVIDIA | `--gpu-type=nvidia` or `-g nvidia` | NVIDIA drivers + nvidia-container-toolkit |
| AMD | `--gpu-type=amd` or `-g amd` | ROCm drivers |
| Intel | `--gpu-type=intel` or `-g intel` | oneAPI runtime |
| None | `--gpu-type=none` or `-g none` | CPU only |

### Verify GPU Access

```bash
ujust jupyter shell -- nvidia-smi  # NVIDIA
ujust jupyter shell -- rocm-smi    # AMD
```

## Troubleshooting

### Instance Won't Start

**Symptom:** `ujust jupyter start` fails

**Check:**

```bash
# Check service status
systemctl --user status jupyter-1

# Check logs
ujust jupyter logs --lines=50
```

**Common causes:**

- Port already in use
- GPU not available
- Image not pulled

### GPU Not Detected

**Symptom:** No GPU acceleration in notebooks

**Check:**

```bash
# Verify GPU config
ujust jupyter status

# Test inside container
ujust jupyter shell -- nvidia-smi
```

**Fix:**

```bash
# Reconfigure with explicit GPU type
ujust jupyter delete
ujust jupyter config --gpu-type=nvidia
```

### Token Issues

**Symptom:** Can't access Jupyter, token required

**Fix:**

```bash
# Show current token
ujust jupyter token-show

# Or disable token for local use
ujust jupyter token-disable
```

### Port Conflict

**Symptom:** "Address already in use"

**Fix:**

```bash
# Find what's using the port
lsof -i :8888

# Use different port
ujust jupyter config --port=8889
```

## Cross-References

- **Related Skills:** `pod` (build images), `configure gpu` (GPU setup)
- **GPU Setup:** `ujust config gpu setup`
- **Documentation:** [Podman Quadlet Docs](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)

## When to Use This Skill

Use when the user asks about:

- "install jupyter", "setup jupyterlab", "ML development"
- "start jupyter", "stop jupyter", "restart jupyter"
- "jupyter not working", "jupyter won't start"
- "jupyter token", "jupyter password", "jupyter authentication"
- "jupyter GPU", "jupyter nvidia", "jupyter cuda"
- "multiple jupyter", "second jupyter instance"
