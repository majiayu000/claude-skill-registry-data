---
name: vabene-discovery-synthesis
description: Two-phase JTBD synthesis (AI draft + human refinement) over interview transcripts. Per-transcript extracts Forces of Progress and verbatim quotes; weekly aggregate produces candidate opportunities for the Opportunity Solution Tree. Never modifies source transcripts.
version: "0.1.0"
author: ben
requires:
  tools:
    - bash
    - telegram
triggers:
  - "synthesize interviews"
  - "discovery synth"
  - "process transcripts"
  - "weekly opportunities"
  - "weekly opportunities --include-unreviewed"
  - "synth status"
---

# VaBene Discovery Synthesis

## Purpose

Turn raw customer interview transcripts into structured JTBD insights via a draft-then-refine loop. Per-transcript extraction surfaces the Forces of Progress (Push / Pull / Anxiety / Habit) plus verbatim quotes; a weekly aggregate pass surfaces candidate opportunities for the Opportunity Solution Tree.

The bottleneck this skill is built around is well-documented: teams complete JTBD interviews, the recordings sit in a shared drive, and the insights never make it into a product decision. AI draft + human refinement beats either alone — Ben catches things the model misses (and vice versa), so this skill never auto-commits a draft without making it explicit that the entry was AI-only.

**Hard rules:**

- This skill NEVER modifies or deletes source transcripts. Read-only on the input directory.
- Verbatim quotes are validated against the source before commit (substring match after normalization). Quotes that don't match are dropped, not silently kept.
- Auto-committed (un-refined) entries always carry a permanent `synthesis_status: "committed-unreviewed"` audit flag. The weekly aggregate excludes them by default.

---

## State machine

Each transcript moves through these states:

```
new                       <id>.md or <id>.txt appears in transcripts/
  ↓ (synthesize run)
drafted                   AI produces <id>.draft.md + Telegram "draft ready" msg
  ↓ (Ben writes <id>.refined.md)            ↓ (stale-after threshold elapses)
refined                                    committed-unreviewed
(canonical entry → MEMORY.md)              (AI version → MEMORY.md, audit-flagged)
```

The `refined` and `committed-unreviewed` states are terminal. State is encoded by which files exist in `transcripts/` and which `synthesis_status` is on the latest MEMORY.md entry for the transcript.

Default stale-after = 168h (7d). Override via `SYNTH_STALE_AFTER_HOURS` env var or `--simulate-stale-after <hours>` flag (verification uses `0` to test the auto-commit path on day 1).

---

## Input directory and filename convention

- Watched directory: `~/.openclaw/agents/main/transcripts/`
- Source files: `*.md` or `*.txt` (excludes `*.draft.md` and `*.refined.md`)
- Recommended filename convention: `YYYY-MM-DD-<participant-handle>.md` (e.g., `2026-04-26-anna-r.md`). The `transcript_id` is the basename without the extension.
- Recommended source: Otter or Granola export to Markdown, drop the file into the watched directory. Both produce clean Markdown with reasonable speaker labels and timestamps.

If a filename collides with an already-processed transcript (same `transcript_id`), the skill skips it and logs a `synthesis-warn` entry. Rename and re-drop.

---

## Per-transcript extraction

For each new transcript, the skill produces a draft containing:

### Switching trigger

The single moment or event that started the search ("we'd been talking about it for months, but the day my sister got engaged I knew I had to figure something out").

### Forces of Progress (Bob Moesta / Chris Spiek)

Four categorized lists of phrases / paraphrased situations:

- **Push** — what's wrong with the current situation
- **Pull** — what's appealing about the new solution
- **Anxiety** — fears or worries about switching to the new solution
- **Habit** — inertia keeping them in the current situation

A switch happens only when Push + Pull > Anxiety + Habit. The model should populate all four buckets even when sparse — a missing bucket is itself a signal.

### Workarounds

What they tried before this purchase. Group chat, spreadsheet, Partiful, hiring a planner, designating a friend, etc.

### Decision criteria

What they explicitly said mattered when choosing. ("Had to be in the city," "couldn't be more than $100/person," "needed to handle bookings, not just polls.")

