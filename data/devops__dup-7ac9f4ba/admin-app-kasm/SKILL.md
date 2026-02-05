---
name: admin-app-kasm
description: |
  Installs and manages KASM Workspaces, a container-based VDI platform for streaming desktops to browsers.
  Supports Ubuntu ARM64, desktop streaming, isolated browser sessions, and remote workspace access.

  Use when: installing KASM on Ubuntu ARM64, setting up VDI, configuring browser-based desktops, deploying on OCI instances.

  Keywords: kasm workspaces, VDI, virtual desktop, browser streaming, ARM64, kasm port 8443, container desktop
license: MIT
---

# KASM Workspaces - Container VDI

**Purpose**: Install KASM Workspaces on a single Ubuntu server and configure secure browser-based desktops.

## Step 0: Gather Required Information (MANDATORY)

**STOP. Before ANY installation commands, collect ALL parameters from the user.**

Copy this checklist and confirm each item:

```
Required Parameters:
- [ ] KASM_SERVER_IP       - Target server IP address
- [ ] SSH_USER             - SSH username (default: ubuntu)
- [ ] SSH_KEY_PATH         - Path to SSH private key (default: ~/.ssh/id_rsa)
- [ ] KASM_ADMIN_PASSWORD  - Admin password (minimum 12 characters)
- [ ] KASM_ADMIN_EMAIL     - Admin email (default: admin@kasm.local)

Resource Parameters:
- [ ] Server RAM           - Minimum 8GB (4GB KASM + 4GB per concurrent session)
- [ ] SWAP_SIZE_GB         - Swap file size (default: 8GB, recommended for ARM64)

Conditional Parameters (ask user):
- [ ] Using Cloudflare Tunnel for HTTPS? (Y/N)
      If Y: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, TUNNEL_HOSTNAME
- [ ] Custom KASM port? (default: 443 after install, 8443 during install)
```

### Password Requirements (KASM enforced)

- Minimum 12 characters
- Recommended: use a password manager to generate

**DO NOT proceed to Step 1 until ALL required parameters are confirmed.**

---

## Step 1: Determine Installation Path

Based on user answers, follow the appropriate workflow:

### Path A: Fresh Installation
**Use when**: New server, no existing KASM installation.

1. Read `references/INSTALLATION.md`
2. Export all parameters collected in Step 0
3. Follow step-by-step installation

### Path B: Post-Installation Configuration
**Use when**: KASM already installed, need to configure modules.

1. Read `references/QUICKSTART.md`
2. Run post-installation wizard

---

## Step 2: Secure HTTPS Access

**Determine access method based on Step 0 answers:**

| Scenario | Action |
|----------|--------|
| Cloudflare Tunnel = Yes | Read `references/cloudflare-tunnel.md` (uses `noTLSVerify: true`) |
| Direct IP only (dev) | Access via `https://SERVER_IP` (accept self-signed cert) |

---

## Step 3: Verify Installation

Run this verification checklist:

```
Verification:
- [ ] KASM UI accessible at https://SERVER_IP (or tunnel hostname)
- [ ] Login with admin credentials works
- [ ] At least 8 KASM containers running (docker ps | grep kasm)
- [ ] If tunnel: HTTPS working at TUNNEL_HOSTNAME
```

**If login fails**: Extract credentials from `install_log.txt` - see `references/INSTALLATION.md` section "Get Admin Credentials".

---

## Navigation

Detailed references (one level deep):
- Manual installation: `references/INSTALLATION.md`
- Cloudflare Tunnel: `references/cloudflare-tunnel.md`
- Post-installation wizard: `references/QUICKSTART.md`
- Wizard user guide: `references/README-WIZARD.md`
- Wizard spec (draft): `references/post-installation-interview-spec.md`

## Critical Rules

- Ensure Docker CE + Compose plugin installed before KASM.
- Allocate sufficient RAM per concurrent session (2–4GB).
- Do not expose installer port 8443 publicly without HTTPS/tunnel.

## Logging Integration

```bash
log_admin "SUCCESS" "installation" "Installed KASM Workspaces" "version=1.x server=$SERVER_ID"
log_admin "SUCCESS" "operation" "Ran KASM post-install wizard" "modules=$MODULES"
```

## Related Skills

- `admin-devops` for inventory and provisioning.
- `admin-infra-*` for OCI/Hetzner/etc server setup.

## References

- KASM docs: https://kasmweb.com/docs/latest/
- KASM GitHub: https://github.com/kasmtech
