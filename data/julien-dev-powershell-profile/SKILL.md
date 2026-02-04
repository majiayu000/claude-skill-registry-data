---
name: julien-dev-powershell-profile
description: "Manage PowerShell profile, aliases, functions. Triggers: add alias, update profile, modify claude command, Microsoft.PowerShell_profile.ps1"
triggers:
  - powershell profile
  - add alias
  - update profile
  - modify claude command
  - powershell alias
  - ps1 profile
---

# PowerShell Profile Manager

**Profile**: `C:\Users\julien\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`

## Workflow

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-dev-powershell-profile" activated
```

1. Read profile to identify correct section (11 numbered sections)
2. Edit profile (or use Python if OneDrive sync fails)
3. User runs `rup` to reload

## Performance Optimizations

### Lazy Loading MCP Secrets

**Location**: profile:349-431 (`Load-MCPSecrets` function)

**Impact**: Saves ~700ms on EVERY PowerShell startup (-64% faster)

**How it works**:
- CredentialManager Add-Type compilation deferred until needed
- Only loaded when launching `claude` or `happy` commands
- Check `$env:MCP_SECRETS_LOADED` to avoid reloading

**Critical**: When modifying secret loading, ensure it stays lazy!

### Get-ClaudeArgs - DRY Common Logic

**Location**: profile:427-457

**Purpose**: Shared argument generation for `claude`, `happy`, `claude-official`

**Features**:
- Auto-detects `.mcp.json` in current directory
- Auto-resume (unless `--new`, `-n`, `new`, `.` passed)
- Sets `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` (prevents title override)

**When modifying**: Update Get-ClaudeArgs, not individual functions

## Claude/Happy Architecture

### Three Functions, One Goal

| Function | Command | Purpose |
|----------|---------|---------|
| `claude` | happy.cmd | Default - uses Happy wrapper (mobile control) |
| `happy` | happy.cmd | Alias for claude |
| `claude-official` | claude.cmd | Bypass Happy wrapper if needed |

### Why Happy?

Happy (npm: happy-coder) provides enhanced mobile control over Claude Code.

**CRITICAL ISSUE**: Both `happy.cmd` and `claude.cmd` contain:
```cmd
title %COMSPEC%
```
This overwrites terminal title to "C:\WINDOWS\system32\cmd.exe"

**Solution**: Multi-layered hook system (SessionStart + PostToolUse)

See CLAUDE.md section "Solution Complète pour les Titres d'Onglets Dynamiques"

Requires 4 components:
1. Prompt wrapper AFTER Zoxide (profile:86-104) ✅
2. Windows Terminal suppressApplicationTitle: false ✅
3. SessionStart hook restore-terminal-title-on-start.ps1 ✅
4. PostToolUse hook update-terminal-title.js (after every Bash command) ✅

## Reference Files

| Need | File |
|------|------|
| Section details | [references/profile-structure.md](references/profile-structure.md) |
| Code patterns | [references/code-patterns.md](references/code-patterns.md) |
| OneDrive issues | [references/troubleshooting.md](references/troubleshooting.md) |
| Terminal title fix | CLAUDE.md "Solution Complète pour les Titres d'Onglets" |

## Skill Chaining

### Skills Required Before
- None (entry point skill)

### Input Expected
- User request to modify profile/alias/function
- Clear description of desired behavior

### Output Produced
- **Format**: Modified `Microsoft.PowerShell_profile.ps1`
- **Side effects**: Changes apply after `rup` or new terminal

### Compatible Skills After
- None typically (standalone modifications)

### Tools Used
- `Read` (read current profile state)
- `Edit` (modify profile sections)
- `Bash` with Python (workaround for OneDrive sync)

### Visual Workflow

```
User: "Add/modify PowerShell alias"
    ↓
[THIS SKILL]
    ├─► Read profile + refs as needed
    ├─► Identify correct section
    ├─► Edit (or Python workaround)
    └─► Verify modification
    ↓
User runs `rup` or opens new terminal
```