### Pain dollar value

Where quantified, capture the dollar or hours figure they cite ("we lost the deposit on the Tahoe house — $1,200"). Null if not quantified.

### Verbatim quotes

Exact phrases worth keeping for the OST and downstream copy work. Each quote must validate against the source per the rule below.

### Job statement candidate

Single sentence: `When ___, I want ___, so I can ___`.

---

## Verbatim quote validation

Before any quote is written to MEMORY.md, the skill runs this check:

1. **Normalize the source transcript**:
   - Strip bracket annotations matching `\[[^\]]+\]` (e.g. `[laughs]`, `[inaudible]`, `[crosstalk]`)
   - Strip parenthetical interjections of the same shape: `\([^\)]+\)` when ≤ 20 chars (avoids stripping content)
   - Collapse whitespace runs to single space
   - Lowercase
2. **Normalize the quote candidate** identically.
3. **Exact substring match** → label `quote_match: "exact"`.
4. **Fall back** to fuzzy match (Levenshtein ratio ≥ 0.85) → label `quote_match: "fuzzy"`. Store both the AI-asserted quote and the closest matched substring from the transcript so Ben can spot-check during refinement.
5. **No match below 0.85** → drop the quote, append `{ts, scan: "synthesis-warn", transcript_id, dropped_quote, reason: "no_substring_match"}` to MEMORY.md.

This rule applies in both the `drafted → refined` and `drafted → committed-unreviewed` paths. A refined quote that no longer matches the source is also dropped.

---

## Aggregate pass (weekly)

Runs Sundays 10:00 PT (cron creation deferred — see "Cron Setup" below).

**Default behavior — excludes `committed-unreviewed` entries.** Without this, two weeks of vacation = AI-only synthesis silently shapes the OST. Override via trigger `weekly opportunities --include-unreviewed`.

For each candidate opportunity, the aggregate produces:

- The unmet-need statement in customer language
- Supporting verbatims — minimum 3 transcripts; AI must include the raw quotes, not paraphrase them
- Frequency — distinct transcripts citing this in the last 30 days
- Contradictions / disconfirming quotes if any
- First-seen / last-seen timestamps

**Aggregate Telegram message** must always state inclusion / exclusion:

```
🧪 Weekly synth — week of 2026-04-26
  Transcripts in window: 5 (2 excluded as unreviewed; run `weekly opportunities --include-unreviewed` to include).
  Candidate opportunities surfaced: 3
  See {baseDir}/MEMORY.md scan="discovery-opportunities" for full entries.
```

When the window is empty:

```
🧪 Weekly synth — week of 2026-04-26
  No new transcripts processed this week.
```

(Always send a heartbeat; silent runs train the human to assume the cron is broken.)

---

## MEMORY.md schemas (pinned at v0.1)

### Per-transcript entry

Written on commit (either path):

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T10:00:00-07:00","scan":"discovery-synthesis","transcript_id":"2026-04-26-anna-r","synthesis_status":"refined","forces":{"push":["..."],"pull":["..."],"anxiety":["..."],"habit":["..."]},"workarounds":["group chat","Partiful"],"decision_criteria":["had to be in SF","under $100/pp"],"pain_dollar_value":"$1200 lost deposit","quotes":[{"text":"the group chat just dies","ts_in_recording":"00:14:22","quote_match":"exact"}],"job_statement_candidate":"When I'm planning my friend's milestone birthday, I want a single tool that holds options and votes, so I can stop being the bottleneck."}
```

### Per-opportunity entry (aggregate)

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T10:00:00-07:00","scan":"discovery-opportunities","week_of":"2026-04-26","opportunity_id":"a3f1b2c4d5e6","statement":"Coordinating activity choices across a group is the actual bottleneck, not picking the activity","frequency":4,"first_seen":"2026-04-12T14:00:00-07:00","last_seen":"2026-04-25T11:30:00-07:00","supporting_quotes":[{"transcript_id":"2026-04-26-anna-r","quote":"the group chat just dies","ts_in_recording":"00:14:22","synthesis_status":"refined","quote_match":"exact"}],"contradictions":[],"derived_from_unreviewed":false,"unreviewed_count":0}
```

