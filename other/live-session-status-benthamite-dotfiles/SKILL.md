---
name: live-session-status
description: Use when the user asks what another live Claude or Codex session is doing, or before telling the user that another session cannot be seen. Read-only; not for searching past sessions by topic or for messaging a peer.
---

# Report what a live peer session is doing

Every Claude and Codex session writes its conversation to a local transcript
as it runs. You can read it. Never tell Pablo another session is opaque or
cannot be seen; read its transcript and report.

## 1. Identify the peer

- In Claude Code, the `ListAgents` tool names the live peer sessions. Use it
  first when it is available.
- In Codex, or when no such tool exists, identify the peer by project
  directory and recency instead.
- Ask which session Pablo means only when several live candidates fit and the
  choice changes the answer.

## 2. Find its transcript

- Claude: `~/.claude/projects/<slug>/<session-id>.jsonl`. The slug is the
  session's absolute working directory with every character other than a
  letter, digit or `-` replaced by `-` (`/Users/me/My Drive/x` becomes
  `-Users-me-My-Drive-x`). The per-account `~/.claude-*/projects`
  directories link to the same store. Within a project, the live session is
  normally the most recently modified file other than your own.
- Codex: `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<session-id>.jsonl`.
  The first record (`session_meta`) holds the session's `cwd`. The
  per-account `~/.codex-*/sessions` directories link to the same store.
- Sessions in a linked worktree have that worktree as their directory
  (`~/repos/.worktrees/<repo>/<name>`), not the main checkout.
- `"$HOME/My Drive/dotfiles/claude/bin/agent-log-find" --raw --days 1 TERMS`
  lists recently modified transcripts whose text matches the terms, when the
  directory is unknown.

## 3. Read its latest messages

Use the read-only helper in this skill's `scripts/` directory (resolve the
directory containing this `SKILL.md` as `SKILL_DIR`). It prints the last user
and assistant text messages with local timestamps, skipping tool calls and
truncating each message to 700 characters.

```sh
# A known transcript
python3 "$SKILL_DIR/scripts/session_tail.py" PATH.jsonl -n 8
# Newest Claude session in a project, excluding your own session id
python3 "$SKILL_DIR/scripts/session_tail.py" --latest "$PROJECT_DIR" --exclude "$OWN_SESSION_ID"
# Newest Codex session whose cwd is the project
python3 "$SKILL_DIR/scripts/session_tail.py" --latest "$PROJECT_DIR" --codex
```

The header shows the transcript path, when it was last written, its working
directory and, for Claude, its title. Raise `-n` when the recent messages do
not show the task.

## 4. Report

Say in plain words what the session is working on, what it last did or said,
and whether it is waiting on Pablo. Give the last-written time so stale
sessions are obvious. If no transcript can be found, say which locations you
checked; do not claim the session is invisible.
