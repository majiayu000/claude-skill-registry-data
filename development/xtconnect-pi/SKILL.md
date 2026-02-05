---
name: xtconnect-pi
description: |
  Debug and manage XTConnect Raspberry Pi nodes with connection tracking, serial port debugging,
  and master image verification.
  Use when asked about: xtconnect, raspberry pi, pi node, serial port, rs-485, master image,
  debug pi, connect to pi, check deployment, monitor serial, validate master, node status.
---

# XTConnect Pi Node Management

Streamlined workflows for debugging and managing XTConnect Raspberry Pi nodes.

## Installation

```bash
# Install xtpi CLI to ~/.local/bin
./skills/xtconnect-pi/install.sh

# Add to PATH (add to ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

## Quick Start (xtpi CLI)

```bash
xtpi discover              # Find nodes on network
xtpi connect d9f50b55      # Connect by node ID
xtpi status                # Show current node status
xtpi test                  # Test connection
xtpi serial --live         # Monitor serial traffic
xtpi logs -f               # Follow container logs
xtpi fleet                 # Show all known nodes
xtpi ssh                   # Open SSH session
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `xtpi discover` | Find XTConnect nodes on network |
| `xtpi discover --scan` | Scan subnet for Pi devices (slower) |
| `xtpi connect <host>` | Connect to a node (sets context) |
| `xtpi connect -` | Switch to previous node |
| `xtpi status` | Show current node status |
| `xtpi test` | Test connection to current node |
| `xtpi serial` | Show serial port status |
| `xtpi serial --live` | Monitor serial via docker logs |
| `xtpi serial --raw` | Interactive serial session (picocom) |
| `xtpi serial --dump` | Raw hex dump from port |
| `xtpi logs` | View container logs |
| `xtpi logs -f` | Follow logs (tail -f) |
| `xtpi logs --level ERROR` | Filter by log level |
| `xtpi deploy` | Deploy to current node |
| `xtpi deploy --build` | Build and deploy |
| `xtpi fleet` | Show status of all known nodes |
| `xtpi config` | View remote configuration |
| `xtpi config --diff` | Compare remote vs local config |
| `xtpi config --pull` | Pull config from node |
| `xtpi ssh` | Open SSH session |
| `xtpi restart` | Restart container |

## Legacy Scripts (Alternative)

```bash
# Discover available nodes on network
python3 skills/xtconnect-pi/scripts/node_context.py --discover

# Connect to a node (sets context)
python3 skills/xtconnect-pi/scripts/node_context.py --set xtconnect-d9f50b55.local

# Check current context
python3 skills/xtconnect-pi/scripts/node_context.py

# Test SSH connection
python3 skills/xtconnect-pi/scripts/connect.py --test

# Check deployment status
python3 skills/xtconnect-pi/scripts/check_deployment.py

# Monitor serial port
python3 skills/xtconnect-pi/scripts/serial_monitor.py --live
```

## Network Discovery

XTConnect nodes use predictable mDNS hostnames for zero-configuration networking:

| Node Type | Hostname Pattern | Purpose |
|-----------|------------------|---------|
| Production | `xtconnect-{nodeid}.local` | Deployed field nodes |
| Master Image | `xtconnect-master.local` | Golden image for provisioning |

**Node ID Format**: 8-character hex string derived from Pi serial number (e.g., `d9f50b55`)

### Discovery Commands

```bash
# Auto-discover all nodes on network
python3 skills/xtconnect-pi/scripts/node-context.py --discover

# Output:
# Discovered Nodes:
#   xtconnect-d9f50b55.local (Production) - ONLINE
#   xtconnect-a1b2c3d4.local (Production) - ONLINE
#   xtconnect-master.local (Master Image) - ONLINE
#
# Total: 3 nodes
```

## Connection Management

### SSH Configuration

Default credentials:
- **User**: `pi`
- **Key**: `~/.ssh/id_rsa` (default) or specify with `--key-path`
- **Timeout**: 10 seconds

### Context Tracking

