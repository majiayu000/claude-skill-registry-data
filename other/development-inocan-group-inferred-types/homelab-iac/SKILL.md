---
name: homelab-iac
description: Use when working with Proxmox homelab infrastructure - Terraform provisioning, Ansible configuration, or Nix devshells. Covers LXC containers, services, secrets, and IaC workflows.
---

# Homelab Infrastructure as Code

## Overview

This is a Proxmox homelab managed as Infrastructure as Code. **All changes go through Terraform or Ansible. SSH is read-only for debugging.**

| Change Type | Tool |
|-------------|------|
| Container specs (CPU, memory, disk, mounts) | Terraform |
| Software, packages, config files, services | Ansible |
| Development environment | Nix devshells |

## Quick Reference

### Containers

| CTID | Host | IP | Purpose |
|------|------|-----|---------|
| 300 | backup | .120 | Restic backups |
| 301 | samba | .121 | SMB shares |
| 302 | ripper | .131 | MakeMKV (optical drive) |
| 303 | analyzer | .133 | FileBot, media tools |
| 304 | transcoder | .132 | FFmpeg (Intel Arc GPU) |
| 305 | jellyfin | .130 | Media server (dual GPU) |
| 310 | dns | .110 | AdGuard Home |
| 311 | proxy | .111 | Caddy reverse proxy |
| 320 | devbox | .140 | NixOS dev environment |

**SSH:** Use aliases from `~/.ssh/config` (e.g., `ssh ripper`, `ssh jellyfin`).

### Directory Structure

```
terraform/
  proxmox-homelab/   # LXC containers (one .tf per container)
  tailscale/         # VPN configuration
  cloudflare/        # DNS records
  lldap/             # LDAP users/groups

ansible/
  playbooks/         # Service playbooks
  roles/             # Reusable roles
  vars/*_secrets.yml # Vault-encrypted secrets

nixos/               # Devbox NixOS config
flake.nix            # Nix devshells
```

### Secrets

| Type | Location | Edit Command |
|------|----------|--------------|
| Terraform | `terraform/*/secrets.sops.yaml` | `sops <file>` |
| Ansible | `ansible/vars/*_secrets.yml` | `ansible-vault edit <file>` |

## Terraform Workflow

**Always: plan → review → apply → verify**

```bash
cd terraform/<module>
terraform fmt
terraform validate
terraform plan          # REQUIRED before apply
```

Present plan summary to user. Ask: "Does this look correct?"

After approval:
```bash
terraform apply
```

Verify resources exist, update `docs/reference/current-state.md` if needed.

## Ansible Workflow

**Always: lint → check → apply → verify**

```bash
cd ansible
ansible-lint --offline
ansible-playbook playbooks/<service>.yml --syntax-check
ansible-playbook playbooks/<service>.yml --check   # REQUIRED dry-run
```

Present changes to user. Ask: "Does this look correct?"

After approval:
```bash
ansible-playbook playbooks/<service>.yml
```

**Long-running playbooks** (jellyfin, transcoder, proxmox-host): Use 600000ms timeout.

Verify via SSH: `systemctl status <service>`, `journalctl -u <service>`.

## Nix DevShells

```bash
direnv allow              # Auto-load default shell
nix develop .#media-pipeline    # Go toolchain
nix develop .#session-manager   # Bash/shellcheck
```

Modify shells in `flake.nix`. Always test with `nix develop` before committing.

## Adding a New Container

**This is a multi-step workflow. See `add-container.md` for the complete checklist.**

Quick overview:
1. Create `terraform/proxmox-homelab/<name>.tf`
2. Run Terraform workflow (plan → apply)
3. Add to Ansible inventory
4. Create playbook and roles
5. Run Ansible workflow (check → apply)
6. Update documentation

## Common Operations

### Scale Container Resources

Edit CPU/memory in `terraform/proxmox-homelab/<name>.tf`, run Terraform workflow.

### Add Ansible Role to Existing Container

1. Create `ansible/roles/<name>/` with tasks/handlers/templates
2. Add role to playbook
3. Run Ansible workflow

### GPU Passthrough

Requires coordination:
- **Terraform:** Container privileged, features.nesting=true
- **Ansible:** GPU passthrough role delegates to Proxmox host

See jellyfin.tf and dual_gpu_passthrough role for patterns.

### Backup Operations

```bash
# On backup container
restic snapshots
restic restore <snapshot-id> --target /restore
```

## Safety Protocols

### Never Do

- Apply Terraform/Ansible without dry-run first
- Skip user approval for any changes
- Edit terraform.tfstate manually
- Commit .tfstate files or unencrypted secrets
- Run `apt`, `systemctl`, or edit files via SSH (use IaC instead)
- Delete or modify infrastructure without understanding dependencies

### Always Do

- Read current-state.md before making changes
- Present plan/check output before applying
- Verify changes after applying (SSH, service status, logs)
- Commit changes including documentation updates
- Use SOPS/Vault for secrets, never plaintext

### Git Discipline

- Never skip pre-commit hooks
- Commit Terraform and Ansible changes separately
- Update current-state.md when infrastructure changes
