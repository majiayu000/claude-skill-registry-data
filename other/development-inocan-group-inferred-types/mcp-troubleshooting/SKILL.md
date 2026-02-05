---
name: mcp-troubleshooting
description: "Systematic troubleshooting for MCP tools including installation issues, runtime errors, config problems, and debugging strategies. Use when MCP tools not working, debugging errors, or helping users..."
---

# MCP Troubleshooting Guide for @j0kz/mcp-agents

Systematic approach to diagnosing and resolving MCP tool issues.

## When to Use This Skill

- Tools not appearing in editor after installation
- "Module not found" or import errors
- MCP servers not responding
- Commands not recognized by AI
- Config file issues
- Installation failures
- Cache-related problems

## Evidence Base

**Current State:**
- README.md troubleshooting section with common issues
- Clear cache workflow (`npm cache clean --force`)
- Platform-specific config paths (Claude Code, Cursor, Windsurf, Qoder, VS Code, Roo)
- Installation validation steps
- 632+ tests for validation

---

## Quick Fix (90% Success Rate)

```bash
# The 3-minute solution that fixes most issues:

# 1. Clear npm cache
npm cache clean --force

# 2. Reinstall tools
npx @j0kz/mcp-agents@latest

# 3. Fully restart editor (close ALL windows)

# 4. Test by asking AI: "What MCP tools are available?"
```

---

## Installation Guide

For complete platform-specific installation instructions:

```bash
cat .claude/skills/mcp-troubleshooting/references/installation-guide.md
```

### Quick Install Verification

```bash
# Check installation
ls -la ~/.config/claude/mcp-servers/  # Claude Code (Mac/Linux)
ls -la ~/AppData/Roaming/Claude/mcp-servers/  # Claude Code (Windows)

# Verify config exists
cat ~/.config/claude/mcp-servers-config.json  # Mac/Linux
cat ~/AppData/Roaming/Claude/mcp-servers-config.json  # Windows

# Test a tool directly
npx @j0kz/smart-reviewer@latest review test.ts
```

---

## Platform Configuration

For detailed platform-specific configuration:

```bash
cat .claude/skills/mcp-troubleshooting/references/platform-config-guide.md
```

### Config File Locations

| Editor | Mac/Linux | Windows |
|--------|-----------|---------|
| Claude Code | `~/.config/claude/` | `%APPDATA%\Claude\` |
| Cursor | `~/.cursor/` | `%APPDATA%\Cursor\` |
| Windsurf | `~/.windsurf/` | `%APPDATA%\Windsurf\` |
| VS Code | `~/.vscode/` | `%APPDATA%\Code\` |

---

## Common Issues & Solutions

### Issue 1: Tools Not Appearing

**Symptoms:** AI doesn't recognize MCP commands

**Solution:**
```bash
# 1. Check config file exists
cat ~/.config/claude/mcp-servers-config.json

# 2. Verify tools are listed
# Should see 9 entries for @j0kz tools

# 3. Restart editor completely
# Close ALL windows, not just reload

# 4. Ask AI to list tools
"What MCP tools are available?"
```

### Issue 2: Module Not Found

**Symptoms:** Error: Cannot find module '@j0kz/...'

**Solution:**
```bash
# 1. Clear cache
npm cache clean --force

# 2. Remove old installations
rm -rf ~/.npm/_npx/
rm -rf node_modules/

# 3. Reinstall
npx @j0kz/mcp-agents@latest --force

# 4. Use @latest tag
npx @j0kz/smart-reviewer@latest  # Always use @latest
```

### Issue 3: Permission Denied

**Symptoms:** EACCES or permission errors

**Solution:**
```bash
# Mac/Linux: Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Windows: Run as Administrator
# Right-click terminal → Run as Administrator
npx @j0kz/mcp-agents@latest
```

### Issue 4: Config Not Updating

**Symptoms:** Old tools still showing after update

**Solution:**
```bash
# 1. Backup existing config
cp ~/.config/claude/mcp-servers-config.json ~/mcp-backup.json

# 2. Remove and reinstall
rm ~/.config/claude/mcp-servers-config.json
npx @j0kz/mcp-agents@latest

# 3. Force restart editor
# Task Manager → End all editor processes
```

---

## Debugging Strategies

For comprehensive debugging approaches:

```bash
cat .claude/skills/mcp-troubleshooting/references/debugging-strategies.md
```

### Debug Commands

```bash
# Check npm global packages
npm list -g --depth=0

# View npm cache
npm cache ls

# Test specific tool version
npx @j0kz/smart-reviewer@1.0.36 --version

# Enable verbose logging
DEBUG=* npx @j0kz/smart-reviewer@latest review test.ts

# Check Node version (should be 18+)
node --version
```

---

## Error Messages Explained

### "Tool not found"
- Config file missing or corrupted
- Editor needs full restart
- Installation incomplete

### "Cannot execute binary"
- Node.js version too old (need 18+)
- Platform mismatch (ARM vs x64)
- Corrupted npm cache

### "ENOENT: no such file"
- Path in config is wrong
- Tool not installed properly
- Windows path escaping issue

### "Timeout waiting for response"
- Tool crashed during execution
- Memory limit exceeded
- Infinite loop in code being analyzed

---

## Advanced Troubleshooting

### Manual Config Edit

```json
// Example mcp-servers-config.json entry
{
  "@j0kz/smart-reviewer": {
    "command": "npx",
    "args": ["@j0kz/smart-reviewer-mcp@latest"],
    "description": "Smart code review with auto-fix"
  }
}
```

### Environment Variables

```bash
# Set Node memory limit
export NODE_OPTIONS="--max-old-space-size=4096"

# Enable debug output
export DEBUG=mcp:*

# Use specific npm registry
export NPM_CONFIG_REGISTRY=https://registry.npmjs.org/
```

### Network Issues

```bash
# Behind proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Clear proxy
npm config delete proxy
npm config delete https-proxy

# Use different registry
npm config set registry https://registry.npmjs.org/
```

---

## Recovery Procedures

### Complete Reset

```bash
# 1. Backup config
cp ~/.config/claude/mcp-servers-config.json ~/backup-mcp.json

# 2. Clean everything
npm cache clean --force
rm -rf ~/.npm/_npx/
rm ~/.config/claude/mcp-servers-config.json

# 3. Fresh install
npx @j0kz/mcp-agents@latest

# 4. Restart editor
```

### Rollback to Previous Version

```bash
# If latest version has issues
npx @j0kz/mcp-agents@1.0.35  # Use specific version

# Or install globally
npm install -g @j0kz/mcp-agents@1.0.35
```

---

## Getting Help

### Self-Diagnosis

```bash
# Run health check
npx @j0kz/mcp-agents@latest --health

# Version info
npx @j0kz/mcp-agents@latest --version

# List installed tools
cat ~/.config/claude/mcp-servers-config.json | grep "@j0kz"
```

### Report Issues

If problems persist:

1. Check GitHub Issues: https://github.com/j0KZ/mcp-agents/issues
2. Include:
   - Error message (full text)
   - Platform (OS, Node version)
   - Editor (Claude Code, Cursor, etc.)
   - Steps to reproduce
   - Config file contents

---

## Prevention Tips

1. **Always use @latest tag** in commands
2. **Fully restart editor** after config changes
3. **Keep Node.js updated** (v18+ required)
4. **Clear cache periodically** if issues arise
5. **Don't edit config while editor is running**
6. **Use one editor at a time** for MCP tools
7. **Check firewall/antivirus** isn't blocking npm

---

**Quick Test:** After troubleshooting, ask AI: "Use smart-reviewer to analyze a TypeScript file"