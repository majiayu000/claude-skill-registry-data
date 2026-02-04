---
name: admin-app-coolify
description: |
  Installs and manages Coolify, an open-source self-hosted PaaS for deploying applications with Docker.
  Provides a Heroku-like experience on your own infrastructure.

  Use when: installing Coolify, deploying Docker apps, setting up a self-hosted PaaS, or configuring the Traefik proxy.

  Keywords: coolify, self-hosted paas, docker deployment, traefik proxy, open source heroku
license: MIT
---

# Coolify - Self-Hosted PaaS

**Purpose**: Install and operate Coolify on a single server, then deploy apps via Nixpacks, Dockerfile, or Docker Compose.

## Step 0: Gather Required Information (MANDATORY)

**STOP. Before ANY installation commands, collect ALL parameters from the user.**

Copy this checklist and confirm each item:

```
Required Parameters:
- [ ] COOLIFY_SERVER_IP     - Target server IP address
- [ ] SSH_USER              - SSH username (default: ubuntu)
- [ ] SSH_KEY_PATH          - Path to SSH private key (default: ~/.ssh/id_rsa)
- [ ] COOLIFY_ROOT_USER_EMAIL    - Admin email address
- [ ] COOLIFY_ROOT_USER_PASSWORD - Admin password (see requirements below)
- [ ] COOLIFY_INSTANCE_DOMAIN    - Main Coolify URL (e.g., coolify.example.com)
- [ ] COOLIFY_WILDCARD_DOMAIN    - Base domain for apps (e.g., example.com)

Conditional Parameters (ask user):
- [ ] Using Cloudflare Tunnel for HTTPS? (Y/N)
      If Y: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID
- [ ] Need OAuth callbacks or webhooks? (Y/N)
      If Y: Will configure origin certificates
- [ ] Additional SSH public keys to authorize? (optional)
```

### Password Requirements (Coolify enforced)

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one symbol (!@#$%^&*)

**DO NOT proceed to Step 1 until ALL required parameters are confirmed.**

---

## Step 1: Determine Installation Path

Based on user answers, follow the appropriate workflow:

### Path A: Full Automation (Recommended)
**Use when**: New server, Cloudflare Tunnel for HTTPS, standard setup.

1. Read `references/ENHANCED_SETUP.md`
2. Export all parameters collected in Step 0
3. Run enhanced setup script

### Path B: Manual Installation
**Use when**: Existing server, custom requirements, or debugging.

1. Read `references/INSTALLATION.md`
2. Follow step-by-step SSH commands
3. Configure SSH keys for localhost management (critical step)

---

## Step 2: Secure HTTPS Access

**Determine access method based on Step 0 answers:**

| Scenario | Action |
|----------|--------|
| Cloudflare Tunnel = Yes | Read `references/cloudflare-tunnel.md` |
| OAuth/webhooks = Yes | Also read `references/cloudflare-origin-certificates.md` |
| Direct IP only (dev) | Skip tunnel, access via `http://SERVER_IP:8000` |

---

## Step 3: Verify Installation

Run this verification checklist:

```
Verification:
- [ ] Coolify UI accessible at configured domain or IP:8000
- [ ] Login with COOLIFY_ROOT_USER_EMAIL and password works
- [ ] Servers → localhost shows "Connected" (green)
- [ ] If tunnel: HTTPS working at COOLIFY_INSTANCE_DOMAIN
```

**If localhost not connected**: The SSH key configuration failed. See `references/INSTALLATION.md` section "Configure Coolify SSH Access".

---

## Navigation

Detailed references (one level deep):
- Manual SSH installation: `references/INSTALLATION.md`
- Fully automated setup: `references/ENHANCED_SETUP.md`
- Bundled scripts: `references/BUNDLED_SCRIPTS.md`
- Cloudflare Tunnel (wildcard): `references/cloudflare-tunnel.md`
- Origin certificates (OAuth/webhooks): `references/cloudflare-origin-certificates.md`
- Error 1033 troubleshooting: `references/TROUBLESHOOTING_CF1033.md`

## Critical Rules

- Always install Docker CE with Compose plugin before Coolify.
- Do not expose port 8000 publicly without HTTPS (tunnel or reverse proxy).
- Keep `/data/coolify` intact; treat it as state.
- Always configure Coolify's SSH key for localhost management.

## Logging Integration

Log major operations using centralized logging from `admin`:

```bash
log_admin "SUCCESS" "installation" "Installed Coolify" "version=4.x server=$SERVER_ID"
log_admin "SUCCESS" "system-change" "Configured Coolify" "domain=$DOMAIN"
log_admin "SUCCESS" "operation" "Deployed app via Coolify" "app=$APP_NAME"
```

## Related Skills

- `admin-devops` for inventory and provisioning.
- `admin-infra-*` for provider-specific VM setup.
- `admin-wsl` for local Docker/CLI support when coordinating from WSL.

## References

- Coolify docs: https://coolify.io/docs
- Coolify GitHub: https://github.com/coollabsio/coolify
