---
name: sweep-tracker
agent: hestia
description: Hestia's delegation tracker sweep skill. Reads DELEGATION_TRACKER.md, closes finished items, archives stale items beyond threshold, flags orphaned items. Returns counts. Edit-only on status fields.
allowed-tools: Read, Edit, Grep, Glob
user-invocable: true
triggers:
  - sweep tracker
  - clean delegation tracker
  - sweep delegation
  - tracker sweep
  - close finished items
  - archive stale items
  - DELEGATION_TRACKER sweep
  - clean up tracker
---

# Sweep Tracker

You are Hestia sweeping the DELEGATION_TRACKER. Terse. Factual. Lists only. No prose.

## What this skill does

Read `memory/DELEGATION_TRACKER.md` (or the path specified). Close finished items. Archive stale items that have passed the staleness threshold. Flag orphaned items (no owner, no update in 30+ days). Return counts of what was swept.

## Protocol

### Step 1: Read the tracker

Read `memory/DELEGATION_TRACKER.md` or the user-specified path in full.

### Step 2: Classify each item

For each item in the tracker:
- **DONE** — status is complete/closed/shipped → strike through with `~~` and add `closed: YYYY-MM-DD`
- **STALE** — last update >30 days ago, no resolved status → move to `## Archive` section with a note
- **ORPHANED** — no assignee or owner listed, open >14 days → flag with `> [!danger] Orphaned — no owner`
- **ACTIVE** — recently updated, clear owner, clear next step → leave untouched
- **BLOCKED** — explicitly marked blocked → leave untouched, add to report

### Step 3: Edit the tracker

Use Edit to:
- Strike through DONE items: `~~item text~~`
- Add `closed: YYYY-MM-DD` to DONE items
- Move STALE items to an `## Archive` section at the bottom
- Add orphan warnings

### Step 4: Return report (terse)

```
## Tracker Sweep — YYYY-MM-DD

Swept: N items
Closed: N (list item IDs or names)
Archived: N (list)
Flagged orphaned: N (list)
Blocked: N (list — no action taken)
Active/untouched: N
```

## Constraints

- Edit only status fields and `closed:` date additions. No rewriting item content.
- No Write tool. No new files. Edit only.
- No Bash, no Agent, no WebFetch.
- Report is bullet lists and counts only. No prose.
- If tracker file does not exist, say so and stop.
