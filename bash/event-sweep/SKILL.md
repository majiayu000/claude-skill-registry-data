---
name: event-sweep
description: Weekly sweep of ALL transcript-bearing spoken events (earnings calls, conference firesides, CMDs, investor days, AGMs, investor updates) for every active thesis, via the Quartr watchlist. Produces a triage digest in Daily Intel/ flagging thesis-touching mentions and recommending deep reads. Use when user says "event sweep", "what did my companies say this week", "conference sweep", or on the weekly schedule. Also `--setup` (build/rebuild the Quartr watchlist from active theses) and `[N]` (window override in days, default 8).
model: opus
effort: high
allowed-tools: Read Grep Glob Write Edit ToolSearch mcp__quartr Bash(date * jq * ls * cat * grep * mkdir * printf * wc * find *)
---

Surveillance layer over the book's spoken record. Every week: one watchlist-scoped Quartr events query → event summaries for everything with a transcript → cross-reference against each thesis's Conviction Triggers and Outstanding Questions → one digest note in `Daily Intel/`. The digest is a **scanning surface** (like the n8n news briefs — pruned by `/clean daily-intel` after 90 days), NOT a Research note: it flags and points, it never concludes. Deep analysis stays with `/transcript TICKER` (earnings) and `/transcript TICKER --event <id>` (non-earnings), which the digest recommends per hit.

Rationale (G-2): conference firesides and mid-quarter investor updates are the highest signal-per-word spoken sources — no scripted safe-harbour remarks, sell-side hosts ask what the market is debating, and they land in the information vacuum between prints. FMP sees none of them; Quartr transcribes them. Nobody reads them systematically; this skill makes the vault the reader of record for every active name.

## Arguments

- *(none)* — sweep the default window (last 8 days) + upcoming 7-day preview
- `[N]` — window override in days (e.g. `/event-sweep 14` after a holiday gap)
- `--setup` — build or rebuild the Quartr watchlist from active theses; run once initially and whenever the digest's drift check reports a failure

## Step 0: Pre-flight