### Warn entry (drop log)

```jsonl
{"schema_version":"0.1","ts":"2026-04-26T10:00:00-07:00","scan":"synthesis-warn","transcript_id":"2026-04-26-anna-r","dropped_quote":"the group chat absolutely melts down","reason":"no_substring_match"}
```

### Schema-version contract

`schema_version: "0.1"` is on every entry written by this skill. v0.2 readers can branch on this without ambiguity. The imminent-interviews choice means a v0.2 rework is expected after the first 2–3 real transcripts; that's accepted.

---

## Workflow (per-run)

### Step 1 — Discover new transcripts

```bash
TRANSCRIPTS_DIR="$HOME/.openclaw/agents/main/transcripts"
[[ -d "$TRANSCRIPTS_DIR" ]] || { echo "ERROR: transcripts dir missing at $TRANSCRIPTS_DIR" >&2; exit 1; }

# Source files only — exclude drafts and refinements
find "$TRANSCRIPTS_DIR" -maxdepth 1 -type f \
  \( -name '*.md' -o -name '*.txt' \) \
  -not -name '*.draft.md' \
  -not -name '*.refined.md'
```

For each file, derive `transcript_id = basename(file) without extension`. Cross-check against MEMORY.md for an existing entry with that `transcript_id`.

### Step 2 — Branch by state

For each `transcript_id`:

