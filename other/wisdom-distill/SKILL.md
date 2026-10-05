---
name: wisdom-distill
description: >-
  Squeeze three to five durable lessons out of the owner's own words from the last seven days
  into a weekly note in the insights folder. The LLM reads only a collector's digest, never the
  raw corpus. Triggers: "/wisdom-distill", "distill my week", "weekly wisdom".
license: MIT
---

# /wisdom-distill — the wisdom of the week

> 🧒 When reporting to a non-technical operator, end with an "In plain words" recap in their language.

## Run (deterministic first — 0 tokens)
`python "$IMPORTS_ROOT/wisdom_week_gather.py"` (or `... 14` for a 14-day window) ->
notes marked `origin: anton`/`#anton-original` inside the window (date field, mtime as fallback), excluding
`_originals/_imports/_Dashboards`, capped at 60 x 500 chars -> `$IMPORTS_ROOT/_wisdom_week_digest.md`.
**The LLM reads only the digest, never the corpus.**

## Distill (top model — synthesis, not grunt work)
From the digest, pull 3-5 durable lessons of the week (each must survive a month; "how the owner now thinks/decides").
Format: the lesson in one line in the owner's voice · Source: [[note-a]], [[note-b]] (2+ = stronger) ·
What it changes: which decision it will show up in. Drop transient items, other people's ideas, the self-evident.
Thin week (<3) — say so plainly, do not invent.

## Save (backup-first: vault_backup.py)
Note: $OBSIDIAN_VAULT/03-Insights/insight-weekly-wisdom-YYYY-Www.md
Frontmatter: title, date, type: insight, origin: anton, authored_by: hybrid,
tags: [insight, weekly-wisdom, anton-original], summary. Link the sources
(no-orphan-notes-rule); if beliefs are touched, link the matching belief-* note. NO 🧒 block inside the note.

## Scheduled twin
Cron `wisdom-distill-weekly`: Sunday 23:20 local time (routines-run-at-night). Gatherer ->
distillation (top-model subagent) -> note -> announcement in the fleet log chat (bus_ping.py --post).
The manual twin is this skill. Single source of truth = wisdom_week_gather.py.

## Related
Active-brain map A-E: item D · /five-hard (monthly) · /precedent (decisions) · recurring_scan.py
(the whole corpus) · vault-backup-rule · model-routing (synthesis -> top model).



<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
