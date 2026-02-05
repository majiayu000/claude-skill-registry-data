---
name: claude-hooks-developer
description: Create, configure, and manage Claude Code hooks for workflow automation, validation, and security. Guides hook implementation, configuration patterns, and best practices.
---

# Claude Code Hooks Developer

Compact skill for creating and managing Claude Code hooks that intercept tool calls, validate operations, and enhance workflows.

## When to Use

Activate when the user:
- Needs to create a new hook (PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc.)
- Wants to configure hooks in `.claude/settings.json` or `.claude/settings.local.json`
- Asks about hook lifecycle events or available hook types
- Needs to validate/block operations, format files, or send notifications
- Mentions security controls, file protection, or command validation
- Wants examples of hook patterns or common use cases

## Core Capabilities

- **Hook Types**: Guide selection between PreToolUse, PostToolUse, UserPromptSubmit, Stop, SubagentStop, SessionStart, Notification, PermissionRequest
- **Hook Configuration**: Generate correct JSON structure for `settings.json` with matchers, commands, and paths
- **Script Templates**: Provide Python/Bash templates for common hook patterns
- **Security Patterns**: Implement file protection, dangerous command blocking, and access control
- **Environment Variables**: Utilize CLAUDE_PROJECT_DIR, CLAUDE_TOOL_INPUT_*, and other hook context
- **Decision Control**: Properly use exit codes (0=approve, 2=block) and JSON decision objects
- **Common Use Cases**: Format files, validate commands, send notifications, log operations, enforce policies

## Quick Workflow

1. Identify the hook event type based on the desired trigger point
2. Create the hook script in `.claude/hooks/` (Python or Bash)
3. Make script executable (`chmod +x`)
4. Add hook configuration to `.claude/settings.json` or `.claude/settings.local.json`
5. Test the hook with relevant tool operations
6. Verify proper exit codes and error messages

## Hook Event Types

- **PreToolUse**: Runs before tool execution (can block/modify)
- **PostToolUse**: Runs after tool execution (validation/cleanup)
- **UserPromptSubmit**: Validates user prompts before processing
- **Stop**: Controls whether Claude continues working
- **SubagentStop**: Controls sub-agent continuation
- **SessionStart**: Runs at session initialization
- **Notification**: Responds to system notifications
- **PermissionRequest**: Auto-approves/denies permission dialogs

## Exit Codes

- **0**: Approve/Success - operation continues
- **2**: Block - operation blocked with error message
- **Other**: Error - operation fails

## Reference Documentation

- **Detailed Workflows & Patterns**: See `reference.md` in this directory
- **Real-World Usage Examples**: See `examples.md` in this directory
- **Hook Configuration Guide**: `.claude/hooks/doc-standards-reminder.sh` (example)
