---
name: setup-flywheel
description: Configure Flywheel MCP server, validate connection, and onboard to your vault
auto_trigger: true
trigger_keywords:
  - "setup flywheel"
  - "configure flywheel"
  - "install flywheel"
  - "flywheel setup"
  - "flywheel not working"
  - "flywheel not connecting"
  - "mcp not working"
  - "fix flywheel connection"
allowed-tools: Read, Write, mcp__flywheel__health_check, mcp__flywheel__get_vault_stats, mcp__flywheel__get_folder_structure
---

# Setup Flywheel

## Purpose

Complete Flywheel setup in one command:
1. Configure MCP server for your platform
2. Validate the connection works
3. Show vault stats and structure
4. Suggest next steps

## Workflow

```
User: "setup flywheel"
        │
        ▼
┌─────────────────────────────────────┐
│ Phase 1: Platform Detection         │
│   Platform: win32 → cmd /c npx     │
│   Platform: linux → npx (incl WSL) │
│   Platform: darwin → npx           │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Phase 2: Generate .mcp.json         │
│   - Detect vault path               │
│   - Merge with existing servers     │
│   - User confirms before write      │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Phase 2.5: Generate .flywheel.json  │
│   - Create client config if missing │
│   - Default: exclude_task_tags: []  │
│   - Explain customization options   │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Phase 3: Validate Connection        │
│   mcp__flywheel__health_check()    │
│   - If fail → restart instructions │
│   - If pass → continue to Phase 4  │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│ Phase 4: Vault Onboarding           │
│   mcp__flywheel__get_vault_stats() │
│   - Note count, link density       │
│   - Folder structure                │
│   - Suggested next steps            │
└─────────────────────────────────────┘
```

## Six Gates Compliance

| Gate | Status | Notes |
|------|--------|-------|
| 1. Read Before Write | ✅ | Reads existing .mcp.json before writing |
| 2. File Exists Check | ✅ | Creates new file if none exists |
| 3. Chain Validation | ✅ | Phases executed sequentially |
| 4. Mutation Confirm | ✅ | User confirms before writing .mcp.json |
| 5. MCP Health | ✅ | Validates MCP after setup |
| 6. Post Validation | ✅ | Shows vault stats to confirm working |

## Configuration Layers (IMPORTANT)

Claude Code uses **layered configuration** with precedence:

| Layer | File | Scope | Precedence |
|-------|------|-------|------------|
| **User** | `~/.claude/settings.json` | All projects globally | **Highest** |
| **Project** | `.mcp.json` | This project only | Lowest |

**Key insight**: User settings OVERRIDE project settings.

### Before Generating Config

**Check if user already has Flywheel in `~/.claude/settings.json`:**

1. Read `~/.claude/settings.json` (if exists)
2. Check for `mcpServers.flywheel`
3. If found → **Report existing config and skip Phase 2**

```
## Flywheel Already Configured (User Level)

Found existing Flywheel config in ~/.claude/settings.json

This config applies to ALL your projects automatically.
No action needed - proceeding to validation...
```

### Windows Users

For Windows (`Platform: win32`), **user-level config is recommended** because:
- The `cmd /c npx` wrapper applies to all Flywheel projects
- No need to add Windows wrapper to every project's `.mcp.json`
- Projects can stay platform-agnostic (committed to git)

**If suggesting user-level changes, ALWAYS warn about global scope:**

```
⚠️  This will modify ~/.claude/settings.json
    Changes apply to ALL projects, not just this one.
    Confirm? (y/n)
```

## Phase 1: Platform Detection (CRITICAL)

**Check the `Platform:` field in the environment info at the start of the session.**

| `Platform:` value | Runtime | Command | Path style |
|-------------------|---------|---------|------------|
| `linux` | Linux or WSL | `npx` | `/mnt/c/...` (WSL) or `/home/...` |
| `win32` | Native Windows | `cmd /c npx` | `C:/...` |
| `darwin` | macOS | `npx` | `/Users/...` |

**CRITICAL: NEVER infer platform from filesystem path.**
- `/mnt/c/Users/...` means WSL accessing Windows files → use `npx` (NOT `cmd /c`)
- The `Platform:` field is AUTHORITATIVE

## Phase 2: Generate .mcp.json

### Vault Path Detection

**Zero-config approach**: If `.mcp.json` is placed in the vault root (the working directory), no `PROJECT_PATH` is needed—the server defaults to `cwd()`.

**Only ask for vault path if**:
- The working directory is clearly NOT the vault (e.g., a parent folder)
- User explicitly wants to point to a different location

For WSL users with vaults on Windows filesystem:
- Convert `C:\Users\name\vault` → `/mnt/c/Users/name/vault`

### Generate Configuration

