---
name: admin
description: |
  Context-aware development companion that knows your machine and adapts instructions accordingly.
  Central orchestrator for system administration - reads device profile, routes to specialists.

  Use when: installing tools, managing servers, setting up dev environments, coordinating any admin task.
  The skill adapts to YOUR preferences (uv over pip, scoop over winget, etc.)
license: MIT
---

# Admin - Context-Aware DevOps Companion

**Purpose**: Read your device profile, adapt instructions to your setup, route to specialist skills.

## Core Value

When a GitHub repo says `pip install package`, this skill knows you prefer `uv` and suggests `uv pip install package` instead.

---

## ⚠️ STEP 0: Detect Environment (MANDATORY FIRST)

**Before ANY operation, run this detection to find the profile:**

```bash
# Detect environment and set ADMIN_ROOT
if grep -qi microsoft /proc/version 2>/dev/null; then
    # WSL - profile is on Windows side
    WIN_USER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')
    ADMIN_ROOT="/mnt/c/Users/$WIN_USER/.admin"
    ENV_TYPE="wsl"
elif [[ "$OS" == "Windows_NT" || -n "$MSYSTEM" ]]; then
    # Git Bash on Windows
    ADMIN_ROOT="$HOME/.admin"
    ENV_TYPE="windows-gitbash"
elif [[ "$(uname -s)" == "Darwin" ]]; then
    # macOS
    ADMIN_ROOT="$HOME/.admin"
    ENV_TYPE="macos"
else
    # Native Linux
    ADMIN_ROOT="$HOME/.admin"
    ENV_TYPE="linux"
fi

HOSTNAME=$(hostname)
PROFILE_PATH="$ADMIN_ROOT/profiles/$HOSTNAME.json"

echo "Environment: $ENV_TYPE"
echo "Admin Root:  $ADMIN_ROOT"
echo "Profile:     $PROFILE_PATH"
echo "Exists:      $(test -f "$PROFILE_PATH" && echo 'YES' || echo 'NO')"
```

### Critical Path Rules

