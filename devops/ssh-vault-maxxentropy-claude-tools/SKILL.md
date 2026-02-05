---
name: ssh-vault
description: |
  SSH key lifecycle management. Create, deploy, rotate, and revoke SSH keys with full tracking.
  Use when asked about: ssh keys, manage ssh, create ssh key, deploy key, ssh config, key rotation,
  ssh access, authorized_keys, ssh audit, which keys, ssh inventory.
---

# SSH Vault - SSH Key Lifecycle Management

Manage SSH keys as first-class objects with full lifecycle tracking: create, deploy, verify, rotate, and revoke.

## Quick Start

```bash
# Create a new key with metadata
sshv key create homelab-2024 --purpose "Home lab servers"

# Add a host
sshv host add pi-node-01 --hostname 192.168.1.101 --user pi

# Deploy key to host
sshv deploy homelab-2024 pi-node-01

# Verify all deployments
sshv verify

# Security audit
sshv audit
```

## Why SSH Vault?

Traditional SSH key management problems:
- Keys scattered in ~/.ssh with no organization
- No tracking of which key is deployed where
- No rotation reminders or workflow
- No easy way to revoke access
- ~/.ssh/config becomes unwieldy

SSH Vault solves these by treating keys as managed resources with full lifecycle tracking.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SSH KEY LIFECYCLE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   CREATE ──► DEPLOY ──► USE ──► ROTATE ──► REVOKE                           │
│      │          │        │         │          │                              │
│      ▼          ▼        ▼         ▼          ▼                              │
│   • ed25519   • Track   • Agent  • Remind   • Remove from                    │
│   • Metadata  • Verify  • Config • Workflow   authorized_keys                │
│   • Purpose   • Audit            • New key  • Audit trail                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## CLI Reference

### Key Management

```bash
# Create a new key
sshv key create <key-id> [options]
  --purpose "description"    # What this key is for
  --expires 2y               # Rotation reminder (default: 2 years)
  --algorithm ed25519        # Algorithm (default: ed25519)
  --for-service azure-devops # Auto-select algorithm for service
  --no-passphrase            # Skip passphrase prompt

# Create key for a specific service (auto-selects correct algorithm)
sshv key create ado-macstudio-2024 --for-service azure-devops  # Uses RSA
sshv key create github-2024 --for-service github               # Uses ed25519

# List all keys
sshv key list
  --format table|json        # Output format

# Show key details
sshv key show <key-id>

# Delete a key (must revoke from all hosts first)
sshv key delete <key-id>
  --force                    # Delete even if deployed

# Rotate a key
sshv key rotate <key-id>
  --new-id <new-key-id>      # ID for new key (default: <old>-rotated)
```

### Host Management

```bash
# Add a host
sshv host add <host-id> [options]
  --hostname <ip-or-dns>     # Required
  --user <username>          # SSH user (default: current user)
  --port 22                  # SSH port (default: 22)

# List all hosts
sshv host list

# Show host details
sshv host show <host-id>

# Remove a host
sshv host remove <host-id>
```

### Deployment Operations

```bash
# Deploy key to host
sshv deploy <key-id> <host-id>
  --verify                   # Verify after deploy

# Verify deployments
sshv verify [key-id] [host-id]
  --all                      # Verify all deployments

# Revoke key from host
sshv revoke <key-id> <host-id>

# Revoke key from all hosts
sshv revoke <key-id> --all
```

### Config Management

```bash
# Sync inventory to ~/.ssh/config
sshv config sync
  --dry-run                  # Show what would change

# Show managed config entries
sshv config show

# Remove managed entries from config
sshv config clean
```

### Security Audit

```bash
# Run security audit
sshv audit
  --fix                      # Offer to fix issues
  --json                     # JSON output

# Check specific key
sshv audit <key-id>
```

### Service Profiles

Different services have different SSH key requirements. Azure DevOps requires RSA keys, while GitHub/GitLab work with ed25519 (recommended).

