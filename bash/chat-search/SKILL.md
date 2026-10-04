---
name: chat-search
description: Use when a user asks to search local Codex chat history by keyword, recall a past conversation, find an old thread title, or look up prior user or assistant snippets stored in this machine's ~/.codex sessions.
---

# Chat Search

## Overview

This is the short alias for local Codex conversation search.
Use the shared search script instead of manually grepping `~/.codex`.
If you want a shell command, use `codex-chat-search`.

## Workflow

Run:

```bash
codex-chat-search <keyword ...>
```

Keep the default role filter unless you explicitly need prompt or AGENTS text.
Use `--help` for the full flag list.

## Quick Reference

| Need | Command |
| --- | --- |
| Search title + messages | `codex-chat-search arbitrage morpho` |
| Only thread titles | `codex-chat-search morpho --scope title` |
| Archived threads only | `codex-chat-search skill --archived only` |
| JSON output | `codex-chat-search pnl review --json` |

## Common Mistakes

- Do not use this for repo code search.
- Do not add `developer` unless you really want system prompt noise.
- Add another keyword or a date filter when the query is too broad.
- If `codex-chat-search` was just installed in the current `zsh` shell and does
  not run immediately, execute `rehash` once.