- **No prior entry, no `<id>.draft.md`** → produce draft. Save to `<TRANSCRIPTS_DIR>/<id>.draft.md`. Telegram "draft ready" message. Do not commit to MEMORY.md yet.
- **Draft exists, refined doesn't, age < stale-after** → no-op (waiting on Ben).
- **Draft exists, refined doesn't, age ≥ stale-after** → commit AI draft as `synthesis_status: "committed-unreviewed"` to MEMORY.md.
- **Draft exists, refined exists** → validate refined quotes per the verbatim rule, commit refined version to MEMORY.md as `synthesis_status: "refined"`.
- **Already committed in MEMORY.md** → skip (don't reprocess).

### Step 3 — Aggregate (only when triggered)

When trigger is `weekly opportunities` (or its `--include-unreviewed` variant):

1. Pull all `discovery-synthesis` MEMORY.md entries from the last 30d, applying the unreviewed filter.
2. Cluster by job-statement-candidate similarity (model decides; document threshold in next-version README).
3. Emit one `discovery-opportunities` entry per cluster meeting `frequency >= 3`.
4. Send the heartbeat Telegram message.

### Step 4 — Status check (manual trigger only)

`synth status` trigger: read MEMORY.md, count by `synthesis_status` for the last 30d, list any drafts that have been pending > stale-after / 2 (early warning). Send to Telegram.

---

## Telegram message formats

### Draft-ready

```
🧠 Discovery synth — draft ready
Transcript: 2026-04-26-anna-r
Forces: P=4, P=2, A=3, H=2 (Push=4, Pull=2, Anxiety=3, Habit=2)
Quotes captured: 6 (5 exact, 1 fuzzy)
Job statement: "When I'm planning my friend's milestone birthday, I want a single tool that holds options and votes, so I can stop being the bottleneck."

Edit at:
  ~/.openclaw/agents/main/transcripts/2026-04-26-anna-r.draft.md

Save your edits as:
  ~/.openclaw/agents/main/transcripts/2026-04-26-anna-r.refined.md

Auto-commits as 'committed-unreviewed' in 7 days if not refined.
```

### Refined commit

```
✅ Discovery synth — refined
Transcript: 2026-04-26-anna-r
Committed to MEMORY.md (synthesis_status: refined).
```

### Auto-commit-unreviewed

```
⚠️ Discovery synth — auto-committed unreviewed
Transcript: 2026-04-26-anna-r (no refinement after 7 days)
Committed to MEMORY.md with permanent audit flag (synthesis_status: committed-unreviewed).
Excluded from default weekly aggregate. Re-review at any time by saving a .refined.md and re-running synth.
```

### Aggregate (see "Aggregate pass" above)

---

## Cron Setup

Deferred. Wire only after ≥ 3 successful manual runs per state-machine path (drafted, refined commit, unreviewed commit, aggregate include-default, aggregate include-unreviewed). For reference / future creation:

```bash
# Per-run synthesis (drafts + refined commits + auto-commit watchdog) — every hour during waking hours
openclaw cron add \
  --name "VaBene Discovery Synthesis" \
  --cron "0 8-22 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-discovery-synthesis skill. Process any new transcripts, watchdog drafts past the stale-after window. Never modify source transcripts." \
  --model claude-sonnet-4-6 \
  --to <TELEGRAM_CHAT_ID> \
  --announce \
  --channel telegram

# Weekly aggregate — Sunday 10am PT
openclaw cron add \
  --name "VaBene Weekly Opportunities" \
  --cron "0 10 * * 0" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the vabene-discovery-synthesis skill with trigger 'weekly opportunities'. Aggregate over last 30d, emit candidate opportunities; exclude committed-unreviewed by default." \
  --model claude-sonnet-4-6 \
  --to <TELEGRAM_CHAT_ID> \
  --announce \
  --channel telegram
```

Sonnet (not Haiku) because synthesis quality matters more than throughput.

---

## Manual Telegram triggers

| Command | What it does |
|---|---|
| `synthesize interviews` | Full per-run pass: draft new, commit refined, watchdog stale drafts |
| `discovery synth` | Alias |
| `process transcripts` | Alias |
| `weekly opportunities` | Aggregate pass, default (excludes committed-unreviewed) |
| `weekly opportunities --include-unreviewed` | Aggregate pass, includes unreviewed entries with `derived_from_unreviewed: true` flag |
| `synth status` | Counts by synthesis_status over last 30d + early-warning list of drafts approaching stale-after |

---

## Tuning levers (in priority order)

When iterating on this skill, tune in this order:

1. **`SYNTH_STALE_AFTER_HOURS`** — default 168 (7d). Lower if Ben wants faster auto-commits (but: more unreviewed entries shape the aggregate). Raise if Ben wants more leeway.
2. **Fuzzy match threshold** — default 0.85 Levenshtein ratio. Tighten (0.90) if too many paraphrases sneak through; loosen (0.80) if too many real quotes get dropped.
3. **Aggregate `frequency` floor** — default 3 transcripts. Lower to 2 once the corpus is small (first 5 interviews); raise to 4–5 once volume permits.
4. **Cluster similarity threshold** in the aggregate — last-resort tuning. The whole skill schema is v0.1 — expect a v0.2 rewrite after the first 2–3 real transcripts redefine what "good" extraction looks like for SF self-host celebrants.

Document any tuning change in MEMORY.md (a `synthesis-warn` entry is fine for ad-hoc notes) and in this skill's README change log. Weights are easy to fiddle and hard to reason about retroactively.

---

## Relationship to other skills

- **`vabene-interview-finder`** — finds Reddit users worth interviewing. Upstream of this skill.
- **`vabene-interview-recruiter`** — drafts comment-first / DM outreach for finder leads, tracks state through scheduled / interviewed / gift-sent. The `interviewed` outcome on a recruiter entry is the upstream cue for a transcript to land in the watched directory.
- **`vabene-reddit-monitor`** — separate concern (acquisition leads vs. research candidates). Schemas overlap on `lead_id` but transcripts feed only from interviewed candidates.

When a recruiter entry transitions to `outcome: "interviewed"`, the human's responsibility is to ensure the transcript actually arrives in `~/.openclaw/agents/main/transcripts/` with the correct filename. Nothing in this skill auto-fetches; that's by design (no recording-tool integration in v0.1).

---

## Security

- Read-only on source transcripts. The skill writes only to `*.draft.md` siblings and to MEMORY.md.
- Transcripts contain PII (names, locations, employer references, possibly phone numbers in the wild). MEMORY.md entries strip identifying narrative but include verbatim quotes — treat MEMORY.md as PII-bearing per the existing `memory/README.md` policy.
- All Telegram messages route through the configured bot.
- No external recording-tool API calls. Otter / Granola export is a manual step.
