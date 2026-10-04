---
name: improve-system
description: 'The self-improvement loop — parse freshly synced /raw data, auto-apply low-risk fixes, write high-stakes proposals to output/review_[date].md for sign-off. Use for the scheduled routine or "improve the system".'
---

# Improve System

Parse freshly synced raw data and turn it into workspace improvements,
segregated into three explicit risk tiers. This is the command the **System
Improvements routine** fires (Tuesday and Friday afternoons, after
`/data-ingestion`).

## Step 1 — Process pending reviews first

Before proposing anything new, look for previous `output/review_*.md` files
containing checked boxes:

- `[x] Approve` → apply that change now, then mark the item `(applied YYYY-MM-DD)`
- `[x] Reject` → mark it `(dismissed)` and never re-propose it
- Answered context questions → fold the answer into this run's analysis

## Step 2 — Analyze fresh data

Read `output/.improvement-log.md` for the last run date (if missing, this is
the first run). Scan `wiki/index.md` for entries added since then, opening raw
files only where the index summary suggests a lesson. Look for:

- Recurring mistakes across session digests
- Manual workflows repeated 2+ times (skill candidates)
- Wiki entries contradicted by newer curated content
- Data bloat: unindexed raw files, duplicate entries, dead links
- Skills/config that session evidence shows are misfiring

## Step 3 — Segregate into tiers

**Tier 1 — Auto-approve** (apply quietly now):
Low-risk hygiene only — indexing unindexed raw files, fixing dead wiki links,
deduplicating index rows, linking matching files, tidying data bloat. Never
anything under `.claude/` or CLAUDE.md. Append each applied change as one line
to the hidden log `output/.improvement-log.md`
(`YYYY-MM-DD | auto | <what> | <why>`).

**Tier 2 — Needs sign-off** (propose, don't touch):
Changing CLAUDE.md/system prompts, modifying or creating skills, altering
routines or settings, deleting anything. Write each to today's review file
`output/review_YYYY-MM-DD.md`:

```
### Proposal N: <title>
- **What**: <exact change, with file paths>
- **Why**: <evidence from raw/wiki, with links>
- **Risk**: <what could break>
- [ ] Approve
- [ ] Reject
```

**Tier 3 — More context required**:
For findings that need the user's judgment, append explicit questions to the
same review file under `## Questions for you`, each with the context needed to
answer inline.

## Step 4 — Report

```
## Improve System — YYYY-MM-DD
- Reviews processed: <n approved applied, n rejected dismissed>
- Auto-applied: <n> (see output/.improvement-log.md)
- Awaiting sign-off: <n> in output/review_YYYY-MM-DD.md
- Questions: <n>
```

If there were zero findings in every tier, say so and skip creating a review
file. When run by a scheduled routine, commit and push to
`knowledge-base-updates` as the routine prompt instructs — an ephemeral
container discards uncommitted work. Otherwise do not commit unless the user
asks.
