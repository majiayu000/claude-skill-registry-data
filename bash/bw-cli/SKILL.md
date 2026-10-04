---
name: bw-cli
description: Securely interact with Bitwarden password manager via the bw CLI. Covers authentication (login/unlock/logout), vault operations (list/get/create/edit/delete items, folders, attachments), password/passphrase generation, organization management, and secure session handling. Use for "bitwarden", "bw", "password safe", "vaultwarden", "vault", "password manager", "generate password", "get password", "unlock vault". Requires bw CLI installed and internet access.
---

# Bitwarden CLI Skill

Secure vault operations using the Bitwarden command-line interface.

## When to use

**Activate this skill when the user wants to:**
- Authenticate to Bitwarden (`login`, `unlock`, `logout`, `status`)
- Retrieve credentials (`get password`, `get username`, `get totp`, `get item`)
- Manage vault items (`list`, `create`, `edit`, `delete`, `restore`)
- Generate passwords/passphrases (`generate`)
- Handle attachments (`create attachment`, `get attachment`)
- Manage organizations (`list organizations`, `move`, `confirm`)
- Export/import vault data
- Work with Vaultwarden/self-hosted instances

**Do NOT use for:**
- Installing Bitwarden browser extensions or mobile apps
- Comparing password managers theoretically
- Self-hosting Bitwarden server setup (use server administration tools)
- General encryption questions unrelated to Bitwarden

## Prerequisites

- `bw` CLI installed (verify with `bw --version`)
- Internet access (or access to self-hosted server)
- For vault operations: valid `BW_SESSION` environment variable or interactive unlock

## Authentication & Session Management

Bitwarden CLI uses a two-step authentication model:
1. **Login** (`bw login`) - Authenticates identity, creates local vault copy
2. **Unlock** (`bw unlock`) - Decrypts vault, generates session key

### ⚠️ ALWAYS Sync Before Accessing Vault

**CRITICAL:** The Bitwarden CLI maintains a local copy of the vault that can become stale. **Always run `bw sync` before accessing vault data** to ensure you have the latest items:

```bash
# Sync vault before any retrieval operation
bw sync

# Then proceed with vault operations
bw get item "Coda API Token"
```

**Best practice pattern for all vault operations:**
1. Check status / unlock if needed
2. **Run `bw sync`** (always!)
3. Then list, get, create, edit items

This prevents working with outdated data, especially when:
- Items were added/updated via other devices or browser extensions
- Working with shared organization items
- Recent changes haven't propagated to the local vault copy

### Quick Start: Interactive Login

```bash
# Login (supports email/password, API key, or SSO)
bw login

# Unlock to get session key
bw unlock
# Copy the export command from output, then:
export BW_SESSION="..."
```

### Automated/Scripted Login

Use environment variables for automation:

```bash
# Method 1: API Key (recommended for automation)
export BW_CLIENTID="user.xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export BW_CLIENTSECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
bw login --apikey
bw unlock --passwordenv BW_PASSWORD # if BW_PASSWORD set

# Method 2: Password file
bw unlock --passwordfile ~/.secrets/bw-master-password.txt
```

### Secure Password Storage (User-Requested)

If the user explicitly requests saving the master password to disk for convenience:

```bash
# 1. Create secrets directory in workspace
mkdir -p ~/.openclaw/workspace/.secrets
chmod 700 ~/.openclaw/workspace/.secrets

# 2. Store password (user enters interactively)
read -s BW_MASTER_PASS
echo "$BW_MASTER_PASS" > ~/.openclaw/workspace/.secrets/bw-password.txt
chmod 600 ~/.openclaw/workspace/.secrets/bw-password.txt

# 3. Ensure git ignores it
echo ".secrets/" >> ~/.openclaw/workspace/.gitignore
```

**Security requirements:**
- File must be created with mode `600` (user read/write only)
- Directory must be mode `700`
- Must add `.secrets/` to `.gitignore` immediately
- Must inform user of risks

### Check Status

```bash
bw status
```

Returns JSON with `status`: `unauthenticated`, `locked`, or `unlocked`.

### End Session

```bash
# Lock (keep login, destroy session key)
bw lock

# Logout (complete logout, requires re-authentication)
bw logout
# REQUIRES CONFIRMATION
```

## Core Vault Operations

### List Items

```bash
# All items
bw list items

# Search with filters
bw list items --search github
bw list items --folderid null --search "api key"
bw list items --collectionid xxx --organizationid xxx

# Other objects
bw list folders
bw list organizations
bw list collections
```

### Retrieve Items

```bash
# Get specific fields (searches by name if not UUID)
bw get password "GitHub"
bw get username "GitHub"
bw get totp "GitHub"  # 2FA code
bw get notes "GitHub"
bw get uri "GitHub"

# Get full item JSON (useful for scripts)
bw get item "GitHub" --pretty

# By exact ID
bw get item 7ac9cae8-5067-4faf-b6ab-acfd00e2c328
```

