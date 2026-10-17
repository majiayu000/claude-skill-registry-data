---
name: k3s
description: >
  K3s lightweight Kubernetes: server flags, service management,
  node operations, kubeconfig, and upgrade procedures for ARM64 clusters.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, k3s, arm64, raspberry-pi, cluster]
---

# K3s Skill

## Cluster Context

Single-node K3s cluster on Raspberry Pi CM4 (ARM64), Ubuntu 24.04.

Node: `srv-rk1-01` / `cm4-unknow-3` at `192.168.178.133`
Version pinned in: `roles/install-k3s/defaults/main.yml`
SSH: `ssh dalmine@192.168.178.133`

## Active Server Flags

```
--flannel-backend=none        # Cilium handles CNI
--disable-network-policy      # Cilium handles network policy
--disable-kube-proxy          # Cilium handles kube-proxy (BPF)
--disable servicelb           # MetalLB handles LoadBalancer
--disable traefik             # not used
--disable metrics-server      # not used
--disable-cloud-controller    # bare metal, no cloud
--write-kubeconfig-mode 644
--token <token>
```

> **Note:** `--disable local-storage` was previously set but has been removed.
> `local-path-provisioner` is re-enabled to provide PVC storage for Pi-hole.
> See "Local Storage (local-path-provisioner)" section below.

## Local Storage (local-path-provisioner)

K3s ships with `local-path-provisioner` built-in. It was previously disabled
but is required for Pi-hole (PVC for DNS data persistence).

**StorageClass:** `local-path` (default after re-enabling)

Verify it is active:
```bash
kubectl get storageclass
kubectl get pods -n kube-system -l app=local-path-provisioner
```

If you need to disable it again (e.g., migrating to a different storage solution):
1. Add `--disable local-storage` back to `k3s_server_exec` in `roles/install-k3s/defaults/main.yml`
2. Uninstall + reinstall K3s (flag changes require reinstall — see "Changing Server Flags")

## Changing Server Flags

Flags are set via `INSTALL_K3S_EXEC` env var at install time — they become
part of the systemd unit `/etc/systemd/system/k3s.service`.

To change flags after install:
1. Edit `k3s_server_exec` in `roles/install-k3s/defaults/main.yml`
2. Uninstall and reinstall: `ansible-playbook playbooks/uninstall.yml && ansible-playbook playbooks/bootstrap.yml`
   — or — manually patch the service file and `systemctl daemon-reload && systemctl restart k3s`

## Service Management (on the node)

```bash
# Status
sudo systemctl status k3s

# Restart
sudo systemctl restart k3s

# Live logs
sudo journalctl -u k3s -f

# Last 100 lines
sudo journalctl -u k3s --no-pager -n 100

# K3s CLI (runs kubectl with embedded kubeconfig)
sudo k3s kubectl get nodes
sudo k3s kubectl get pods -A
```

## kubeconfig

K3s writes kubeconfig to `/etc/rancher/k3s/k3s.yaml` (root-owned).
The `get-kubeconfig` Ansible role fetches it to `~/.kube/config` on localhost,
replacing `127.0.0.1` with `192.168.178.133`.

```bash
# Re-fetch kubeconfig manually
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
  --start-at-task "Make sure ~/.kube directory exists"
```

## Upgrade Procedure

1. Check latest release: https://github.com/k3s-io/k3s/releases
2. Verify compatibility matrix (K3s version ↔ Cilium version)
3. Update `k3s_version` in `roles/install-k3s/defaults/main.yml`
4. Drain node (single-node: skip or `kubectl cordon` only)
5. Uninstall + reinstall:
   ```bash
   ansible-playbook playbooks/uninstall.yml -i inventory/hosts.ini
   ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini
   ```
6. Verify: `kubectl get nodes` shows new version

## Troubleshooting

### Node `NotReady` after K3s start
- Expected if CNI (Cilium) not yet installed — `NetworkUnavailable=True`
- Check: `kubectl describe node | grep NetworkUnavailable`
- Fix: run install-cilium role

### K3s crashlooping
```bash
sudo journalctl -u k3s -n 50 --no-pager
sudo systemctl status k3s
```
Common causes:
- Port conflict: another process on 6443
- Disk full: `df -h` on node
- Bad flags: check `/etc/systemd/system/k3s.service` ExecStart line
- Leftover state after failed uninstall: check `/var/lib/rancher`, `/run/k3s`

### `kubectl` permission denied on node
- K3s kubeconfig at `/etc/rancher/k3s/k3s.yaml` is root-only by default
- Fix: `--write-kubeconfig-mode 644` is already in server flags
- Or use: `sudo k3s kubectl ...`

### Add a new agent node
1. Add new host to `[agent_nodes]` in `inventory/hosts.ini`
2. Ensure `k3s_token` matches the server token
3. Run: `ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini`
   — agent-only tasks are gated on `'agent_nodes' in group_names`

## Useful Commands

```bash
# Verify K3s server flags live
sudo systemctl cat k3s

# Check K3s binary version on node
ssh dalmine@192.168.178.133 'k3s --version'

# All running containers via containerd (K3s embeds containerd)
ssh dalmine@192.168.178.133 'sudo k3s ctr containers list'

# Token (needed for joining agents)
ssh dalmine@192.168.178.133 'sudo cat /var/lib/rancher/k3s/server/node-token'
```
