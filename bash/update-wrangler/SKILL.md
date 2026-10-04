---
name: updating-wrangler
description: Update the wrangler plugin to the latest version by clearing all caching layers. Use when user says "update yourself", "update wrangler", or after pushing changes to the wrangler repo.
---

# Update Wrangler Plugin

This skill updates the wrangler plugin to the latest version from GitHub by clearing all caching layers.

## When to Use

- User says "update yourself" or "update wrangler"
- After pushing changes to the wrangler GitHub repo
- When slash commands or skills aren't showing up after changes
- When plugin behavior doesn't match the latest code

## Background: The Caching Problem

Claude Code's plugin system has **three layers** that can get out of sync:

| Layer | Location | Purpose |
|-------|----------|---------|
| **GitHub** | Remote repository | Source of truth |
| **Marketplace clone** | `~/.claude/plugins/marketplaces/{marketplace}/` | Local git clone |
| **Installed cache** | `~/.claude/plugins/cache/{marketplace}/wrangler/` | Files Claude Code uses |

The `/plugin` command only reads from the marketplace clone, and only re-installs if version changes. Pushing to GitHub doesn't update the other layers.

## Instructions

### Step 1: Find the Marketplace Name

```bash
# Find which marketplace wrangler is installed from
grep -l wrangler ~/.claude/plugins/marketplaces/*/plugin.json 2>/dev/null | head -1 | xargs dirname | xargs basename
```

Or check `~/.claude/plugins/installed_plugins.json` for the key containing "wrangler" (e.g., `wrangler@samjhecht-plugins` means marketplace is `samjhecht-plugins`).

### Step 2: Update All Layers

Execute these commands (replace `{marketplace}` with actual name):

```bash
# 1. Update the marketplace clone
cd ~/.claude/plugins/marketplaces/{marketplace} && git fetch origin && git reset --hard origin/main && cd -

# 2. Clear the installed cache
rm -rf ~/.claude/plugins/cache/{marketplace}/wrangler/

# 3. Rebuild MCP bundle (CRITICAL - Claude Code doesn't run postinstall)
cd ~/.claude/plugins/marketplaces/{marketplace} && npm install && cd -

# 4. Reset installed_plugins.json entry (forces reinstall)
```

Step 3 rebuilds the MCP bundle. This is critical because Claude Code copies plugin files but doesn't run `npm install` or postinstall scripts. The MCP server requires `mcp/dist/bundle.cjs` which is built by the postinstall script.

For step 4, edit `~/.claude/plugins/installed_plugins.json` and set the wrangler entry to an empty array:

```json
"wrangler@{marketplace}": []
```

### Step 3: Inform User

Tell the user:
```
Wrangler plugin cache cleared. Please restart Claude Code to complete the update.

The plugin will reinstall from the latest code on next startup.
```

## Automated Script

Execute the script directly:

```bash
./scripts/update-wrangler.sh
```

Or offer to add it to the user's shell config for easy access:

```bash
# Add to ~/.zshrc or ~/.bashrc
source /path/to/wrangler/skills/updating-wrangler/scripts/update-wrangler.sh

# Then just run:
update-wrangler
```

The script ([scripts/update-wrangler.sh](scripts/update-wrangler.sh)) handles:
- Finding the marketplace name automatically
- Updating the marketplace clone from origin
- Clearing the plugin cache
- Resetting the installed_plugins.json entry

**Requires:** `jq` for JSON manipulation (falls back to manual instructions if not installed)

## Manual Alternative

If the user prefers not to use the script, provide these manual steps:

1. **Find your marketplace name** in `~/.claude/plugins/installed_plugins.json`
2. **Pull latest code**: `cd ~/.claude/plugins/marketplaces/{marketplace} && git pull`
3. **Delete cache**: `rm -rf ~/.claude/plugins/cache/{marketplace}/wrangler/`
4. **Rebuild MCP bundle**: `cd ~/.claude/plugins/marketplaces/{marketplace} && npm install`
5. **Edit** `~/.claude/plugins/installed_plugins.json` - set wrangler entry to `[]`
6. **Restart Claude Code**

## Verification

After restart, verify the update worked:

```bash
# Check the installed commit
cat ~/.claude/plugins/installed_plugins.json | grep -A5 wrangler

# Check commands exist
ls ~/.claude/plugins/cache/{marketplace}/wrangler/*/commands/
```

## Why This Is Necessary

- Version numbers alone don't trigger updates (same version = no reinstall)
- The marketplace clone is a local git repo that doesn't auto-fetch
- `installed_plugins.json` caches the commit SHA and won't reinstall unless cleared
- All three layers must be updated for changes to take effect
