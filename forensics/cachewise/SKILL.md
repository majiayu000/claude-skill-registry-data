---
name: cachewise
description: >-
  Prompt-cache economics forensics — why your Claude Code tokens burn so fast,
  with the numbers to prove it. Parses local ~/.claude transcripts (0 tokens,
  a bundled Python script does the counting) and attributes every cache-miss
  rebuild to a cause — idle gaps past the 5-min TTL, mid-session model/effort
  switches, prefix churn (MCP tool-lists, edited CLAUDE.md, dynamic content),
  and cold re-boots of a session you could have resumed — each priced in real
  USD, then prescribes the fixes ranked by dollars saved. Tracks before/after
  in out/cachewise/tracker.md so the next run measures whether a fix worked.
  Use when the user asks why they hit usage limits so fast, wants their cache
  hit rate or token spend analyzed, or where their tokens are going — e.g.
  "/cachewise", "analyze my prompt cache", "what's burning my tokens". For
  recurring behavior mistakes use tune; for today's schedule use daybrief.
---

# cachewise — where your cache dollars leak

`/cachewise` — analyze the last 30 days across every project
`/cachewise --days N` — widen or narrow the window

Answer one question: **which habits are rebuilding cache you already paid
for, and what would each fix save?** Prompt caching makes a cache read cost
0.1× and a rebuild cost 1.25× — so every avoidable miss is a ~12× markup on
that slice of context. ccusage and `/cost` count the tokens; cachewise says
*why* the expensive ones happened and *what to change*. The evidence is on
disk — the transcripts recorded every cache write; this skill attributes
them so the numbers, not folklore, drive the fix.

## Step 0 — Run the analyzer

The counting is deterministic and token-free — **never read the raw JSONL
yourself** (parsing thousands of transcript lines with the model is the
exact token burn this skill exists to stop). Run the bundled script:

```bash
python3 .claude/skills/cachewise/scripts/analyze.py --days 30
```

It scans `~/.claude/projects/**/*.jsonl` and prints one JSON document.
No `~/.claude` data (fresh machine, or none in the window) → the script
returns zero turns; say so plainly and stop, there's nothing to diagnose.

Before trusting the numbers, glance at `flags`:
- `pricing_fallback_models` — models priced at the Sonnet-4.x fallback
  because their id wasn't in the table (USD is approximate for those).
- `missing_timestamp_turns` / `malformed_lines` — data the parser skipped;
  large counts mean the picture is partial.

## Step 1 — Read the attribution

The report splits cost three ways — keep them distinct, they prescribe
differently:

- **`miss_attribution`** — cache *rebuilds*, the avoidable core. Each cause
  carries tokens + USD (the money a cache hit would have saved):
  `idle_gap`, `model_switch`, `write_churn`, and `unattributed` (cause
  undeterminable, usually missing timestamps). The USD is *avoidable* spend,
  not total spend.
- **`context_tax`** — not a miss: the standing read-cost of sessions that
  carry far more prefix per turn than your same-model norm. Sprawl, priced
  as excess reads.
- **`dead_session`** — **low-confidence** heuristic: cold re-boots of a
  same-project session soon after another ended. Report it as a lead, not a
  fact — say "possibly" and cite the count.

`totals.usd.total` is the whole API-equivalent spend in the window;
`miss_attribution.total_usd` is the slice that better habits recover.

## Step 2 — Render the report

Present, in chat, most-expensive-first:

1. **Headline** — window, total API-equivalent spend, cache hit rate, and
   the avoidable miss total in USD (e.g. "94% hit rate; **$1,534 of $5,944
   was avoidable cache rebuilds**").
2. **Prescriptions** — walk `prescriptions` in order (already ranked by
   USD). For each: the cause, its dollar cost, the one-line fix from the
   script, and the top offending sessions/projects from `top_offenders` so
   the user sees *where* it happened. Mark `dead_session` and `context_tax`
   as the softer, lower-confidence lines they are.
3. **Caveats** — surface any `flags` that make the numbers approximate, and
   the standing note: for subscription (Pro/Max) users these are
   API-equivalent *values*, not a bill — the ratios still hold, the absolute
   dollars are a yardstick.

Keep it honest: if the hit rate is already high and avoidable spend is a
rounding error, say the setup is healthy rather than manufacturing a
problem.

## Step 3 — Track before/after

Memory is what turns a one-off report into a measurable fix. Append a run
to `out/cachewise/tracker.md` (create it if absent; date via `date +%F`):

```markdown
## <date> · window <N>d
- Spend: $<total> · hit rate <pct>% · avoidable $<miss_total>
- By cause: idle_gap $X · write_churn $Y · model_switch $Z · dead_session $W (low-conf) · context_tax $V
- Prescribed: <the top 1–3 fixes handed to the user this run>
- Since last run: <hit-rate and avoidable-$ delta vs the previous entry, or "baseline">
```

On every run after the first, read the previous entry and lead the report
with the delta — did avoidable spend fall after last run's fix, or not?
A prescription whose number didn't move next run is one to retire or
rethink, not repeat.

## Guardrails

- **The script counts; the model interprets.** Reading raw transcripts into
  context to tally tokens is the waste this skill diagnoses — don't commit
  it. If the script can't answer something, extend the script, not the habit.
- **Avoidable, not total.** Miss USD is what better habits recover, never
  the whole bill — conflating them scares the user off legitimate spend.
- **Confidence is labeled, not implied.** `dead_session` and `context_tax`
  are heuristics; present them as leads. Never state a cause the transcript
  can't support — `unattributed` exists so misses aren't force-fit.
- **Prices carry a date.** The USD table is stamped `pricing_asof`; when it
  ages, reverify against the official pricing page rather than trusting it.
- **Privacy is structural.** Transcripts stay local; only aggregate numbers
  reach the report. `out/cachewise/` holds no prompt content.
