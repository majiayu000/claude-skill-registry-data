---
name: pending-queue
description: A Claude Code SessionStart hook that keeps an agent's follow-ups (chase a reply, re-run a script, check a deploy) in ~/.claude/pending.json and injects anything overdue or due within 3 days into every new session — so work items never go on your personal calendar and never get forgotten. Use when you say "remind me next session", "bring this up when we're working", "track this follow-up", "don't put that on my calendar", or want a lightweight in-session to-do queue for agents.
---

# pending-queue (SessionStart hook)

Work items whose only audience is a future agent session — "chase the records request on
the 14th", "re-run the scrape Monday", "check whether the deploy went READY" — don't belong
on a person's calendar: they clutter the month view, and a calendar row can't carry the
reference numbers and steps that make them actionable. This hook keeps them in a JSON file
and surfaces them as context when a session starts.

## Install

1. Copy `hooks/pending.py` to `~/.claude/hooks/pending.py`.
2. Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [ { "type": "command",
                     "command": "python3 ~/.claude/hooks/pending.py 2>/dev/null || true",
                     "timeout": 10 } ] }
    ]
  }
}
```

3. Create `~/.claude/pending.json` as a JSON array:

```json
[
  {"id": "_README", "what": "Entries: id, due (YYYY-MM-DD), project, what, how, done. Ids starting with _ are ignored."},
  {"id": "chase-county-request", "due": "2026-11-14", "project": "my-repo",
   "what": "Chase the county records request if no reply",
   "how": "Reference #R-123. Portal: <url>. Contact: records office. If still silent, file the appeal form.",
   "done": false}
]
```

## What it does

- Shows entries that are overdue or due within `SOON_DAYS` (3), capped at 12, sorted by
  date, with entries for the current project (matched on the cwd's folder name) first.
- Injects them via `hookSpecificOutput.additionalContext` and prints a one-line
  `systemMessage` ("2 pending follow-ups, 1 overdue").
- **Fails silent and open**: any error prints nothing and exits 0. A hook that breaks a
  session start is worse than a forgotten follow-up.
- Test the rendering with a fixture: `CLAUDE_PENDING_FILE=/tmp/p.json python3 ~/.claude/hooks/pending.py`.

## Rules for the agent

- **The `how` field must stand alone.** A future session gets no transcript; put the
  reference number, URL, contact and next step in it.
- **Rewrite an entry rather than adding a second one** for the same thread, so a chase never
  fires on a question already answered. Set `done: true` to retire it.
- Raise items when relevant to what the user is doing; don't derail them.
- Calendar vs. queue: appointments, travel, people, and irreversible actions only the human
  can take go on the calendar; everything whose only audience is a future session goes here.