1. **Lock**: `vault-wide` scope per `_shared/preflight.md` Procedure 1, timeout 10 min. (Writes one new Daily Intel file + `.data` state; reads many theses.)
2. **Rename-marker**: glob `.rename_incomplete.*` — warn-only (this skill edits no thesis; a mid-rename ticker's digest section may carry the old name for one week).
3. **Quartr probe** (hard): per `_shared/quartr.md` §1 load `search_companies,list_events,get_event_summary,read_transcript,create_watchlist,add_to_watchlist,remove_from_watchlist,list_watchlists`. Unavailable → abort: `❌ Quartr MCP unavailable — /event-sweep has no fallback source. Retry when the server is up.` (No FMP fallback exists for non-earnings events; a degraded sweep would silently miss exactly the events this skill exists to catch.)
4. **Mental-models load (light tier)**: read `[[Generalist - Overview]]` only — the digest's flag-language must follow the READING PROTOCOL (a mention that appears to confirm a trigger is a hypothesis to deep-read, never a confirmation). Skip industry/lens files: this is triage, not analysis.

## Step 1: Watchlist state + membership drift

State file: `.data/quartr_watchlist.json` — `{"watchlistId": N, "name": "Vault Active", "members": {"TICKER": companyId, ...}, "misses": ["TICKER: reason"], "last_synced": "YYYY-MM-DD"}`.

- **Missing state file** → run the `--setup` path below, then continue into the sweep.
- **Drift check (every run)**: recompute the active set — `grep -l '^status: active' Theses/*.md` → vault tickers from filenames. Diff against `members`:
  - New active thesis → resolve companyId per `_shared/quartr.md` §3 (`quartr_id:` frontmatter → `.data/quartr_ids.json` → verified `search_companies`; unresolvable → append to `misses`, never guess) → `add_to_watchlist`.
  - Ticker no longer active (closed / moved to monitoring) → `remove_from_watchlist`.
  - Update state file + `last_synced`. Report adds/removes in the digest header. This makes `/status` transitions self-healing — no manual watchlist maintenance.

### `--setup` path

1. Active set from thesis frontmatter (as above). 2. Resolve every ticker to a companyId (cache-first; batch the unresolved through verified `search_companies`; record misses — private names like SPCX are expected misses). 3. Reuse an existing "Vault Active" watchlist if `list_watchlists` finds one (empty it via remove/add reconciliation rather than deleting — deletion churns any Quartr-side alert scoped to it); else `create_watchlist {name: "Vault Active"}`. 4. `add_to_watchlist` in batches of ≤50. 5. Write state file. 6. Report: member count, misses with reasons.

## Step 2: Event queries (two windows, one watchlist)

```
mcp__quartr__list_events {watchlistId, startDate: TODAY-N(-8d default), endDate: TOMORROW, expand: ["transcript"], limit: 200, order: "desc"}   # the sweep window
mcp__quartr__list_events {watchlistId, startDate: TOMORROW, endDate: TODAY+7d, expand: [], limit: 100, order: "asc"}                              # upcoming preview
```

Partition the sweep window by `transcript.available`:
- **Transcript-bearing** (any eventType — earnings, conference, fireside_chat, CMD, investor_day, analyst_day, AGM, guidance, investor_update, update_and_briefing): the summary queue.
- **Appearance stubs** (event happened, no transcript): list-only — the appearance itself is signal; webcast may exist on the IR page.

`limit: 200` covers a normal week (~44 names × 0-3 events). If the response hits the limit, page by tightening `endDate` and re-querying — never silently truncate (report `⚠️ event window truncated` if a full week genuinely exceeds paging effort).

## Step 3: Summaries (the "everything discussed" layer — FULL detail, 2026-09-09 depth upgrade)

Per transcript-bearing event: `mcp__quartr__get_event_summary {eventId}`.

- Summary present → render it into the digest (Step 5) **at full detail, not condensed**: keep every substantive bullet across every section (executive summary, financials, guidance, segments, ratios, significant events, capital allocation, market conditions). Reformat to vault style; strip `<document-source>` markers; keep the event URL as the section link. The ONLY cuts allowed are pure legal boilerplate ("forward-looking statements are subject to risks…", generic non-GAAP reconciliation notes) and exact duplicate bullets — a bullet with a number, name, product, mechanism, or competitive claim is never cut. The digest is the user's substitute for attending the event; under-summarising defeats it.
- Summary `null` + transcript available → fallback `read_transcript {eventId, section: "qna"}` and extract the load-bearing exchanges (Step 3.5 format); events beyond the Step 3.5 cap are listed as `transcript available, summary pending — deep-read: /transcript TICKER --event <id>`.
- Quartr summaries are machine-generated: treat as **pointers, not evidence**. Any figure destined for a thesis or Research note must come from a deep read (`/transcript`) or the underlying document, never quoted from the digest.

## Step 3.5: Q&A extraction for thesis-touching events

For every event that fires a Step 4 flag (cap: **6 qna reads per run**, priority by flag strength): `read_transcript {eventId, section: "qna"}` — large results persist to a file; jq-extract `(speakerName, speakerRole, text, url)` per paragraph from disk and select the **4-8 sharpest exchanges**: trigger/question-relevant topics first, then any exchange where management gave a number, named a customer/competitor, described a mechanism, or visibly deflected. Render each as a compact Q→A block with the analyst/host question (paraphrase allowed), the substantive core of management's answer (tight quote or close paraphrase), and the paragraph's timestamped deep-link on the speaker attribution. Conference firesides are often 100% Q&A — if `qna` returns empty for a fireside, read `section: "full"` instead and treat the whole event as Q&A. This layer is the sweep's real depth: summaries carry the prepared narrative; the exchanges carry what the market actually probed and how management handled it.

## Step 4: Thesis cross-reference (flag, never conclude)

Per company with ≥1 summarised event: extract the thesis's `## Conviction Triggers` and `## Outstanding Questions` sections (targeted section read, not a full-file read). Flag any summary bullet that bears on a trigger's named variable or an open question. Each flag records: the bullet, the trigger/question text it touches, direction it *appears* to point, and the deep-read command. READING PROTOCOL applies: flags are hypotheses; wording like "confirms"/"fires" is banned in the digest — use "touches", "bears on", "warrants deep read".

## Step 5: Write the digest

File: `Daily Intel/YYYY-MM-DD - Event Sweep.md` (matches the Daily Intel naming pattern; pruned by `/clean daily-intel` >90d). Frontmatter: `date`, `tags: [meta, daily-intel, event-sweep]`, `window: YYYY-MM-DD..YYYY-MM-DD`. NO `publish:` (scanning surface, never website-synced). Structure:

```markdown
# Event Sweep — week to YYYY-MM-DD

[1-line stats: N events across M companies · X transcript-bearing · Y stubs · drift: +A/-B]

## Thesis-touching highlights
[Ranked list — the flags from Step 4, each: TICKER · event · the touching bullet · trigger/question touched · → deep read command]

## By company
### TICKER — [Event title] ([type], YYYY-MM-DD) — [event URL]
[FULL summary per Step 3 — every substantive bullet, organised under the summary's own sub-themes (bold lead-ins or #### sub-heads for long earnings events). → suggested action: /transcript TICKER (earnings) or /transcript TICKER --event <id> (non-earnings), only where warranted]

#### Q&A highlights (flagged events only, per Step 3.5)
[4-8 Q→A blocks with timestamped deep-links]

## Appearances without transcripts
[TICKER · event · date — check IR webcast if the appearance matters]

## Upcoming week
[From the preview query: TICKER · event · date/time — earnings prints get a "queue /transcript" tag]

## Coverage gaps
[Watchlist misses + any truncation warnings]
```

**No thesis Log entries, no thesis edits, no `_hot.md` writes** — the digest is disposable triage. The paper trail starts when a recommended deep read runs.

## Step 6: Release lock + report

Standard release per preflight §1.7. Chat report: stats line, top 3 thesis-touching flags, digest wikilink, and the deep-read queue.

## Design constraints (xxx DO NOT VIOLATE xxx)

1. **Flag, never conclude.** The digest carries zero conviction language and never writes to a thesis. A sweep that "confirms" triggers unsupervised is an inside-view echo chamber running on a cron — the exact failure the READING PROTOCOL blocks.
2. **Summaries are pointers.** Machine summaries never become Evidence. Deep reads (`/transcript`) create the record; the digest only routes attention.
3. **Watchlist "Vault Active" is owned by this skill.** Other skills may READ it (`/catalyst` may use `list_events {watchlistId}` instead of per-ticker fan-out); only `/event-sweep` mutates membership, always from thesis `status:` — the vault is canonical, the watchlist is a mirror.
4. **Misses are visible.** Every unresolvable ticker appears in the digest's Coverage gaps every week until resolved (or given a `quartr_id:` override). Silent coverage holes in a surveillance tool are worse than no tool.
5. **Bounded cost, depth-weighted.** One events query + one summary per event + ≤6 qna reads (Step 3.5, flagged events only). Full-transcript bulk reads of unflagged events stay out of scope — that is what the recommended deep reads are for. The qna layer is the deliberate exception: flagged events earn their exchanges in the digest.