**Note:** `get` returns only one result. Use specific search terms.

### Create Items

Workflow: template → modify → encode → create

```bash
# Create folder
bw get template folder | jq '.name="Work Accounts"' | bw encode | bw create folder

# Create login item
bw get template item | jq \
  '.name="New Service" | .login=$(bw get template item.login | jq '.username="user@example.com" | .password="secret123"')' \
  | bw encode | bw create item
```

**Item types:** Login (1), Secure Note (2), Card (3), Identity (4). See [references/commands.md](./references/commands.md) for details.

### Edit Items

```bash
# Get item, modify password, save back
bw get item <id> | jq '.login.password="newpass"' | bw encode | bw edit item <id>

# Move to collection
echo '["collection-uuid"]' | bw encode | bw edit item-collections <item-id> --organizationid <org-id>
```

### Delete and Restore

```bash
# Send to trash (recoverable for 30 days)
bw delete item <id>

# PERMANENT DELETE - REQUIRES EXPLICIT CONFIRMATION
bw delete item <id> --permanent

# Restore from trash
bw restore item <id>
```

### Attachments

```bash
# Attach file to existing item
bw create attachment --file ./document.pdf --itemid <item-id>

# Download attachment
bw get attachment document.pdf --itemid <item-id> --output ./downloads/
```

## Password/Passphrase Generation

```bash
# Default: 14 chars, upper+lower+numbers
bw generate

# Custom: 20 chars with special characters
bw generate --uppercase --lowercase --number --special --length 20

# Passphrase: 4 words, dash-separated, capitalized
bw generate --passphrase --words 4 --separator "-" --capitalize --includeNumber
```

## Organization Management

```bash
# List organizations
bw list organizations

# List org collections
bw list org-collections --organizationid <org-id>

# Move personal item to organization
echo '["collection-uuid"]' | bw encode | bw move <item-id> <org-id>

# Confirm member (verify fingerprint first!)
bw get fingerprint <user-id>
bw confirm org-member <user-id> --organizationid <org-id>

# Device approvals (admin only)
bw device-approval list --organizationid <org-id>
bw device-approval approve <request-id> --organizationid <org-id>
```

## Import/Export

```bash
# Import from other password managers
bw import --formats  # list supported formats
bw import lastpasscsv ./export.csv

# Export vault - REQUIRES CONFIRMATION for destination outside workspace
bw export --output ~/.openclaw/workspace/ --format encrypted_json
bw export --output ~/.openclaw/workspace/ --format zip  # includes attachments
```

## Self-Hosted / Vaultwarden

```bash
# Configure for self-hosted instance
bw config server https://vaultwarden.example.com

# EU cloud
bw config server https://vault.bitwarden.eu

# Check current server
bw config server
```

## Safety & Security Guardrails

### Automatic Confirmations Required

| Action | Confirmation Required | Reason |
|--------|----------------------|--------|
| `bw delete --permanent` | Yes | Irreversible data loss |
| `bw logout` | Yes | Destroys session, requires re-auth |
| `bw export` outside workspace | Yes | Potential data exfiltration |
| `bw serve` | Yes | Opens network service |
| Saving master password to disk | Yes (with security instructions) | Credential exposure risk |
| `sudo` (for installing bw) | Yes | System privilege escalation |

### Secret Handling

- **Never log `BW_SESSION`** - redact from all output
- **Never log master passwords** - use `--quiet` when piping passwords
- **Session keys** - valid until `bw lock` or `bw logout`, or new terminal
- **Environment variables** - `BW_PASSWORD`, `BW_CLIENTID`, `BW_CLIENTSECRET` should be unset after use in scripts

### Workspace Boundaries

- Default all exports to `~/.openclaw/workspace/`
- Create `.secrets/` subdirectory for sensitive files (mode 700)
- Auto-add `.secrets/` to `.gitignore`
- Confirm before writing outside workspace

## Troubleshooting

### "Your authentication request appears to be coming from a bot"

Use API key authentication instead of email/password, or provide `client_secret` when prompted.

### "Vault is locked"

Run `bw unlock` and set `BW_SESSION` environment variable.

### Self-signed certificates (self-hosted)

```bash
export NODE_EXTRA_CA_CERTS="/path/to/ca-cert.pem"
```

### Debug mode

```bash
export BITWARDENCLI_DEBUG=true
```

## References

- Full command reference: [references/commands.md](./references/commands.md)
- Helper scripts:
  - [scripts/unlock-session.sh](./scripts/unlock-session.sh) - Safe unlock with session export
  - [scripts/safe-get-field.sh](./scripts/safe-get-field.sh) - Retrieve specific fields safely
  - [scripts/create-login-item.sh](./scripts/create-login-item.sh) - Interactive login creation
