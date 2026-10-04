---
name: earnings-sweep
description: Earnings-season triage across ALL active theses (not just Live Portfolio holdings) — every earnings call reported inside the window gets a Quartr event summary, a Conviction-Trigger/Outstanding-Questions cross-reference, and a coverage check against existing Research notes, producing a ranked deep-read queue for /transcript. Use when user says "earnings sweep", "who reported", "triage earnings", "catch up on earnings season", or after any earnings-heavy stretch. Default window 14 days; `/earnings-sweep 90` covers a full season.
model: opus
effort: high
allowed-tools: Read Grep Glob Edit Write ToolSearch mcp__quartr Bash(date * jq * ls * cat * grep * printf * wc * find *)
---

The breadth layer `/transcript` lacks: one pass over every active-thesis earnings call in the window, cheap summaries first, so the expensive deep reads land only where a thesis is actually touched. Universe = **all `status: active` theses** via the `/event-sweep`-maintained "Vault Active" watchlist (which mirrors exactly that set, self-healing on `/status` transitions) — NOT the Live Portfolio holdings table, which is a subset. Output is a scanning surface in `Daily Intel/` (pruned by `/clean daily-intel`), never a Research note: the paper trail starts when a recommended `/transcript` runs.

**Division of labour vs `/event-sweep`** (keep these from drifting into each other): `/event-sweep` is the scheduled weekly surveillance of ALL event types at fixed cadence; `/earnings-sweep` is on-demand, earnings-only, takes an arbitrary window (a fortnight or a whole season), adds the **coverage dedupe** (which reporters already have vault research) and the **ranked deep-read queue**. During earnings season the weekly sweep says "these reported"; this skill says "here is the order in which to actually read them, and which ones you already covered".

## Arguments

- `/earnings-sweep` — window = last 14 days
- `/earnings-sweep [N]` — window = last N days (clamp 1-120; a season is ~90)

## Step 0: Pre-flight

1. **Lock**: `vault-wide` per `_shared/preflight.md` Procedure 1, timeout 10 min.
2. **Rename-marker**: glob `.rename_incomplete.*` — warn-only (no thesis edits in this skill).
3. **Quartr probe** (hard): per `_shared/quartr.md` §1 load `list_events,get_event_summary,read_transcript`. Unavailable → abort (no fallback source for summaries).
4. **Universe**: read `.data/quartr_watchlist.json` → `watchlistId` + members. Missing → recompute active set from thesis frontmatter (`grep -l '^status: active' Theses/*.md`), resolve via `.data/quartr_ids.json`, and emit `ℹ️ watchlist state missing — run /event-sweep --setup to persist; proceeding from thesis frontmatter` (per-company `list_events` fan-out in that degraded case, capped at the active count).
5. **Mental models (light tier)**: `[[Generalist - Overview]]` only — triage flags follow the READING PROTOCOL (touches are hypotheses; "confirms"/"fires" language banned in the digest).

## Step 1: Find the reporters

```
mcp__quartr__list_events {watchlistId, startDate: TODAY-N, endDate: TOMORROW, expand: ["transcript"], limit: 200, order: "desc"}
```

Filter to `parentEventType: "earnings_call"` (covers `q_1`…`q_4`, `h_1`/`h_2`). Partition: transcript-bearing (summary queue) vs reported-no-transcript-yet (list with `transcript pending — re-run in a few days` tag). `limit` hit → page by date and warn on truncation, never silently drop reporters.

## Step 2: Coverage dedupe (before spending a single summary call)

Per reporter, check whether the vault already ingested this print: glob `Research/*[TICKER]*` for notes dated on/after the event date with `source_type: earnings` or `transcript_quarter` matching the event's quarter, and grep the thesis `## Log` for a `Transcript ingested: [QN-YYYY]` entry. Already covered → the reporter appears in the digest under **Already ingested** with its note wikilink and drops out of the queue. This is the anti-duplicate-work layer: a season-length window re-run must not recommend re-reading what `/transcript` already processed.

## Step 3: Summaries + cross-reference (uncovered reporters only)

Per uncovered reporter:

1. `get_event_summary {eventId}` — render at **full detail** into the digest (every substantive bullet; only legal boilerplate cut — same contract as `/event-sweep` Step 3). Null summary + transcript available → `read_transcript {section: "qna"}` fallback capped at **3 per run**; beyond the cap, tag `summary pending — deep-read directly`.
2. Targeted section reads of the thesis: `## Conviction Triggers` + `## Outstanding Questions` (+ `## Key Metrics` table row for the guidance comparison). Flag every summary bullet that bears on a trigger variable, an open question, or moves a guided figure the thesis quotes. Record direction it *appears* to point + the deep link.

## Step 4: Rank the deep-read queue

Score per reporter (transparent, mechanical): **+3 per trigger-variable touch** · **+2 per Outstanding-Question touch** · **+1 for a guidance change vs what the thesis carries** · **+1 if `conviction: high`** · **−1 if the summary is pure in-line-quarter with no framing change**. Sort descending; ties break by conviction then market-cap-agnostic recency. The queue is a recommendation list of `/transcript TICKER` commands in order — the user (or a later session) executes; this skill never runs them.

## Step 5: Write the digest

`Daily Intel/YYYY-MM-DD - Earnings Sweep.md` — frontmatter `date`, `tags: [meta, daily-intel, earnings-sweep]`, `window: <start>..<end>`; no `publish:`. Structure:

```markdown
# Earnings Sweep — [window]

[stats: M active names · R reported in window · C already ingested · U triaged · Q queued for deep reads]

## Deep-read queue (ranked)
[1. /transcript TICKER — score N — one-line why (the strongest touch) · event link]

## Trigger/question touches
[table: TICKER · summary bullet · trigger/question touched · apparent direction · deep link]

## By reporter (full summaries)
### TICKER — QN FYYY (date) — [event URL]
[full summary per Step 3 · guidance-vs-thesis note · → queue position or "no thesis touch — skim only"]

## Already ingested
[TICKER · quarter · [[existing research note]]]

## Pending transcripts
[TICKER · reported date · re-run hint]
```

**No thesis writes, no Log entries, no `_hot.md`.** Summaries are pointers (contract §6): figures reach theses only through `/transcript` or filings.

## Step 6: Release lock + report

Stats line, top 3 of the queue with their one-line whys, digest wikilink.

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **Universe is active theses, not holdings.** The Live Portfolio table is a subset of the book's attention; a thesis being researched deserves earnings triage before it is owned.
2. **Dedupe before spend.** Step 2 runs before any summary call — a 90-day re-run over a covered season should cost near zero and recommend nothing already done.
3. **Flag, never conclude; summaries are pointers.** Same discipline as `/event-sweep`; the ranked queue is the only opinion this skill emits, and it is an attention ranking, not a verdict.
4. **Bounded cost.** One events query + one summary per uncovered reporter + ≤3 qna fallbacks. Season-length windows are bounded by reality (~44 names × ≤2 prints an actual quarter-window contains).