The skill maintains connection state in `.xtconnect/context.json` (project root, gitignored):

```bash
# Check current context
python3 skills/xtconnect-pi/scripts/node-context.py

# Output:
# Current Node: xtconnect-d9f50b55.local
#   Node ID: d9f50b55
#   Connection: CONNECTED
#   Last Seen: 2 minutes ago
#   Serial Port: /dev/xtconnect-serial

# Set explicit node
python3 skills/xtconnect-pi/scripts/node-context.py --set xtconnect-master.local

# View connection history
python3 skills/xtconnect-pi/scripts/node-context.py --history

# Switch to previous node
python3 skills/xtconnect-pi/scripts/node-context.py --set -
```

**Context Detection Priority:**
1. Environment variable: `XTCONNECT_NODE`
2. Explicit set via `--set`
3. Last connected node from context file
4. Auto-discovery (if single node found)

### Testing Connection

```bash
# Test SSH connection
python3 skills/xtconnect-pi/scripts/connect.py --test

# Output:
# Testing connection to xtconnect-d9f50b55.local...
#   SSH: ✓ Connected
#   Docker: ✓ Running
#   Container: ✓ xtconnect-node (RUNNING)
#   Serial: ✓ /dev/xtconnect-serial present
#
# Connection Status: HEALTHY

# Test with specific SSH key
python3 skills/xtconnect-pi/scripts/connect.py --test --key-path ~/.ssh/xtconnect_rsa

# Open interactive SSH session
python3 skills/xtconnect-pi/scripts/connect.py --ssh
```

## Master Image Verification

Streamlined workflow for validating master images before provisioning new nodes.

### Full Validation

```bash
# Run complete validation suite
python3 skills/xtconnect-pi/scripts/master-image-verify.py

# Output:
# Master Image Validation: xtconnect-master.local
# ===============================================
#
# System Checks:
#   ✓ SSH connection
#   ✓ Docker service running
#   ✓ Network configuration
#   ✓ Disk space (15.2 GB free)
#
# Application Checks:
#   ✓ Boot manager service active
#   ✓ Config directory structure
#   ✓ Serial port device exists
#   ✓ udev rules configured
#
# Deployment Checks:
#   ✓ Docker images present
#   ✓ Environment variables configured
#   ✓ Read-only filesystem toggleable
#
# Validation Result: PASSED
# Master image ready for provisioning
```

### Individual Checks

```bash
# Check specific components
python3 skills/xtconnect-pi/scripts/master-image-verify.py --check docker
python3 skills/xtconnect-pi/scripts/master-image-verify.py --check serial
python3 skills/xtconnect-pi/scripts/master-image-verify.py --check config
python3 skills/xtconnect-pi/scripts/master-image-verify.py --check network
```

### Integration with Project Scripts

The skill references existing deployment scripts in the xtconnect.nodeservice project:

| Script | Purpose | Location |
|--------|---------|----------|
| `deployment/validate-installation.sh` | QA checklist | Run by verify script |
| `deployment/provision-master-image.sh` | Create master | Reference only |
| `deploy.sh` | Deploy to Pi | Can trigger from skill |
| `dev.sh` | Local dev | Not Pi-related |

## Serial Port Debugging

Monitor and debug RS-485 serial communication with agricultural controllers.

### Port Configuration

XTConnect nodes use a FTDI USB-to-serial adapter with udev rule:

```
/dev/xtconnect-serial → /dev/ttyUSB0
```

**Default Settings**:
- Baud Rate: 19200
- Data Bits: 8
- Stop Bits: 1
- Parity: None
- Flow Control: None

### Port Status

```bash
# Check serial port status
python3 skills/xtconnect-pi/scripts/serial-monitor.py --status

# Output:
# Serial Port: /dev/xtconnect-serial
#   Status: OPEN (by xtconnect-node container)
#   Configuration:
#     Baud Rate: 19200
#     Data Bits: 8
#     Stop Bits: 1
#     Parity: None
#   Last Activity: 3 seconds ago
#   Device: FTDI FT232R (idVendor=0403, idProduct=6001)
```

