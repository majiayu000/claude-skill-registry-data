---
name: cc
description: Short slash command wrapper for Claude relay sessions. Provides /cc commands like /cc on <project>, /cc tail, /cc off, and /cc <message> to interact with Claude Code through Telegram or other chat channels.
metadata: {"openclaw":{"emoji":"⚡","requires":{"bins":["tmux","claude"],"skills":["claude-relay"]}}}
---

# cc — Claude Code Quick Commands

A chat-friendly frontend for the `claude-relay` skill. Designed for Telegram and other messaging channels where typing full relay commands is cumbersome.

**Requires**: `claude-relay` skill must be installed.

## Script

Always execute the wrapper script:

```bash
{baseDir}/scripts/cc.sh <raw-args>
```

## Command reference

| Command | Action |
|---------|--------|
| `projects` / `list` | List available projects from map + project root |
| `on <project>` / `start <project>` | Start or reuse Claude session (supports fuzzy match) |
| `off [project]` / `stop [project]` | Stop session (default: last project) |
| `tail [project] [lines]` | Print recent output (default: 120 lines) |
| `status` | List active relay sessions |
| `<any text>` | Send as message to current project session |

When sending a message, if the first word resolves to a project alias with an active session, it's treated as an explicit project target with the rest as the message.

After sending a message, the script auto-waits and tails output. No need to manually tail.

## Relay mode (auto-forward)

Once a session is started (`on <project>`), enter **relay mode**:

- ALL subsequent user messages are automatically forwarded to Claude Code (no prefix needed).
- Agent acts as a pure passthrough: forward message → wait for output → return raw output. No added commentary.
- Relay mode ends when `off` is received or `/cc` menu is invoked.
- The `>> <text>` prefix still works as explicit send (strip the prefix), but is not required.
- Exception: messages that are clearly cc commands (`tail`, `off`, `status`, `projects`, `/cc`) are handled as commands, NOT forwarded.
- **No narration**: Do NOT add commentary, status text, or filler.
- **No progress messages**: Never send intermediate updates like "thinking...", "still processing...", etc.
- **Only message when**: (a) a user decision is needed, (b) the FINAL result is ready, or (c) something actually failed.
- **Batch updates**: For long processes with multiple steps, wait for the final outcome and send ONE summary.
- **Choices → Buttons**: When Claude Code output contains a numbered choice menu, convert to inline buttons with `callback_data` format `cc:reply:<number>`.
- **Long output**: If output is very long, summarize key points and offer a full tail button.

## Interactive buttons (Telegram)

When the platform supports inline buttons:

1. `/cc` (no args) → show action menu:
   - Row 1: [📋 Projects] [📊 Status]
   - Row 2: [⏹ Off]

2. `/cc on` (no project) → show project picker from projects.map

3. After successful `on <project>` → show: [📤 Tail] [⏹ Off]

4. Callback data format: `cc:on:<project>`, `cc:projects`, `cc:status`, `cc:tail`, `cc:off`

Use the `message` tool with `buttons` parameter for inline button menus.

## Critical: No duplicate messages

When using the `message` tool to send buttons/menus:
1. Do NOT write ANY text before or after the tool call
2. Your ENTIRE response must be: tool call → `NO_REPLY`
3. Any text you write becomes a SEPARATE visible message

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAUDE_RELAY_DIR` | (auto-detected) | Path to claude-relay skill directory |
| `CLAUDE_RELAY_ROOT` | `$HOME/projects` | Root directory for project discovery |
| `CLAUDE_RELAY_MAP` | `<relay-skill-dir>/projects.map` | Path to project alias map file |
