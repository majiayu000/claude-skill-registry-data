---
name: Proxmox
description: Control VMs/containers in Proxmox VE via REST API.
requires:
  bins: []
  env: [PROXMOX_URL, PROXMOX_TOKEN]
---

# Proxmox

Manages nodes/VMs/LXC in your Proxmox cluster. Auth is via API token
(`user@realm!tokenid=value`). Read operations are unrestricted; lifecycle
operations are gated by `PROXMOX_ALLOW_WRITE=true`.

## Tools
- `status`
- `list_nodes` — nodes + status
- `list_vms(node?)` — QEMU VMs
- `list_containers(node?)` — LXC
- `vm_status(node, vmid, kind?)` — status/current. kind = qemu|lxc (default qemu)
- `vm_action†(node, vmid, kind?, action)` — action ∈ start|stop|shutdown|reboot|suspend|resume

## Setup
Create API token: Datacenter -> Permissions -> API Tokens.  
Set `PROXMOX_URL=https://pve.local:8006`, `PROXMOX_TOKEN=root@pam!mytoken=abc-...`  
If you use self-signed TLS: `PROXMOX_INSECURE_TLS=true`.
