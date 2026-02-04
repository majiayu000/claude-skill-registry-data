---
name: handler-work-tracker-linear
description: "[DEPRECATED] Linear handler - Use Fractary CLI instead"
model: haiku
handler_type: work-tracker
platform: linear
deprecated: true
---

# Linear Work Tracker Handler

> **⚠️ DEPRECATED**: This handler is deprecated. Skills now use Fractary CLI (`fractary work <command>`) directly instead of platform-specific handlers.
>
> **Migration**: See `specs/WORK-00356-implement-faber-cli-work-commands.md` for the CLI migration plan.

<CONTEXT>
You are the Linear handler for the work plugin. This handler is **DEPRECATED** as of the CLI migration.

**New approach**: Skills invoke `fractary work <command> --json` directly instead of routing through platform-specific handlers.

**Why deprecated**:
1. CLI provides platform abstraction at a lower level
2. Reduces context by eliminating handler layer
3. Simplifies skill implementations
4. Centralized maintenance in CLI codebase
</CONTEXT>

<CRITICAL_RULES>
1. **DEPRECATED** - Do not use this handler for new implementations
2. Skills should use Fractary CLI directly: `fractary work <command> --json`
3. Existing scripts retained for backward compatibility only
4. No new features will be added to this handler
</CRITICAL_RULES>

## Migration Guide

### Before (Handler-based)
```
Skill → Handler → scripts/*.sh → Linear GraphQL API
```

### After (CLI-based)
```
Skill → Fractary CLI → Linear GraphQL API
```

### Example Migration

**Before (deprecated):**
```bash
# Skill invokes handler script
./scripts/fetch-issue.sh TEAM-123
```

**After (recommended):**
```bash
# Skill invokes CLI directly
fractary work issue fetch TEAM-123 --json
```

## CLI Command Mapping

| Handler Operation | CLI Command | Status |
|-------------------|-------------|--------|
| fetch-issue | `fractary work issue fetch <id>` | ✅ Available |
| create-issue | `fractary work issue create` | ✅ Available |
| update-issue | `fractary work issue update <id>` | ✅ Available |
| close-issue | `fractary work issue close <id>` | ✅ Available |
| reopen-issue | `fractary work issue reopen <id>` | ❌ Missing |
| list-issues | `fractary work issue search` | ✅ Available |
| create-comment | `fractary work comment create <id>` | ✅ Available |
| list-comments | `fractary work comment list <id>` | ✅ Available |
| add-label | `fractary work label add <id>` | ✅ Available |
| remove-label | `fractary work label remove <id>` | ✅ Available |
| assign-issue | `fractary work issue assign <id>` | ❌ Missing |
| classify-issue | `fractary work issue classify <id>` | ❌ Missing |

## Backward Compatibility

Existing scripts in `scripts/` are retained for:
- Backward compatibility with old skill versions
- Reference implementations for CLI development
- Testing and validation

Scripts will be removed in a future major version once CLI migration is complete.

## Dependencies (for legacy scripts)

### Required Tools
- `curl` - HTTP requests
- `jq` - JSON processor

### Environment Variables
- `LINEAR_API_KEY` - Linear API key

## Script Locations (Legacy)

```
handler-work-tracker-linear/
├── SKILL.md (this file)
├── scripts/                    # DEPRECATED - for backward compatibility only
│   ├── fetch-issue.sh
│   ├── classify-issue.sh
│   ├── create-comment.sh
│   ├── add-label.sh
│   ├── remove-label.sh
│   ├── close-issue.sh
│   ├── reopen-issue.sh
│   ├── update-state.sh
│   ├── list-issues.sh
│   └── ...
└── docs/
    └── linear-api.md
```

## Linear-Specific Notes (Reference)

### Authentication
Linear uses Bearer token authentication with API key.

### Issue Identifiers
Format: `TEAM-NUMBER` (e.g., ENG-123) or UUIDs internally.

### GraphQL API
Linear uses GraphQL for all operations.

### UUID Lookups
Labels, states, and users are referenced by UUID. Scripts must lookup UUIDs by name.

## See Also

- `specs/WORK-00356-implement-faber-cli-work-commands.md` - CLI migration spec
- `specs/WORK-00356-1-missing-cli-work-commands.md` - Missing CLI commands
- `plugins/work/skills/cli-helper/SKILL.md` - CLI invocation patterns
