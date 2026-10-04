---
name: selection-report
description: Write output/<slug>/_selection.json for a source — the shipped shorts (scores + rationale from segments.raw.json, linked to their delivered filename) ALONGSIDE the considered-not-shipped RLM candidate menu (candidates.hint.json, each marked picked/unused) and the topic list (topics.json). Deterministic, no Claude, idempotent, non-fatal. Runs once at end of run AND standalone over the whole output/ backlog. Answers "show me the other arguments alongside the shorts".
---

# selection-report

A read-only audit artifact: for each source, what got shipped, what was considered
and passed over, and why. Sources every field from `work/<id>/` — no Claude.

## Usage
```bash
selection-report.sh <work_dir> [output_root]   # one source -> output/<slug>/_selection.json
selection-report.sh --backlog [output_root]    # every work/<id> with a matching output/<slug>/
```
`output_root` defaults to `$OUTPUT_DIR` (`.env`) or `<repo>/output`.

## Inputs (all from `work/<id>/`, all optional → graceful empty sections)
- `ingest.json` — title/url/duration + the slug that names `output/<slug>/`.
- `segments.raw.json` — the produced shorts with scores + rationale (the SHIPPED set).
- `clip_NN.done.completion` — written by `start.sh` save-local; maps span N → the
  delivered filename (the title differs from `title_suggestion` because `generate-title`
  re-titles). Absent in the legacy `shorts.sh` path → `name: null`.
- `candidates.hint.json` — the rlm discovery menu (CONSIDERED set; absent on non-rlm
  short sources → empty).
- `topics.json` — the topic chapters.

## Output `output/<slug>/_selection.json`
```json
{
  "source_id": "...", "title": "...", "url": "...", "slug": "...", "duration_sec": 0,
  "shipped_count": 0, "considered_count": 0, "considered_picked": 0, "topics_count": 0,
  "shipped":   [ { "rank", "name", "delivered", "t0","t1","cuts", "hook_type",
                   "opening_line","title_suggestion","rationale","topic",
                   "overall_score","hook_score","context_score","structure_score",
                   "hook_payoff_coherence","payoff_offset_sec","replay_quotient",
                   "thread?","thread_kind?" } ],
  "considered":[ { "t0","t1","quote","why","confidence",
                   "picked","picked_by",            // picked = overlaps a shipped cut
                   "thread?","kind?","cuts?","bridge?" } ],
  "topics":    [ { "t0","t1","title","summary" } ]
}
```
A candidate is `picked: true` when its `[t0,t1]` overlaps any shipped span's cuts;
`picked_by` names the short it overlaps most.

## Where it runs
`start.sh` end-of-run (after `sources-ledger`, before `schedule-drip`) for the just-run
source; `shorts.sh` end-of-run; standalone `--backlog` to backfill existing output dirs.
Idempotent — rewritten each run.
