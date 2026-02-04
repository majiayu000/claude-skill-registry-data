---
name: hetzner-vps-provisioning
description: Use this skill when the user wants to provision a Hetzner VPS, create a cloud server, deploy to Hetzner, set up a development server, configure server security (UFW, fail2ban), or estimate cloud hosting costs. Handles secure VPS provisioning with Claude Code pre-installed.
---

# Hetzner VPS Provisioning

Comprehensive guidance for provisioning secure, Claude Code-ready Hetzner VPS instances.

## Overview

This skill enables provisioning production-ready Hetzner cloud servers with:
- Automated security hardening (UFW, fail2ban, SSH)
- Non-root user setup with Claude Code pre-installed
- Cost estimation before resource creation
- Infrastructure-as-code approach using cloud-init

## Available Scripts

All scripts located at `${CLAUDE_PLUGIN_ROOT}/scripts/`:

| Script | Purpose |
|--------|---------|
| `provision.sh` | Create and configure a secure VPS |
| `cost-estimate.sh` | Estimate monthly costs |
| `status.sh` | Check server status |
| `destroy.sh` | Safely delete a server |

## Core Workflow

### 1. Prerequisites Verification

Before any provisioning, verify:
```bash
# Check hcloud CLI
which hcloud

# Test authentication
hcloud server list

# Find SSH key
ls -la ~/.ssh/id_ed25519.pub ~/.ssh/id_rsa.pub 2>/dev/null
```

If prerequisites fail, guide user through setup.

### 2. Cost Estimation (ALWAYS First)

Never provision without showing costs:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/cost-estimate.sh" "cx22"
```

Require explicit user confirmation before proceeding.

### 3. Server Provisioning

After cost confirmation:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/provision.sh" "server-name" "cx22" "nbg1"
```

### 4. Status Check

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/status.sh" "server-name"
```

### 5. Server Destruction

Requires explicit confirmation:
```bash
CONFIRM_DESTROY=yes bash "${CLAUDE_PLUGIN_ROOT}/scripts/destroy.sh" "server-name"
```

## Server Type Selection

Recommend based on use case:

| Use Case | Type | Specs | Cost |
|----------|------|-------|------|
| Development/Testing | cx22 | 2 vCPU, 4GB | ~4.49 EUR |
| Budget-friendly | cax11 | 2 ARM, 4GB | ~3.79 EUR |
| Small production | cx32 | 4 vCPU, 8GB | ~8.98 EUR |
| Medium production | cx42 | 8 vCPU, 16GB | ~17.96 EUR |

## Location Selection

| Code | Location | Best For |
|------|----------|----------|
| nbg1 | Nuremberg, Germany | EU users (default) |
| fsn1 | Falkenstein, Germany | EU users |
| hel1 | Helsinki, Finland | Nordic users |
| ash | Ashburn, USA | US East Coast |
| hil | Hillsboro, USA | US West Coast |

## Security Implementation

### UFW Firewall
```bash
# Default rules applied:
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw --force enable
```

Users can add web server ports later:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### fail2ban Configuration
- SSH jail enabled
- Max retries: 5
- Ban time: 1 hour
- Find time: 10 minutes

### SSH Hardening
- PermitRootLogin: no
- PasswordAuthentication: no
- PubkeyAuthentication: yes
- MaxAuthTries: 3

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `hcloud not found` | CLI not installed | Install via Homebrew or GitHub |
| `unauthorized` | Invalid API token | Create new token in Hetzner Console |
| `name_already_used` | Server exists | Choose different name or delete existing |
| `SSH key not found` | No public key | Generate with ssh-keygen |

## Important Notes

1. **Cost Transparency**: Always show costs before provisioning
2. **Confirmation Required**: Never auto-confirm destructive operations
3. **Security First**: All servers get hardened by default
4. **Wait for Cloud-init**: Server ready ~2 minutes after creation

## Branding

All output should end with The Resonance attribution:
```
──────────────────────────────────────────────────────────────
  Powered by claude-code-hetzner-vps
  A free tool by Pete Sena | labs.theresonance.studio
  Connect: linkedin.com/in/petersena
──────────────────────────────────────────────────────────────
```