### Live Monitoring

```bash
# Monitor serial traffic in real-time (via SignalR protocol trace hub)
python3 skills/xtconnect-pi/scripts/serial-monitor.py --live

# Output (live updating):
# Monitoring /dev/xtconnect-serial (19200 baud)
# Press Ctrl+C to stop
#
# [10:30:15.234] TX → 01 03 00 00 00 02 C4 0B
# [10:30:15.256] RX ← 01 03 04 00 19 00 32 3A 4F
# [10:30:16.234] TX → 01 03 00 02 00 02 64 0B
# [10:30:16.256] RX ← 01 03 04 00 64 00 78 FA 8C

# With ASCII interpretation
python3 skills/xtconnect-pi/scripts/serial-monitor.py --live --ascii

# With Modbus decoding
python3 skills/xtconnect-pi/scripts/serial-monitor.py --live --decode modbus
```

### Traffic Capture

```bash
# Capture to file for analysis
python3 skills/xtconnect-pi/scripts/serial-monitor.py --capture output.log --duration 60

# Output:
# Capturing serial traffic to output.log...
# Duration: 60 seconds
# Press Ctrl+C to stop early
#
# Capture complete:
#   Packets: 245
#   TX: 122 packets
#   RX: 123 packets
#   Duration: 60.02 seconds
#   File: output.log (12.4 KB)
```

### Common Serial Issues

| Symptom | Likely Cause | Debug Command |
|---------|--------------|---------------|
| No serial device | USB adapter not detected | `--status` to check device |
| Permission denied | Container lacks device access | Check docker-compose.yml |
| Garbled data | Wrong baud rate | Verify 19200 baud config |
| No traffic | Controller not connected | Physical connection check |
| Intermittent | Loose connection | Check USB/RS-485 cables |

## Deployment Verification

Check the health and configuration of deployed nodes.

### Deployment Status

```bash
# Full deployment check
python3 skills/xtconnect-pi/scripts/check-deployment.py

# Output:
# Deployment Status: xtconnect-d9f50b55.local
# ===========================================
#
# Container:
#   Image: xtconnect-node:latest
#   Status: RUNNING
#   Uptime: 1h 30m
#   Health: HEALTHY
#
# Configuration:
#   ✓ /data/config/appsettings.json
#   ✓ /data/config/node-info.json
#   Node ID: d9f50b55
#   Serial Port: /dev/xtconnect-serial
#
# Performance:
#   CPU: 12%
#   Memory: 45 MB / 512 MB
#   Disk: 2.3 GB / 15.2 GB free
#
# Recent Activity:
#   Last Poll: 5 seconds ago
#   Last Upload: 2 minutes ago
#   Errors (24h): 0
```

### Log Access

```bash
# View recent logs
python3 skills/xtconnect-pi/scripts/check-deployment.py --logs --lines 50

# Follow logs (tail -f style)
python3 skills/xtconnect-pi/scripts/check-deployment.py --logs --follow

# Filter logs by level
python3 skills/xtconnect-pi/scripts/check-deployment.py --logs --level ERROR

# Export logs for analysis
python3 skills/xtconnect-pi/scripts/check-deployment.py --logs --export logs.txt --since 24h
```

### Configuration Inspection

```bash
# View current configuration on Pi
python3 skills/xtconnect-pi/scripts/check-deployment.py --config

# Compare remote config with local project files
python3 skills/xtconnect-pi/scripts/check-deployment.py --config --diff
```

## Common Workflows

### Testing a New Master Image

```bash
# 1. Ensure master Pi is on network
python3 skills/xtconnect-pi/scripts/node-context.py --discover

# 2. Connect to master image
python3 skills/xtconnect-pi/scripts/node-context.py --set xtconnect-master.local

# 3. Run full validation
python3 skills/xtconnect-pi/scripts/master-image-verify.py

# 4. Check serial port
python3 skills/xtconnect-pi/scripts/serial-monitor.py --status

# 5. If all passes, image is ready for cloning
```

