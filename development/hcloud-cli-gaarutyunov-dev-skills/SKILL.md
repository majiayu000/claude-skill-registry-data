---
name: hcloud-cli
description: Use when interacting with Hetzner Cloud via command line - managing servers, networks, volumes, load balancers, firewalls, DNS, or any cloud infrastructure operations with hcloud CLI
---

# Hetzner Cloud CLI (hcloud)

## Overview

hcloud is the official CLI for Hetzner Cloud. Use it for quick operations, scripting, and CI/CD workflows. For complex automation or custom Go integrations, use the `hetzner:hcloud-go-sdk` skill instead.

## Quick Setup

```bash
# Install
brew install hcloud  # or: go install github.com/hetznercloud/cli/cmd/hcloud@latest

# Authenticate
hcloud context create myproject
# Enter your API token when prompted (from https://console.hetzner.cloud)
```

See `references/configuration.md` for multi-project and advanced setup.

## Quick Reference

| Task | Command |
|------|---------|
| **Servers** | |
| List servers | `hcloud server list` |
| Create server | `hcloud server create --name web --type cpx22 --image ubuntu-24.04` |
| SSH to server | `hcloud server ssh web` |
| Delete server | `hcloud server delete web` |
| Reboot/Reset | `hcloud server reboot web` / `hcloud server reset web` |
| **Networks** | |
| Create network | `hcloud network create --name private --ip-range 10.0.0.0/8` |
| Attach server | `hcloud server attach-to-network web --network private` |
| **Volumes** | |
| Create volume | `hcloud volume create --name data --size 100 --server web` |
| Attach volume | `hcloud volume attach data --server web --automount` |
| **Firewalls** | |
| Create firewall | `hcloud firewall create --name web-fw` |
| Add rule | `hcloud firewall add-rule web-fw --direction in --protocol tcp --port 80` |
| Apply to server | `hcloud firewall apply-to-resource web-fw --type server --server web` |
| **Load Balancers** | |
| Create LB | `hcloud load-balancer create --name lb --type lb11 --location fsn1` |
| Add target | `hcloud load-balancer add-target lb --server web` |
| **SSH Keys** | |
| Upload key | `hcloud ssh-key create --name mykey --public-key-from-file ~/.ssh/id_rsa.pub` |
| **DNS (Zones)** | |
| List zones | `hcloud zone list` |
| Create zone | `hcloud zone create --name example.com` |

## Command Categories

See `references/commands.md` for complete command reference:
- Servers (lifecycle, rescue, metrics, console)
- Networks, subnets, routes
- Volumes, storage boxes
- Firewalls and rules
- Load balancers, targets, services
- Floating IPs, primary IPs
- SSH keys, images, ISOs
- DNS zones and records
- Certificates, placement groups

## Output Formats

```bash
# JSON output for scripting
hcloud server list --output json | jq '.[] | select(.status == "running")'

# YAML output
hcloud server describe web --output yaml

# Go template formatting
hcloud server describe web --output format='{{.ServerType.Cores}} cores'

# Table customization
hcloud server list --output columns=id,name,status,ipv4
hcloud server list --output noheader
```

## Context Management (Multi-Project)

```bash
# Create contexts for different projects/tokens
hcloud context create production
hcloud context create staging

# Switch context
hcloud context use production

# List contexts
hcloud context list
```

## Common Patterns

```bash
# Create server with SSH key and private network
hcloud server create \
  --name web-01 \
  --type cpx22 \
  --image ubuntu-24.04 \
  --ssh-key mykey \
  --network private \
  --location fsn1

# Create firewall with rules file
hcloud firewall create --name web-fw --rules-file rules.json

# Bulk server creation
for i in {1..3}; do
  hcloud server create --name "node-$i" --type cx22 --image ubuntu-24.04
done

# Wait for server to be running
hcloud server create --name app --type cx22 --image ubuntu-24.04
while [[ $(hcloud server describe app -o format='{{.Status}}') != "running" ]]; do
  sleep 2
done
```

## Common Mistakes

| Problem | Solution |
|---------|----------|
| "context not set" | Run `hcloud context create <name>` and enter token |
| "resource not found" | Check `hcloud <resource> list` - might be in different project |
| Token expired | Update with `hcloud context create <name>` (same name replaces) |
| Wrong location | Use `--location fsn1` or `nbg1` or `hel1` explicitly |
| Server unreachable | Check firewall rules, ensure SSH port 22 is open |
| Volume not visible | Use `--automount` or mount manually via SSH |
