---
name: mcp-configuration-skill
description: "DEPRECATED - This skill references MCP servers that no longer exist in the codebase. The ConfigurationRegistry server was archived during MCP cleanup. Use native file system tools and flash-sidekick for configuration tasks."
tags: [deprecated, mcp, legacy]
status: archived
---

# ⚠️ DEPRECATED: MCP Configuration Skill

**STATUS:** This skill is deprecated and should not be used.

## Why This Skill Was Deprecated

During the MCP cleanup (December 2025), we simplified the MCP architecture from 6 custom servers to 3 production-ready servers:

1. **flash-sidekick** - Dual-engine Gemini wrapper (Flash 2.5 Lite + Pro 2.5)
2. **playwright** - Browser automation testing
3. **docker** - Container management

### Servers That Were Removed

- ❌ **ConfigurationRegistry** (`configuration-server.py`) - Moved to `_legacy_archive/`
- ❌ **CodebaseDocumentation** (`documentation-server.py`) - Moved to `_legacy_archive/`
- ❌ **GenKitFlowRegistry** - Never implemented
- ❌ **APIContractValidator** - Never implemented
- ❌ **DesignSystemServer** - Never implemented
- ❌ **FirestoreDataAccessServer** - Never implemented

### Reasons for Removal

1. **Reduced Complexity**: Custom servers added maintenance overhead
2. **Caching Issues**: Led to stale configuration states
3. **npm exec Errors**: Caused persistent CI/CD failures
4. **Redundancy**: File system tools provide the same functionality
5. **Single Source of Truth**: Direct file access is more reliable

## Migration Guide

### Old Approach (Using This Deprecated Skill)

```
method: list_scripts
Returns: Cached list of 84 scripts
Risk: Cache may be stale
```

### New Approach (Recommended)

```bash
# List all scripts directly
find scripts/ backend/scripts/ .claude/scripts/ -type f -name "*.sh" -o -name "*.py"

# Or use grep_search/find_by_name tools
grep_search for specific scripts
find_by_name for pattern matching
```

### Environment Configuration

Instead of using the MCP server:

```bash
# Development
cat .env.development

# Staging  
cat .env.staging

# Production
cat .env.production

# Validation
./scripts/validate-env.sh
```

## What To Use Instead

| Old MCP Method | New Approach |
|----------------|--------------|
| `list_scripts` | `find_by_name` tool with pattern matching |
| `get_environment` | Read `.env.*` files directly |
| `validate_all` | Run `./scripts/validate-env.sh` |
| `render_template` | Use `envsubst` or native templating |
| `index` | Direct file system queries |

## Current MCP Ecosystem

For actual MCP capabilities, use:

1. **flash-sidekick MCP** - `mcp_flash-sidekick_*` tools
   - `consult_pro` - Deep reasoning with Pro 2.5
   - `quick_summarize` - Fast summarization with Flash Lite
   - `generate_idf` - Python IDF generation

2. **GitHub MCP** - `mcp_github_*` tools
   - Repository management
   - PR/issue tracking
   - Code search

3. **Playwright MCP** - Browser automation (via browser_subagent)

4. **Docker MCP** - Container operations

## Related Documentation

- See conversation `0b3a6c3f-6c7e-4743-bc7c-a34b3bbe08e3` for MCP cleanup details
- Current MCP configuration: `/home/njd/careercopilot/careercopilot-1/mcp.json`
- Archived servers: `_legacy_archive/`

---

**Last Updated**: 2025-12-28  
**Deprecated**: 2025-12-27  
**Replacement**: Native file system tools + flash-sidekick MCP