| Running From | Profile Location | Why |
|--------------|------------------|-----|
| **WSL** | `/mnt/c/Users/{WIN_USER}/.admin/profiles/` | Profile lives on Windows, WSL accesses via /mnt/c |
| **Windows Git Bash** | `$HOME/.admin/profiles/` | Same as Windows native |
| **Windows PowerShell** | `$HOME\.admin\profiles\` | Windows native |
| **Native Linux** | `~/.admin/profiles/` | Linux home |
| **macOS** | `~/.admin/profiles/` | macOS home |

### Common Mistake

❌ **WRONG**: Assume `~/.admin` always works
```bash
# This FAILS in WSL because ~ is /home/wsladmin, not Windows
ls ~/.admin/profiles/  # Empty or doesn't exist
```

✅ **RIGHT**: Detect environment first, then find profile
```bash
# In WSL, profile is on Windows side
ls /mnt/c/Users/Owner/.admin/profiles/  # Found!
```

---

## Quick Start: After Detection

### Bash (WSL/Linux/macOS)
```bash
# After running detection above
source /path/to/admin/scripts/load-profile.sh
load_admin_profile "$PROFILE_PATH"
show_admin_summary
```

### PowerShell (Windows)
```powershell
. scripts/Load-Profile.ps1
Load-AdminProfile -Export
Show-AdminSummary
```

---

## The Key Innovation: Preferences

```json
"preferences": {
  "python": { "manager": "uv", "reason": "Fast, modern, replaces pip+venv" },
  "node": { "manager": "npm", "reason": "Default, bun for speed" },
  "packages": { "manager": "scoop", "reason": "Portable installs" }
}
```

**Always check preferences before suggesting commands.**

---

## Adaptation Examples

| User Wants | README Says | Profile Shows | You Suggest |
|------------|-------------|---------------|-------------|
| Install Python pkg | `pip install x` | `preferences.python.manager: "uv"` | `uv pip install x` |
| Install Node pkg | `npm install` | `preferences.node.manager: "pnpm"` | `pnpm install` |
| Install CLI tool | `brew install x` | `preferences.packages.manager: "scoop"` | `scoop install x` |

---

## Profile Sections Quick Reference

| Section | What It Contains | When To Use |
|---------|------------------|-------------|
| `device` | OS, hostname, hardware | Platform detection |
| `paths` | Critical locations | Finding configs, skills, keys |
| `tools` | Installed tools + paths | Check before install |
| `preferences` | User choices | **Adapt commands** |
| `servers` | Managed servers | SSH, deployments |
| `deployments` | .env.local references | Load provider configs |
| `capabilities` | Quick flags | Route decisions |
| `issues` | Known problems | Avoid repeating fixes |
| `mcp` | MCP server configs | MCP troubleshooting |
| `wsl` | WSL config (Windows) | Cross-platform |

---

## Routing Rules

| Task Type | Route To | Requires |
|-----------|----------|----------|
| Server provisioning | `admin-devops` | - |
| OCI infrastructure | `admin-infra-oci` | OCI CLI configured |
| Hetzner infrastructure | `admin-infra-hetzner` | Hetzner token |
| Other clouds | `admin-infra-{provider}` | Provider credentials |
| Coolify installation | `admin-app-coolify` | Server access |
| KASM installation | `admin-app-kasm` | Server access |
| Windows system admin | `admin-windows` | Windows platform |
| WSL administration | `admin-wsl` | WSL present |
| Linux/macOS admin | `admin-unix` | Non-Windows |
| MCP servers | `admin-mcp` | - |

---

## Tool Installation Workflow

1. **Detect environment** (Step 0 above)
2. **Load profile**: `load_admin_profile "$PROFILE_PATH"`
3. **Check if installed**: `jq '.tools.{name}.present' "$PROFILE_PATH"`
4. **If not installed**:
   - Check preferred manager: `jq '.preferences.packages.manager' "$PROFILE_PATH"`
   - Construct install command for that manager
5. **After install**: Update profile

---

## Server Operations Workflow

1. **List servers**: `jq '.servers[]' "$PROFILE_PATH"`
2. **Get SSH details**: 
   ```bash
   SERVER=$(jq '.servers[] | select(.id == "cool-two")' "$PROFILE_PATH")
   ```
3. **Handle path conversion** (WSL needs to convert Windows paths):
   ```bash
   KEY_PATH=$(echo "$SERVER" | jq -r '.keyPath')
   # Convert C:/Users/... to /mnt/c/Users/...
   if [[ "$KEY_PATH" == *":"* ]]; then
       DRIVE=$(echo "$KEY_PATH" | cut -c1 | tr '[:upper:]' '[:lower:]')
       REST=$(echo "$KEY_PATH" | cut -c3- | sed 's|\\|/|g')
       KEY_PATH="/mnt/$DRIVE$REST"
   fi
   ```

---

## First-Run Setup

If profile doesn't exist:

**Windows (PowerShell)**:
```powershell
.\scripts\Initialize-AdminProfile.ps1
```

**WSL/Linux** - Profile should be created from Windows side first, then accessed from WSL via `/mnt/c/...`

---

## Capability Checks

```bash
# Load profile first, then check
HAS_DOCKER=$(jq -r '.capabilities.hasDocker' "$PROFILE_PATH")
HAS_WSL=$(jq -r '.capabilities.hasWsl' "$PROFILE_PATH")

if [[ "$HAS_DOCKER" == "true" ]]; then
    docker info
fi
```

---

## References

- `references/device-profiles.md` - Profile management details
- `references/routing-guide.md` - Detailed routing logic
- `references/first-run-setup.md` - Initial setup flow
- `references/cross-platform.md` - Windows ↔ WSL coordination

## Scripts

| Script | Purpose |
|--------|---------|
| `Load-Profile.ps1` | PowerShell profile loader |
| `load-profile.sh` | Bash profile loader |
| `Initialize-AdminProfile.ps1` | Create new profile (Windows) |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `admin-devops` | Server inventory & provisioning |
| `admin-infra-*` | Cloud provider provisioning |
| `admin-app-*` | Application deployment |
| `admin-windows` | Windows administration |
| `admin-wsl` | WSL administration |
| `admin-unix` | Linux/macOS administration |
| `admin-mcp` | MCP server management |
