---
name: setup-mcp
description: Configure scan-mcp MCP server in Claude Code's global configuration. Use when user wants to setup, configure, initialize, enable, or install the scan-mcp MCP server. Runs preflight checks for prerequisites (Node 22+, SANE tools, tiffcp), helps install missing dependencies, and adds server configuration with user-specified INBOX_DIR.
---

# scan-mcp MCP Server Setup

Configure the scan-mcp MCP server in Claude Code's global configuration to enable scanner control.

## Setup Workflow

### Step 1: Gather User Preferences

Ask user for:
1. **INBOX_DIR location** (default: `~/Documents/scanned_documents/inbox`)
2. **Installation method**: npx (recommended) or local

### Step 2: Run Preflight Checks

```bash
npx -y scan-mcp --preflight-only
```

**Expected on success**: All checks passed!

**If preflight fails**: Parse output to identify missing dependencies, then guide user through installation (see [PLATFORMS.md](PLATFORMS.md)).

Common missing items:
- SANE utilities (`scanimage`, `scanadf`)
- TIFF tools (`tiffcp` or ImageMagick `convert`)

### Step 3: Locate Claude Code MCP Configuration

Claude Code config location:
- `~/.config/claude/config.json` (Linux/macOS)
- Create if doesn't exist

### Step 4: Add or Update Configuration

**Configuration structure (npx - recommended)**:
```json
{
  "mcpServers": {
    "scan": {
      "command": "npx",
      "args": ["-y", "scan-mcp"],
      "env": {
        "INBOX_DIR": "~/Documents/scanned_documents/inbox"
      }
    }
  }
}
```

**Important**:
- If config.json doesn't exist: Create it with scan-mcp server entry
- If config.json exists but no mcpServers: Add mcpServers section
- If mcpServers exists: Add or update "scan" entry
- Preserve existing MCP server configurations

**For local installation** (advanced): See [ADVANCED.md](ADVANCED.md).

### Step 5: Verify Configuration

1. Inform user that Claude Code needs restart to pick up new configuration
2. Suggest testing: `claude mcp` or asking "scan this document"
3. If issues occur, suggest running `/doctor`

## Quick Example

**User**: "Setup scan-mcp"

**Actions**:
1. Ask: "Where would you like scanned documents stored? (Default: ~/Documents/scanned_documents/inbox)"
2. Run: `npx -y scan-mcp --preflight-only`
3. If preflight passes:
   - Locate/create `~/.config/claude/config.json`
   - Add scan-mcp server configuration
   - Confirm: "scan-mcp configured. Please restart Claude Code. Test with 'scan this document'."
4. If preflight fails:
   - Identify missing dependencies
   - Provide installation commands (see PLATFORMS.md)
   - Re-run preflight after user installs

## Reference Materials

- **[PLATFORMS.md](PLATFORMS.md)** — Platform-specific prerequisite installation
- **[SCANNERS.md](SCANNERS.md)** — Scanner permissions and device setup
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Common setup issues and solutions
- **[ADVANCED.md](ADVANCED.md)** — Local installation, multiple configs, advanced options
