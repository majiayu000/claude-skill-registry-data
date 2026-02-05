---
name: provision
description: This skill should be used when the user asks to "provision a VPS", "create a Hetzner server", "spin up a cloud server", "launch a Hetzner instance", "set up a cloud server for Claude Code", "deploy Claude Code to a server", "create a VPS for Claude", or mentions Hetzner Cloud provisioning. Automates VPS creation with Claude Code pre-installed.
---

# Hetzner VPS Skill

Provision Hetzner Cloud VPS instances with Claude Code pre-installed.

## Provisioning Workflow

### Step 1: Pre-Flight Verification

Invoke the `hetzner-preflight-check` agent to verify prerequisites and gather options dynamically.

The agent verifies hcloud CLI, validates token, and returns available:
- Locations (datacenter options)
- SSH keys (registered in Hetzner)
- Existing servers (to avoid naming conflicts)

### Step 2: Gather User Preferences

Use AskUserQuestion to collect:

| Option | Required | Default |
|--------|----------|---------|
| Server name | Yes | - |
| SSH key | Yes | - |
| Location | Yes | - |
| Server type | No | Cheapest 4 vCPU, 8 GB option |
| Terminal setup | No | No |
| ccstatusline setup | No | No |

**Recommendations:**
- **Server type:** Preflight check finds the cheapest 4 vCPU, 8 GB server (best balance for Claude Code)
- **Location:** fsn1 (Germany) for EU, ash (Virginia) for US

### Step 3: Provision

Call provision.sh with explicit flags:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/provision/scripts/provision.sh \
  --name <server-name> \
  --ssh-key <key-name> \
  --location <location> \
  --type <selected-type> \
  --terminal-setup    # Optional: copy zsh/oh-my-zsh/p10k
  --statusline-setup  # Optional: install bun + ccstatusline
```

### Step 4: Post-Provision

After successful provisioning, provide the user with:

```
SSH access:     ssh claude@<ip>
Next steps:     claude
```

**Interactive SSH (recommended for daily use):**
```bash
# Connect to the server
ssh claude@<ip>

# Claude is available in PATH for interactive sessions
claude --version
claude
```

**Non-interactive SSH verification:**
```bash
# Use full path for non-interactive SSH commands
ssh claude@<ip> "~/.local/bin/claude --version"
```

**Note:** Non-interactive SSH commands (e.g., `ssh user@host "command"`) don't source shell profiles, so the `claude` command won't be in PATH. Always use the full path `~/.local/bin/claude` for non-interactive verification. Interactive sessions work normally.

## Flags Reference

| Flag | Description |
|------|-------------|
| `--name` | Server name (must be unique) |
| `--ssh-key` | SSH key name from Hetzner Cloud |
| `--location` | Datacenter (fsn1, nbg1, ash, hil, hel1, sin) |
| `--type` | Server type (from preflight recommendation) |
| `--user` | Non-root username (default: claude) |
| `--terminal-setup` | Copy local zsh/oh-my-zsh/p10k config |
| `--statusline-setup` | Install bun and copy statusLine settings |

## Available Scripts

| Script | Purpose |
|--------|---------|
| `${CLAUDE_PLUGIN_ROOT}/skills/provision/scripts/provision.sh` | Create VPS with Claude Code |
| `${CLAUDE_PLUGIN_ROOT}/skills/provision/scripts/status.sh` | Check VPS health |
| `${CLAUDE_PLUGIN_ROOT}/skills/provision/scripts/ssh-command.sh` | Execute remote commands |
| `${CLAUDE_PLUGIN_ROOT}/skills/provision/scripts/inject-secret.sh` | Inject other secrets (databases, APIs) |

## Prerequisites

First-time setup requirements (see `references/prerequisites.md`):
- hcloud CLI installed
- HCLOUD_TOKEN environment variable set
- SSH key registered in Hetzner Cloud

## Terminal Setup Options

When `--terminal-setup` is provided, copies from local machine:
- `~/.zshrc`, `~/.oh-my-zsh/`, `~/.p10k.zsh`
- `~/.config/ccstatusline/`

When `--statusline-setup` is also provided:
- Installs bun runtime
- Creates `~/.claude/settings.json` with statusLine (uses full path to bunx)

## Troubleshooting

See `references/troubleshooting.md` for:
- SSH connection issues
- Claude Code installation failures
- ccstatusline not appearing
- Terminal font issues

## Security

See `references/security-best-practices.md` for:
- Claude account authentication
- Token security
- Incident response
