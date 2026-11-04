---
name: microvm-agent
description: Manage agent microvms on a NixOS hypervisor host. Use when creating, listing, starting, stopping, or removing microvms that run isolated agent environments, or when planning resource allocation for agent workloads.
---

# Microvm Agent

Provision and manage NixOS microvms on a hypervisor host for running isolated agent environments. Each microvm is a declarative NixOS configuration built with [microvm.nix](https://github.com/astro/microvm.nix) and managed via SSH to the hypervisor host.

## Target Host

The hypervisor host is `nixos-ry4a` (8 cores, 32 GB RAM, x86_64-linux). All management happens over SSH: `ssh root@nixos-ry4a`.

## Resource Defaults

| Resource | Default | Notes |
|---|---|---|
| vCPUs | 2 | Adjustable per VM |
| RAM | 4096 MB | Adjustable per VM |
| Disk | 20 GB qcow2 | Stored under `/var/lib/microvms/<name>/` |
| Network | Tailscale only | Each VM gets its own tailscale identity |

**Budget**: With 32 GB RAM and 8 cores, a practical ceiling is ~6 concurrent VMs at default allocation (leaving headroom for the host).

## VM Profiles

There are two VM lifecycle profiles:

- **persistent**: VM state survives reboots. Disk is preserved. Suitable for long-running agents.
- **ephemeral**: VM is rebuilt from scratch on each start. Disk is discarded on stop. Suitable for one-off tasks.

## Workflow

### 1. Plan the VM

Before creating a VM, confirm these parameters with the user:

- **name**: unique identifier (e.g., `work-agent-1`, `personal-opencode`)
- **profile**: `persistent` or `ephemeral`
- **cpus**: number of vCPUs (default: 2)
- **ramMB**: memory in MB (default: 4096)
- **tailscaleAuthKey**: SOPS key path or ephemeral key for tailscale (required for network access)
- **baseConfig**: which agent config to use (e.g., a nix-agents profile, a repo URL)

Show the user the resource budget summary before proceeding.

### 2. Create the VM

SSH to `nixos-ry4a` and run the creation script:

```bash
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/create-vm.sh \
  --name <name> \
  --cpus <N> \
  --ram <MB> \
  --disk <GB> \
  [--ephemeral]
```

This script is installed on the host. Read `references/vm-lifecycle.md` for what the script does under the hood.

### 3. List VMs

```bash
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/list-vms.sh
```

Shows name, state, vCPUs, RAM, disk usage, and tailscale IP.

### 4. Start / Stop / Restart

```bash
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/manage-vm.sh start <name>
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/manage-vm.sh stop <name>
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/manage-vm.sh restart <name>
```

### 5. Remove a VM

```bash
ssh root@nixos-ry4a -- /var/lib/microvms/scripts/manage-vm.sh remove <name>
```

Warning: this deletes the disk image and all state. Confirm with the user before running.

## Declarative Path (Future)

Currently VMs are managed imperatively via scripts on the host. The declarative path uses `microvm.vms` in the host's NixOS config to define VMs as nix modules. When this is implemented, VMs will be rebuilt via `nixos-rebuild` and the scripts become wrappers around the declarative config. Read `references/declarative-roadmap.md` for the planned approach.

## Read These References As Needed

- `references/vm-lifecycle.md`: what each management script does, disk layout, tailscale integration
- `references/resource-budget.md`: capacity planning and allocation guidelines
- `references/declarative-roadmap.md`: planned migration from imperative scripts to declarative nix modules