**Zero-config (`.mcp.json` in vault root) - PREFERRED:**

For Linux / macOS / WSL (`Platform: linux` or `Platform: darwin`):
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

For Windows (`Platform: win32`):
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
    }
  }
}
```

**With explicit vault path (only if vault ≠ working directory):**

For Linux / macOS / WSL:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/vault"
      }
    }
  }
}
```

For Windows:
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/path/to/vault"
      }
    }
  }
}
```

### Write Configuration

1. Check if `.mcp.json` exists in the project root
2. If exists, read it first (Gate 1)
3. Merge flywheel config with existing servers (don't overwrite other MCPs)
4. Show user the proposed config
5. Ask for confirmation (Gate 4)
6. Write the file

## Phase 2.5: Generate .flywheel.json (Client Config)

After writing `.mcp.json`, create the client-side config file if it doesn't exist:

**Check if `.flywheel.json` exists in the vault root:**
- If exists → Skip (preserve user customizations)
- If missing → Create with defaults

**Default `.flywheel.json`:**
```json
{
  "exclude_task_tags": []
}
```

**Show user the file and explain customization:**
```
## Client Configuration

Created `.flywheel.json` in your vault root.

This file lets you customize Flywheel behavior:
- `exclude_task_tags`: Tags to exclude from task queries (e.g., `["habit", "recurring"]`)

Example: To hide habit tasks from task queries, edit `.flywheel.json`:
{
  "exclude_task_tags": ["habit"]
}
```

## Phase 3: Validate Connection

After writing, check if MCP is available:

**If MCP not loaded yet:**

```
## Restart Required

Configuration written to .mcp.json

**Next Steps:**
1. Restart Claude Code to load the new MCP configuration
2. Say "setup flywheel" again to validate and see your vault stats

(Claude Code needs to restart to load new MCP servers)
```

**If MCP is available**, call `mcp__flywheel__health_check()`:

**On success → continue to Phase 4**

**On failure:**

```
## Connection Failed

✗ MCP server not responding

Troubleshooting:
1. Check the vault path exists
2. Ensure npx is available in PATH
3. Restart Claude Code and try again

Common issues:
- WSL users: Path should be /mnt/c/... not C:\...
- Windows users: Config uses "cmd /c npx" wrapper
```

## Phase 4: Vault Onboarding

Call `mcp__flywheel__get_vault_stats()` and `mcp__flywheel__get_folder_structure()`:

```
## Flywheel Connected!

### Your Vault
- **Notes**: 147 markdown files
- **Wikilinks**: 523 connections
- **Orphans**: 12 unlinked notes
- **Hub notes**: 5 highly connected

### Folder Structure
├── daily-notes/ (89 notes)
├── projects/ (32 notes)
├── people/ (15 notes)
└── reference/ (11 notes)

### Try These Next
- "check vault health" → Deep analysis with recommendations
- "find orphan notes" → Disconnected notes needing links
- "show hub notes" → Your most connected knowledge
- "do a rollup" → Aggregate daily notes into summaries

### Available Skills
Just describe what you want - Flywheel matches your intent:
- "add log entry: fixed the bug" → Appends to daily note
- "find broken links" → Repairs dead wikilinks
- "what links to Project X" → Graph navigation
```

## Error Handling

| Issue | Response |
|-------|----------|
| Can't determine platform | Ask: "Are you on Windows, macOS, or Linux/WSL?" |
| Vault path doesn't exist | Warn user, suggest checking path |
| Existing .mcp.json has syntax errors | Show error, offer to create fresh config |
| MCP health check fails | Suggest restart, provide troubleshooting steps |
| Vault empty | Explain Flywheel works best with existing notes |

## Complete Example Output

```
# Flywheel Setup

## Phase 1: Platform Detected
- Runtime: `win32` (Native Windows)
- Command: `cmd /c npx`

## Phase 2: Configuration
Working directory is your vault - using zero-config!

I'll add this to your `.mcp.json`:

{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"]
    }
  }
}

**Confirm?** (This will be merged with any existing MCP servers)

[User confirms]

## Phase 2.5: Client Config
Created `.flywheel.json` with defaults.
Edit this file to customize task filtering (e.g., exclude #habit tasks).

## Phase 3: Validating...
✓ MCP server connected
✓ Vault accessible (using working directory)

## Phase 4: Your Vault

Notes: 147 | Links: 523 | Orphans: 12

Folder structure:
├── daily-notes/ (89)
├── projects/ (32)
└── ...

### Next Steps
- "check vault health" - Full analysis
- "find orphan notes" - Unlinked content
- "do a rollup" - Aggregate your notes
```

## Related Skills
- `check-health` - Deep vault health analysis
- `find-orphans` - Unlinked notes
- `run-rollup` - Note aggregation workflow
