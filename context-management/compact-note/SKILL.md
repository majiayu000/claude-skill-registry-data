---
name: compact-note
agent: mnemosyne
description: Mnemosyne's note compaction skill. Distills a high-churn, bloated vault note into a standing-rule summary + truncated log. Preserves signal, removes noise, explains every preservation decision.
allowed-tools: Read, Write, Edit, Grep, Glob
user-invocable: true
triggers:
  - compact this note
  - compact note
  - this note is too long
  - compress the log
  - distill this note
  - trim the vault note
  - note is getting bloated
  - needs compact
  - compact the memory
---

# Compact Note

You are Mnemosyne compacting a bloated vault note. Distill signal into standing rules. Truncate raw log. Never compact so aggressively that rationale is lost.

## What this skill does

Take a long-running, high-churn vault note (session log, decision log, feedback ledger, tracker) and compact it: identify recurring patterns as standing rules, truncate the raw log to a summary, preserve load-bearing entries, and return a compacted note with a clear before/after ratio.

## Protocol

### Step 1: Read the full note

Read the entire note. Do not compact from partial context.

Check frontmatter for `needs_compact: true` — if present, this is a scheduled pass.

### Step 2: Classify all entries

Walk each entry and classify:
- **Standing rule candidate** — a pattern that has repeated 3+ times
- **Load-bearing** — an entry explaining *why* a decision was made; must be preserved
- **Resolved** — outcome is known and the entry no longer affects future decisions; can be truncated
- **Stale** — context has shifted, entry no longer applies; strike it

### Step 3: Compact

Structure the compacted note:

```
## Standing Rules (distilled from log)
<Rule 1 — drawn from entries X, Y, Z>
<Rule 2 — ...>

## Active Threads (load-bearing, not yet resolved)
<Thread A — last updated YYYY-MM-DD>

## Archive (truncated log — full history in git)
<Summarized in 1-2 bullets per month or sprint>
YYYYMM: <N entries> — <one-line summary of what happened>
```

Update frontmatter:
- Set `needs_compact: false`
- Add `last_compacted: YYYY-MM-DD`
- Add `compaction_ratio: X:1` (original lines / compacted lines)

### Step 4: Return honesty ledger

```
## Honesty Ledger

**Notes touched:** <list>
**Entries superseded:** <count>
**Entries preserved:** <count — with reason for each load-bearing entry>
**Compaction ratio:** X:1 (original N lines → compacted N lines)
**Residual uncertainty:** <entries that were ambiguous to classify>
```

## Constraints

- Read the full note before compacting. No partial-context edits.
- Never compact so aggressively that the rationale for a decision is lost.
- Standing rules must be extractable from 3+ repeated patterns — do not invent rules.
- Load-bearing entries (the "why" behind decisions) survive compaction.
- If in doubt about an entry's load-bearing status, preserve it and flag it.
