---
description: How to spawn a SolanaOS Gateway and connect headless nodes
---

# SolanaOS Gateway + Node Workflow

## Prerequisites

Ensure the following tools are installed:
- `tmux` — `brew install tmux`
- `tailscale` — https://tailscale.com/download
- `openclaw` — `npm install -g openclaw`
- `go` — https://go.dev/dl/

## Build SolanaOS

// turbo
```bash
cd /Users/8bit/solanaos && go build -ldflags="-s -w" -o build/solanaos .
```

## Spawn the Gateway (Quick)

### Option A: Via SolanaOS CLI

// turbo
```bash
./build/solanaos node gateway-spawn
```

This will:
1. Check for tmux, openclaw, and tailscale
2. Detect your Tailscale IP
3. Start `openclaw gateway` in a detached tmux session
4. Print connection info for remote nodes

### Option B: Via Shell Script

// turbo
```bash
./scripts/gateway-spawn.sh
```

Same result, but works without building SolanaOS first.

## Pair a Node

From the hardware device (Orin Nano, RPi, etc.), run:

```bash
./build/solanaos node pair --bridge <TAILSCALE_IP>:18790 --display-name "My Orin Nano"
```

Then approve from the gateway host:
```bash
openclaw nodes approve <requestId>
```

## Run the Node

```bash
./build/solanaos node run --bridge <TAILSCALE_IP>:18790
```

## Auto-Spawn at Daemon Launch

To make the daemon automatically spawn a gateway at startup:

```bash
GATEWAY_AUTO_SPAWN=true ./build/solanaos daemon
```

Or set in `.env`:
```
GATEWAY_AUTO_SPAWN=true
GATEWAY_SPAWN_PORT=18790
GATEWAY_USE_TAILSCALE=true
```

## Manage the Gateway

// turbo
```bash
# Check status
./scripts/gateway-spawn.sh --status

# Kill the gateway
./build/solanaos node gateway-kill

# Or via script
./scripts/gateway-spawn.sh --kill

# Attach to see gateway logs
tmux attach -t solanaos-gw
```

## Cross-Compile for Hardware

```bash
# Raspberry Pi (ARM64)
GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o build/solanaos-linux-arm64 .

# NVIDIA Orin Nano (ARM64)
GOOS=linux GOARCH=arm64 go build -ldflags="-s -w" -o build/solanaos-orin .
```

## Termius SSH Workflow

1. Add your Tailscale host in Termius (use Tailscale IP)
2. SSH in and run: `./build/solanaos node gateway-spawn`
3. From a second Termius tab: `./build/solanaos node run --bridge <IP>:18790`
