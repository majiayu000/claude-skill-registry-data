---
name: analytics-feedback
description: Close the learning loop from real YouTube performance. Reads the newest YouTube Studio "Table data.csv" export, attributes each video's views/CTR/retention to topic + named-entity tokens, and rewrites the AUTO-managed block of schedule-drip's topics.scorelist (GO winners / HOLD dead niches) plus appends proven-winner search queries to scout-sources' niches.txt. Deterministic, no Claude, idempotent (no-op unless the export's mtime changed). The analytics half of the autopilot loop — runs at the top of every autopilot tick so scout + schedule-drip always reflect what actually performed.
allowed-tools: Bash
user-invocable: true
---

# analytics-feedback

Turns channel analytics into pipeline behavior. YouTube Studio → Analytics → **Content** → Export → unzips to `~/Downloads/Content <range> <channel>/` with `Table data.csv` (per-video views, watch hours, CTR). This skill reads that export and re-derives which topics to chase and which to bury.

## Usage

```bash
analytics-feedback.sh                       # newest export under ~/Downloads/Content*C0BALT_CUT*/
analytics-feedback.sh "/path/Table data.csv"   # explicit file
analytics-feedback.sh --force               # re-learn even if the export's mtime is unchanged
```

Idempotent: records the consumed export's mtime in `work/_autopilot/analytics.csv.mtime` and no-ops on an unchanged export (so it's safe to call every autopilot tick). Drop a fresh export into `~/Downloads` and the next tick relearns.

## What it writes

1. **`.claude/skills/schedule-drip/topics.scorelist`** — preserves everything ABOVE the `# ==== AUTO (analytics-feedback) ...` sentinel (your hand-curated rules are never touched) and regenerates the block below it with data-derived `GO <pattern>` / `HOLD <pattern>` lines. Evidence (`n=`, `med=`, `ctr=`) is on `#` comment lines — never inline on a rule line, because `schedule.py` treats everything after the verdict as the regex.
2. **`.claude/skills/scout-sources/niches.txt`** — preserves your manual seed queries and appends a regenerated AUTO block of search queries built from the GO winners (e.g. a winning `black[ -]?hole` → `black hole physics explained`), so scout expands into proven niches. Additive only.
3. **`work/_autopilot/topic_scores.json`** — full per-token evidence (n, median/mean/min/max views, mean CTR, median retention, total watch hours, verdict, suppressed-alias flag, manual conflicts). The audit trail.

## Classification (env-tunable)

Per token (known entities from a lexicon + auto-discovered title tokens, deduped so `#blackhole` doesn't double-count `black[ -]?hole`):

- **GO** when `n ≥ AF_GO_MIN_N` (3) AND `median_views ≥ AF_GO_VIEWS` (600) AND `mean_ctr ≥ AF_GO_CTR` (5%). Median + the n≥3 floor reject a single viral fluke (a 2-video token with one 6-view dud can't earn GO).
- **HOLD** when `n ≥ AF_HOLD_MIN_N` (2) AND `median_views ≤ AF_HOLD_VIEWS` (60). Dead-is-dead needs less evidence than proven-winner.
- **neutral** otherwise (no line emitted; `schedule.py` defaults unmatched sources to HOLD anyway).

A `HOLD` always wins over a `GO` in `schedule.py`, so the data can demote a manual `GO` (surfaced as a conflict in the JSON) but a manual `HOLD` veto still sticks.

## Where it runs

- **autopilot tick** — first step of `autopilot.sh`, before scout, so discovery + staging always reflect the latest export.
- **standalone** — run it by hand after any fresh export to retune immediately.
