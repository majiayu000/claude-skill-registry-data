---
name: homelab
description: Operate and deploy the homelab managed by this repo. Use when changing or validating NixOS hosts, k3s cluster nodes, declarative microVMs, remote deploys, kubeconfig-backed cluster operations, or host-level troubleshooting across nixos-ry4a, nixos-ry6a, and related homelab systems.
---

# Homelab

Use this skill for homelab work that spans host config, k3s, and microVMs.

## Workflow

1. Identify the target surface before changing anything:
   - `nixos-ry4a` for the microVM hypervisor and assistant VMs
   - `nixos-ry6a` for the primary k3s server
   - `nixos-ry6b` for the secondary k3s agent config
   - cluster-level Kubernetes resources via local kubeconfig tooling
2. Prefer declarative repo changes over imperative host edits.
3. Validate locally before any deploy.
4. Deploy only the affected host(s), then run the smallest useful verification on-host or in-cluster.
5. If a task is microVM-specific, load the microVM reference instead of rediscovering host layout and commands.

## Read These References As Needed

- `references/topology.md`: host roles, source-of-truth files, and current caveats
- `references/deploy-and-verify.md`: validation, deploy, and verification commands
- `references/microvms.md`: `nixos-ry4a` microVM layout, assistant VMs, and checks

## Working Rules

- Treat Nix files in this repo as the source of truth; avoid hand-editing remote hosts except for inspection or emergency recovery.
- Prefer `nix flake check --no-build` and targeted `nix build`/`nix eval` before remote activation.
- For cluster tasks, verify whether the change belongs in host Nix config or in Kubernetes resources before acting.
- Mention blast radius explicitly when a change affects the hypervisor, cluster bootstrap, secrets, ingress, or multiple hosts.
- Assume `nixos-ry6b` config is real but operationally degraded until the hardware is back in service.
