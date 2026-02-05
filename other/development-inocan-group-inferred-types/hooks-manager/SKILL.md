---
name: hooks-manager
description: Manage Claude Code hooks for workflow automation. Create, configure, test, and debug hooks that execute at various lifecycle points. Supports all hook events (PreToolUse, PostToolUse, SessionStart, etc.) with examples and best practices.
version: 1.0.0
---

# Hooks Manager

Manage Claude Code hooks for deterministic workflow automation.

## When to Use

- Creating or modifying hooks for workflow automation
- Testing hook configurations before deployment
- Debugging hook execution issues
- Understanding hook event types and matchers
- Implementing security-aware hook patterns
- Managing project or user-level hook configurations

## What This Skill Does

**Guides you through Claude Code hook management**:

- **Hook Creation**: Generate hook configurations with proper syntax
- **Event Types**: Understand all 9 hook events and when they trigger
- **Security**: Implement hooks with proper security considerations
- **Testing**: Validate hooks before deployment
- **Examples**: Access common hook patterns and implementations
- **Debugging**: Troubleshoot hook execution issues

## 🎯 Core Principle: Hook Lifecycle

**Hooks execute at 9 lifecycle points:**

| Event | Timing | Can Block? (Exit 2) |
|-------|--------|---------------------|
| PreToolUse | Before tool execution | ✅ Yes (blocks tool) |
| PostToolUse | After tool completion | ⚠️ Partial (tool already ran, feeds stderr to Claude) |
| UserPromptSubmit | Before AI processing | ✅ Yes (erases prompt) |
| SessionStart | Session begins/resumes | ❌ No |
| SessionEnd | Session terminates | ❌ No |
| Stop | Claude finishes responding | ✅ Yes (blocks stoppage) |
| SubagentStop | Subagent completes | ✅ Yes (blocks stoppage) |
| PreCompact | Before memory compaction | ✅ Yes (blocks compaction) |
| Notification | Claude sends notification | ❌ No |

**Exit Codes:**
- **0**: Success (stdout visible in transcript mode)
- **2**: Blocking error (stderr fed to Claude or shown to user)
- **Other**: Non-blocking error (stderr shown to user)

→ [Complete Event Types Reference](./reference/event-types.md) - Detailed documentation with examples

## Plugin Hooks Configuration

**PRISM uses plugin-level hooks** configured in `hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/my-hook.py"
          }
        ]
      }
    ]
  }
}
```

**Critical:** Use `${CLAUDE_PLUGIN_ROOT}` for all plugin paths (not relative paths)

→ [Complete Configuration Reference](./reference/commands.md#configuration-format) for full schema

## Quick Start

### Create Your First Hook (Recommended)

1. **Read the event table above** (30 seconds)
2. **Browse examples**: `*hook-examples` (2 min)
3. **Create hook**: `*create-hook` (guided setup)
4. **Test hook**: `*test-hook [name]` (validation)

**Result**: A working hook following best practices

### Quick Lookup (While Building)

Need a command or pattern right now?

→ [Commands Reference](./reference/commands.md) - All 15 commands with examples
→ [Examples Library](./reference/examples.md) - 13 pre-built hook patterns

### Learn Hook System (Deep Dive)

Want to understand hook architecture?

→ [Event Types Reference](./reference/event-types.md) - Complete event documentation
→ [Security Best Practices](./reference/security.md) - Hook security guide

## Available Commands

| Category | Commands |
|----------|----------|
| **Management** | `list-hooks`, `create-hook`, `edit-hook {name}`, `delete-hook {name}`, `enable-hook {name}`, `disable-hook {name}` |
| **Testing** | `test-hook {name}`, `debug-hook {name}`, `validate-config` |
| **Examples** | `hook-examples`, `event-types`, `install-example {name}` |
| **Sharing** | `export-hooks`, `import-hooks {file}` |

→ [Full Command Reference](./reference/commands.md) for detailed usage

## Hook Examples Library

Quick access to 13 pre-built patterns:

- **Logging**: bash-command-logger, file-change-tracker, workflow-auditor
- **Safety**: file-protection, git-safety, syntax-validator
- **Automation**: auto-formatter, auto-tester, auto-commit
- **Notifications**: desktop-alerts, slack-integration, completion-notifier
- **PRISM**: story-context-enforcer

→ [Complete Examples](./reference/examples.md) with full implementations

## Integration with PRISM

The hooks-manager skill enables automation for:

- **Workflow Validation**: Enforce story context in core-development-cycle
- **Quality Gates**: Auto-run tests and validation
- **PSP Tracking**: Auto-update timestamps and metrics
- **Skill Integration**: Hook into any PRISM skill command

**Current PRISM Hooks**:
- `enforce-story-context` - Block workflow commands without active story
- `track-current-story` - Capture story file from *draft command
- `validate-story-updates` - Ensure required sections exist
- `validate-required-sections` - Status-based section validation

## Available Reference Files

All detailed content lives in reference files (progressive disclosure):

- **[Commands Reference](./reference/commands.md)** (~4.5k tokens) - Complete command documentation
- **[Event Types](./reference/event-types.md)** (~4.6k tokens) - All 9 events with examples
- **[Examples Library](./reference/examples.md)** (~4.2k tokens) - 13 pre-built patterns
- **[Security Guide](./reference/security.md)** - Security checklist and best practices

## Common Questions

**Q: Where do I start?**
A: Run `*hook-examples` to browse patterns, then `*create-hook` for guided setup

**Q: Which event should I use?**
A: See [Event Types Reference](./reference/event-types.md) for complete guide

**Q: Can I see working examples?**
A: Yes! Run `*hook-examples` or see [Examples Library](./reference/examples.md)

**Q: How do I test before deployment?**
A: Use `*test-hook [name]` to validate with sample input

**Q: How do I share hooks with my team?**
A: Use `*export-hooks` and commit to `.claude/settings.json`

## Triggers

This skill activates when you mention:
- "create a hook" or "manage hooks"
- "hook automation" or "workflow hooks"
- "PreToolUse" or "PostToolUse" (event names)
- "test hook" or "debug hook"

---

**Need help?** Use `*hook-examples` to browse patterns or `*create-hook` for guided setup.
