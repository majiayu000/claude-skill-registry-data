---
name: find-past-session
description: 'Find or recall a past Claude or Codex session. Use when the user refers to an earlier session ("the session from yesterday", "what did we do about X", "find the session where…") or names an Emacs buffer such as *agent-log-search*. Not for what a live session is doing now (live-session-status).'
user-invocable: false
---

# Find a past session

1. Run `"$HOME/My Drive/dotfiles/claude/bin/agent-log-find" --since YYYY-MM-DD TERMS…`
   first. It searches the rendered Claude and Codex logs
   (`~/.claude/rendered/<project>/<date>_<slug>.md`, with summaries) in under a
   second.
2. Add `--body` to search full logs. Add `--raw` only for sessions too recent
   to be rendered.
3. Never start by grepping raw JSONL transcripts.
4. When Pablo names an Emacs buffer such as `*agent-log-search*`, read it with
   `emacsclient -e` and follow the session links in it.