```bash
# List available services and their requirements
sshv service list

# Show service details (algorithm, fingerprints, docs)
sshv service show azure-devops
sshv service show github

# Built-in services:
# - azure-devops: REQUIRES RSA (ed25519 not supported!)
# - github: Supports all, prefers ed25519
# - gitlab: Supports all, prefers ed25519
# - bitbucket: Supports RSA and ed25519
```

### Agent Management

```bash
# Add key to ssh-agent
sshv agent add <key-id>

# Add all keys matching purpose
sshv agent add --purpose "work"

# Remove key from agent
sshv agent remove <key-id>

# List keys in agent (with our metadata)
sshv agent list
```

### Backup

```bash
# Backup inventory (metadata only)
sshv backup create <output-file>

# Backup with private keys (encrypted)
sshv backup create <output-file> --include-private

# Restore from backup
sshv backup restore <backup-file>
```

## Inventory File

SSH Vault stores metadata in `~/.ssh-vault/inventory.yaml`:

```yaml
version: "1.0"
keys:
  homelab-2024:
    algorithm: ed25519
    created_at: "2024-01-15T10:30:00Z"
    expires_at: "2026-01-15T10:30:00Z"
    purpose: "Home lab servers"
    public_key_path: ~/.ssh/homelab-2024.pub
    private_key_path: ~/.ssh/homelab-2024
    fingerprint: "SHA256:abc123..."
    has_passphrase: true
    deployments:
      - host_id: pi-node-01
        deployed_at: "2024-01-15T11:00:00Z"
        verified_at: "2024-12-15T09:00:00Z"

hosts:
  pi-node-01:
    hostname: 192.168.1.101
    user: pi
    port: 22
    keys: [homelab-2024]
```

## Best Practices

### Key Naming Convention

Include the year for easy rotation tracking:
```
personal-2024
work-github-2024
homelab-2024
```

### One Key Per Purpose

Don't share keys across different trust boundaries:
```
work-servers-2024      # Work infrastructure
personal-servers-2024  # Personal servers
github-2024            # GitHub specifically
```

### Regular Rotation

SSH Vault reminds you when keys are due for rotation:
```bash
sshv audit
# ⚠️  homelab-2022: Expired 2024-01-15 (rotate with: sshv key rotate homelab-2022)
```

### Verify Periodically

Ensure your deployments haven't been modified:
```bash
sshv verify --all
```

## Security Notes

1. **Private keys stay in ~/.ssh/** - We only track metadata
2. **No passphrases stored** - We note if a key has one, but never store it
3. **Inventory is plaintext** - Contains paths and fingerprints, not secrets
4. **Backup encryption** - Use GPG when backing up with private keys

## Integration with ssh-agent

SSH Vault integrates with your existing ssh-agent:

```bash
# Start of work session - load work keys
sshv agent add --purpose "work"

# End of session - clear agent
ssh-add -D
```

## Integration with ~/.ssh/config

SSH Vault can manage a section of your config:

```
# ~/.ssh/config

# Your manual entries here...

# === SSH-VAULT MANAGED - DO NOT EDIT BELOW ===
Host pi-node-01
    HostName 192.168.1.101
    User pi
    IdentityFile ~/.ssh/homelab-2024
    IdentitiesOnly yes

Host dev-server
    HostName dev.example.com
    User admin
    IdentityFile ~/.ssh/work-2024
    IdentitiesOnly yes
# === SSH-VAULT MANAGED - DO NOT EDIT ABOVE ===
```

## Troubleshooting

### "Key not found in authorized_keys"

The key may have been removed externally:
```bash
sshv deploy <key-id> <host-id>  # Re-deploy
```

### "Cannot connect to host"

SSH Vault needs SSH access to verify/revoke:
```bash
ssh user@host  # Test manually first
```

### "Permission denied"

Check key permissions:
```bash
sshv audit  # Will flag permission issues
chmod 600 ~/.ssh/<key>
chmod 644 ~/.ssh/<key>.pub
```

## Files

| Path | Purpose |
|------|---------|
| `~/.ssh-vault/` | SSH Vault data directory |
| `~/.ssh-vault/inventory.yaml` | Key and host inventory |
| `~/.ssh/` | Actual SSH keys (standard location) |
| `~/.ssh/config` | SSH config (partially managed) |
