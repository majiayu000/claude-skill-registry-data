---
name: fleet-manager
description: >
  Multi-machine fleet operations — SSH key management, cross-host syncing,
  Ansible playbook execution, fleet health checks, and inventory management.
  Trigger on: "fleet", "SSH to", "sync to", "cross-host",
  "deploy to", "rsync", "fleet health", "all machines", "inventory", or any
  task involving coordination between multiple hosts or infrastructure nodes.
---

# Fleet Manager

Coordinate operations across a multi-machine infrastructure fleet: primary nodes, GPU hosts, mining nodes, and additional infrastructure as needed.

## Fleet Inventory

| Host | IP | Role | SSH | OS |
|---|---|---|---|---|
| primary-host | <internal-ip-1> | Orchestration, fullnode, relay, monitoring | key auth | Ubuntu 24.04 |
| gpu-host | <internal-ip-2> | GPU cluster, container orchestration, AI workloads | key auth | Ubuntu 24.04 |
| worker-host-1 | <internal-ip-3> | Worker node, inference, container workloads | key auth | Ubuntu 24.04 |
| worker-host-2 | <internal-ip-4> | Mining node, accelerated workloads | key auth (pending) | OS TBD |

## SSH Access

- All hosts use key-only auth (no passwords)
- Keys: `~/.ssh/id_ed25519` on each host
- primary-host ↔ gpu-host: bidirectional key auth established
- worker-host-1: key auth from gpu-host established. primary-host → worker-host-1 may need host key acceptance.
- worker-host-2: pending initial configuration

## Cross-Host Operations

### Sync Configuration
```bash
# primary-host → gpu-host
rsync -avz --exclude='.env.local' --exclude='.secrets.map' \
  <config-source>/ admin_user@<gpu-host-ip>:~/<config-dest>/
ssh admin_user@<gpu-host-ip> "cd ~/<config-dest> && ./scripts/install.sh"

# gpu-host → primary-host (pull changes)
rsync -avz --exclude='.env.local' --exclude='.secrets.map' \
  admin_user@<gpu-host-ip>:~/<config-dest>/ <config-source>/
```

### Remote Command Execution
```bash
ssh admin_user@<gpu-host-ip> "command here"              # gpu-host
ssh admin_user@<primary-host-ip> "command here"          # primary-host (from gpu-host)
ssh admin_user@<worker-host-ip> "command here"           # worker node
```

### Fleet Health Check
```bash
# Create a hosts file with your fleet IPs/hostnames
for host in <primary-host> <gpu-host> <worker-host-1> <worker-host-2>; do
    echo "=== $host ==="
    ssh -o ConnectTimeout=3 admin_user@$host "hostname && uptime && free -h | head -2" 2>/dev/null || echo "UNREACHABLE"
done
```

## Rules

- Always use `127.0.0.1` not `localhost` on all hosts
- GPU nodes may require password authentication; primary nodes typically use NOPASSWD sudoers
- Primary orchestration host is NOT a miner — never deploy mining workloads there
- Maintain an Ansible inventory file with all hosts and their roles
- Use VPN/Tailscale for secure cross-network access between non-contiguous networks
- When syncing configuration, use version control repos — not raw `cp` or inline edits

## Sudoers Differences

| Host Type | sudo | Notes |
|---|---|---|
| Primary orchestration | NOPASSWD (scoped to specific commands) | Enables automated operations; config in /etc/sudoers.d/ |
| GPU worker | password required | Use `echo "$PASS" \| sudo -S` for scripting or interactive prompt |
| Additional workers | password required | Same as GPU worker; consider key-based sudo for automation |
| Mining nodes | TBD | Configure per deployment; recommend scoped NOPASSWD for mining ops only |
