---
name: activity-summary
description: Use when an agent is asked "what did I (or my team) work on yesterday / this week / today" across provider data in a relayfile mount (Linear, GitHub, Notion, Slack, Confluence, Jira, etc.). Tells the agent to consult the pre-computed `digests/yesterday.md` (and sibling digest files) at the workspace root BEFORE doing manual exploration with `ls`/`grep`/`find`. The digest is deterministic, exhaustive over the window, and costs one file read instead of dozens of provider queries.
---

# Activity Summary — Read the Digest First

## Overview

A relayfile workspace pre-computes deterministic daily activity digests at `<mount>/digests/`. These are produced by relayfile itself from the raw provider data, so they are **complete over the time window** (no API pagination gaps) and **free for the agent to consume** (one file read, no LLM generation step).

If you've been asked an activity-summary question, **read the digest before doing anything else.** Reaching for `ls`, `grep`, or per-provider exploration first is the most common reason these answers cost 20+ tool calls when they could cost 1.

## When to use this skill

Trigger phrases from the user — read the digest first:

- "what did I work on yesterday / today / this week"
- "what changed across {GitHub, Linear, Notion, Slack, ...} {yesterday, since Friday, etc.}"
- "summarize my activity"
- "give me a standup update"
- "what did $team_member ship recently"

If the user's question is **not** windowed by time (e.g. "find the Notion page about onboarding"), the digest is not the right entry point — use `by-title/` or `by-id/` indexes instead. See the `workspace-layout` skill.

## What digests look like

```bash
$ ls $MOUNT/digests/
yesterday.md      # rolling — generated at 00:00 local for the prior calendar day
today.md          # rolling — updated continuously as the day progresses
2026-05-12.md     # date-stamped, immutable once the day closes
2026-05-11.md
...
this-week.md      # rolling — Mon→now of the current ISO week
last-week.md      # immutable, prior ISO week
```

The body is plain Markdown with one section per provider:

```markdown
# Activity for 2026-05-12

## linear
- AGE-16 moved to Blocked (waiting on design) — [/linear/issues/AGE-16__87389837-...]
- AGE-9 closed — [/linear/issues/AGE-9__2bb2c00f-...]

## github
- relayfile-adapters#412 merged to main — [/github/repos/.../pulls/412.json]
- relayfile#287 opened — [/github/repos/.../pulls/287.json]

## notion
- "Khaliq's To Dos" edited — [/notion/pages/3566800c-.../content.md]

## slack
- 7 messages in #gtm-prospects mentioning "ACME"
```

Each bullet links to the canonical file in the mount, so a follow-up question ("what changed about AGE-16?") is one `cat` away.

## How to use it

```bash
# 1. Check the digest covers the date the user asked about.
ls $MOUNT/digests/
cat $MOUNT/digests/yesterday.md

# 2. If the user asked about a specific date, prefer the date-stamped file.
cat $MOUNT/digests/2026-05-12.md

# 3. Confirm coverage before answering. The digest header includes the window
#    it spans; if the user's window is wider, read multiple digest files
#    rather than re-deriving from raw provider data.
head -5 $MOUNT/digests/this-week.md
```

That is usually the entire workflow: read → quote → done. Four tool calls or fewer.

## When to fall back to exploration

The digest is the right answer when:

- The window matches a digest file (yesterday, today, a specific past date, this/last week).
- The user wants **everything** in the window, not a filtered slice.

Fall back to direct exploration via `by-edited/<date>/` index subtrees when:

- The window is unusual (e.g. "the last 36 hours"). Use `by-edited/` indexes; see `workspace-layout`.
- The user wants a filter the digest doesn't pre-compute (e.g. "only Linear issues assigned to me").
- The digest file is missing or its header indicates incomplete provider coverage.

## Why this matters

In our published benchmarks, the activity-summary question dropped from ~20 turns and $0.30+ to 4 turns and ~$0.07 once the digest existed and the agent read it first. The digest is one file read that replaces ~25 individual provider queries.

If you find yourself listing more than 2-3 directories to answer an activity question, stop and check `digests/` — you're almost certainly working harder than you need to.
