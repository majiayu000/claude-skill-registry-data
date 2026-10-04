---
name: es-digest
version: 1.0.0
description: Produce a daily or weekly cross-source digest — mentions, action items, and decisions that need attention, not raw activity.
author: matrixx0070
tags: [enterprise-search, digest, action-items, decisions, summary, catch-up]
capabilities: []
---

# Enterprise Search Digest

## When to use
Reach for this to catch someone up on what happened across their tools over a period — start of day, Monday morning, or after time away. You scan every connected source for the window and return what needs attention, filtering out raw noise.

**Not for:** answering a specific "where is X" question (es-search); reconciling conflicting facts into one answer (es-knowledge-synthesis); or configuring which sources feed the digest (es-source-management).

## Method
1. **Set the window and owner.** Confirm the period (default: since last digest, else last 24h or 7d) and whose perspective — the "you" whose mentions and action items matter. *Decision:* if no last-digest timestamp exists, default to 24h for daily, 7d for weekly.
2. **Sweep sources** in the window — chat, email, storage, trackers — scoped to items involving the owner or their teams and projects.
3. **Classify each item:** direct mention/request, action item (owner must do something), decision made, or notable FYI. Drop pure noise.
4. **Extract action items.** Capture the task, who asked, the source link, and any due date. *Decision:* flag anything overdue or blocking others to the top.
5. **Capture decisions** — what was decided, by whom, the thread — so the owner isn't relitigating settled calls.
6. **Prioritize** by urgency and whether the owner is the bottleneck. Lead with what breaks if ignored.

## Example
Weekly digest, owner = Priya. Sweep surfaces 40 items; you drop 31 as noise. "Needs you now": a Slack @Priya asking for signoff on the vendor contract (blocking legal, 2 days old). Action items: "Review PR #212" (from Dev, due Fri, link), "Reply to auditor email" (overdue). Decisions: "Team chose Postgres over Mongo" (arch channel, link). FYI: office moved to floor 3. Quiet: Drive — nothing relevant.

## Pitfalls
- Dumping all activity instead of filtering to what involves the owner and needs action.
- Listing action items without owner, due date, or link, so they aren't actionable.
- Burying an overdue blocker below chronological or per-source ordering.
- Re-surfacing already-settled decisions as if open, prompting relitigation.

## Output format
```
Period: <window>  |  Sources scanned: <list>

Needs you now:
- <item> — <why urgent> — <link>   (most urgent first)

Action items:
- [ ] <task> — from <who> — due <date> — <link>

Decisions:
- <what> — by <who> — <link>

FYI: <brief notable, no action needed>
Quiet: <sources with nothing relevant>
```