### Debugging a Field Node

```bash
# 1. Discover nodes on network
python3 skills/xtconnect-pi/scripts/node-context.py --discover

# 2. Connect to target node
python3 skills/xtconnect-pi/scripts/node-context.py --set xtconnect-d9f50b55.local

# 3. Check deployment status
python3 skills/xtconnect-pi/scripts/check-deployment.py

# 4. Monitor serial communication
python3 skills/xtconnect-pi/scripts/serial-monitor.py --live

# 5. Check logs for errors
python3 skills/xtconnect-pi/scripts/check-deployment.py --logs --level ERROR --since 24h
```

### Quick Context Switching

```bash
# Check where you're connected
python3 skills/xtconnect-pi/scripts/node-context.py

# Switch to different node (context persists)
python3 skills/xtconnect-pi/scripts/node-context.py --set xtconnect-a1b2c3d4.local

# Return to previous node
python3 skills/xtconnect-pi/scripts/node-context.py --set -

# View recent connection history
python3 skills/xtconnect-pi/scripts/node-context.py --history
```

## State Management

### Context File

The skill stores state in `.xtconnect/context.json` (project root):

```json
{
  "version": "1.0",
  "current_node": {
    "hostname": "xtconnect-d9f50b55.local",
    "node_id": "d9f50b55",
    "last_connected": "2025-12-14T10:30:00Z",
    "connection_status": "connected"
  },
  "ssh_config": {
    "key_path": "~/.ssh/id_rsa",
    "user": "pi",
    "timeout": 10
  },
  "recent_nodes": [
    {"hostname": "xtconnect-d9f50b55.local", "last_connected": "2025-12-14T10:30:00Z"},
    {"hostname": "xtconnect-master.local", "last_connected": "2025-12-13T15:00:00Z"}
  ]
}
```

**Git Integration:**
- `.xtconnect/` should be gitignored (local state only)
- Context is per-project
- No global configuration needed

### Configuration

```bash
# Set SSH key path
python3 skills/xtconnect-pi/scripts/node-context.py --config --key-path ~/.ssh/xtconnect_rsa

# Set connection timeout
python3 skills/xtconnect-pi/scripts/node-context.py --config --timeout 15

# View current config
python3 skills/xtconnect-pi/scripts/node-context.py --config
```

## Scripts Reference

| Script | Purpose | Key Commands |
|--------|---------|--------------|
| `node-context.py` | Connection tracking | `--discover`, `--set`, `--history` |
| `connect.py` | SSH connection | `--test`, `--ssh` |
| `master-image-verify.py` | Master image validation | `--check`, (default: full) |
| `serial-monitor.py` | RS-485 debugging | `--status`, `--live`, `--capture` |
| `check-deployment.py` | Deployment verification | `--logs`, `--config` |
| `pi_client.py` | SSH client library | (imported by other scripts) |

## Troubleshooting

### Connection Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `Could not resolve hostname` | mDNS not working | Check Pi is powered, try IP |
| `Permission denied (publickey)` | Wrong SSH key | Specify with `--key-path` |
| `Connection timed out` | Network issue | Check cables, firewall |
| `Host key verification failed` | Key changed | Remove from `~/.ssh/known_hosts` |

### Serial Port Issues

| Error | Cause | Fix |
|-------|-------|-----|
| `No such device` | USB adapter not detected | Check physical connection |
| `Permission denied` | Container lacks access | Check docker-compose devices |
| `Device busy` | Already open | Restart container |

### Deployment Issues

| Error | Cause | Fix |
|-------|-------|-----|
| Container not running | Deploy failed | Check `docker logs` |
| Config missing | Volume mount issue | Verify docker-compose.yml |
| Old version running | Deploy didn't restart | Manual `docker restart` |

## Related Resources

- XTConnect Node Service: `/Users/sean/source/projects/xtconnect.nodeservice`
- Deployment scripts: `deployment/` directory in project
- Reference docs: `skills/xtconnect-pi/references/`
