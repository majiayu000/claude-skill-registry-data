---
name: tabs
description: Use when the user asks to "list my claude sessions", "which windows are waiting", "/ar:tabs". Discovers Claude sessions across tmux windows and reports which need attention.
allowed-tools: Bash(tmux *), Bash(uv *)
argument-hint: "[A,B:command] or [all:continue] or [awaiting:status]"
---

# Claude Session Manager

<purpose>

Discover, analyze, and interact with Claude Code sessions across tmux windows.

## Context

Current tmux sessions and Claude windows:

Run `tmux list-sessions` and read its output before choosing a session.

## Your Task

The user's request is the task description for everything below.

If no arguments provided, discover all Claude sessions and present them to the user.

</purpose>

<workflow>

## Workflow

1. **Discover** - Run the discovery script to get session data
2. **Present** - Show sessions as table with letter labels (A, B, C...)
3. **Ask** - Get user selection for which sessions to interact with
4. **Execute** - Run commands on selected sessions

## Discovery

```bash
"${CLAUDE_PLUGIN_ROOT}/commands/tabs-exec"
```

## User Selection Syntax

| Syntax | Meaning |
|--------|---------|
| `A,C` or `AC` | Select sessions A and C |
| `A:git status` | Run custom command on session A |
| `B:pwd, C:git log` | Different commands per session |
| `all:continue` | Execute on all discovered sessions |
| `awaiting:continue` | Execute only on sessions awaiting input |

## Execution

After user confirms, execute via:

```bash
# Using tabs-exec
# NOTE: --execute requires the full session JSON from discovery phase, not a minimal stub.
# Claude should pass the full session data obtained from the discovery run above.
echo '{"selections": "B,C", "command": "continue", "sessions": [...session_data_from_discovery...]}' | "${CLAUDE_PLUGIN_ROOT}/commands/tabs-exec" --execute

# Direct tmux (for simple commands)
tmux send-keys -t "session:window" "command"
tmux send-keys -t "session:window" C-m   # Enter as a separate call, as tmux-automation requires
```

## Prompt Types

When discovering sessions, detect what state each Claude session is in:

| Type | Visual Indicator |
|------|------------------|
| `input` | Standalone `>` prompt - ready for input |
| `plan_approval` | "Would you like to proceed?" |
| `tool_permission` | `[Y/n]` or numbered options `[1] [2]` |
| `question` | Multi-choice with ❯ selector |
| `clarification` | Question ending with `?` |
| `working` | No prompt detected - Claude is active |

</workflow>

<output_contract>

## Session Table Format

Present discovered sessions as:

```
| # | Session | Purpose | Status |
|---|---------|---------|--------|
| A | main:3  | Feature dev | awaiting input |
| B | main:5  | Testing     | working |
| C | work:1  | Bug fix     | plan approval |
```

Then ask: "Which sessions would you like to interact with?"

**Related**:
- `agents/tmux-session-automation.md` (agent `ar:tmux-session-automation`) - Advanced session lifecycle automation
- `agents/cli-test-automation.md` (agent `ar:cli-test-automation`) - CLI testing automation patterns

**Implementation**: See `tabs-exec` script for discovery and execution logic.

</output_contract>
