---
name: find-session
description: Use when the user asks to find, reopen or resume a past Claude Code session from a description ("the session where I…", "find the thread about…", "/find-session …"). Finds it and, if exactly one matches, opens it in a new tmux window named after the session.
user-invocable: true
argument-hint: "<description of the session>"
---

# Find session

Helper: `~/.claude/skills/find-session/find_session.py` (`search` and `launch`).

## 1. Search

Turn the description into 2–5 distinctive keywords: names, ticket/PR numbers,
product names, model names, email addresses. Include spelling variants as separate
keywords, e.g. `PRD7` `"PRD 7"` `PRD-7`, `whitelist` `allowlist`. Resolve relative
dates against today ("last Friday" → `--since`/`--until` that day; "recently" →
`--since` about 3 weeks ago).

```bash
python3 ~/.claude/skills/find-session/find_session.py search KW1 KW2 ... [--since YYYY-MM-DD] [--until YYYY-MM-DD] [--project apps]
```

Each output line is one candidate (JSON): id, title, cwd, first/last prompt time,
matched keywords, matching prompts, and `open_in` if it is already running.
Ranking is by how many distinct keywords matched, then number of matching prompts.

- `NO_MATCHES` or weak hits only: retry with other keywords or a wider date range,
  then with `--deep` (also searches the full transcripts, slower; `transcript_hits`
  per keyword).
- Read the matching prompts and judge which candidate fits the description. Don't
  just take the top row: in the user's history the same word often appears in
  unrelated sessions (e.g. the supervisor session's own lookups; skip it).

## 2. Exactly one fits

```bash
python3 ~/.claude/skills/find-session/find_session.py launch <session-id> [--name "<name>"]
```

- The window is named after the session's title. If the session has no title, pass
  `--name` with a short name (2–4 words) from what the session was about.
- It opens a detached window in the current tmux session, `cd`s to the session's
  directory and types `claude --resume <id>` into the shell, so the user's `claude`
  alias is used. Never run the claude binary directly.
- `ALREADY_OPEN <window>` means it is running; don't open a second copy, point the
  user to that window.

Reply in two or three lines: the window (`twid:<n> <name>`) to switch to, and one
line on what the session was about and when it was last used.

## 3. Several plausible, or none

Don't launch. List the top candidates (at most 5), one line each: title or first
prompt, project, last used, session id. Ask which one; launch on the reply.
