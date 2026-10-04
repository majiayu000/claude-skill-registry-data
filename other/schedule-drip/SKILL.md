---
name: schedule-drip
description: Deterministic greedy scheduler over the graded clips — the only skill that attacks the #1 unconfounded leak (the 7-day dark gap) and the 53-from-one-source feed-fatigue. STAGING-HANDOFF ONLY, no auto-upload (no API key in the stack): it copies finished clips into dated output/_toupload/<date>/ folders + writes metadata.txt (lowercased title + winning-topic hashtags). Reads every output/**/*.grade.json + a checked-in topics.scorelist (GO/HOLD) + an OPTIONAL output/upload-log.json. GOLD-first gate, rank by grade desc, GO clips fill days first / HOLD only backfills a day that would otherwise be dark, de-dupe near-identical clips (same source + high title-token overlap), enforce MAX_PER_SOURCE_PER_DAY=1 round-robin, drop anything already posted, and EMIT a gap_warnings entry for any dark day in the horizon. Idempotent (_toupload rebuilt deterministically), non-fatal (any error → exit 0). Runs end-of-run / standalone over output/.
allowed-tools: Bash
user-invocable: true
---

# schedule-drip

The selection suite's drip stage. The pipeline today is produce-only: it renders
clips and stops. The human picks ~19 by hand, dies 37% of the time on topic, and
the channel takes 7-day dark gaps while ~80 quality clips rot on disk. With no
evergreen tail (86-100% of a short's views land in days 1-3), **a dark day is
permanent lost reach** — the #1 unconfounded leak in the 28-day analytics.

`schedule-drip` is the deterministic greedy scheduler that fixes it. It consumes
`grade-clip`'s `grade.json` verdicts plus a checked-in topic scorelist and stages
a daily drip into `output/_toupload/<date>/`. **Staging-handoff only — it never
uploads** (there is no API key in the stack); a human posts from the dated
folders.

## Usage

```bash
schedule-drip.sh [output_dir=output]
```

## Inputs

- Every `output/**/*.grade.json` (skips `_preview` / `source` / `_toupload` /
  `_triage`). The locked schema lives in `SELECTION-SUITE-CONTRACT.md`.
- `topics.scorelist` (checked in here) — one rule per line, `<GO|HOLD> <regex>`,
  matched case-insensitively against `source-slug + title`. **HOLD is a denylist
  and WINS** over an incidental GO substring (e.g. "focus" inside a
  productivity-death source's "stay-focused"). Default when nothing matches:
  `HOLD` (conservative).
- OPTIONAL `output/upload-log.json` — a list, or `{uploaded|posted: [...]}`, of
  already-posted clip paths / basenames / titles. **Absence means "nothing posted
  yet" — never a crash.**
- "Today" comes from the system `date`.

## Algorithm (deterministic greedy)

1. **Gate (GOLD-first):** keep a clip only if `tier==GOLD` with no `hard_caps`, OR
   `grade>=GRADE_MIN_UPLOAD` with no `hard_caps`. A clip with any unfixed hard cap
   stays out of the drip until `fix-cold-open` repairs it.
2. **Drop posted:** anything matched in `upload-log.json`.
3. **Rank** by grade desc (then source, then path for stable ties).
4. **De-dupe near-identical:** same source + ≥0.7 title-token overlap → keep the
   higher grade, drop the rest (collapses the `clip` / `clip-1.25x` speed-up twins).
5. **Topic verdict:** GO vs HOLD from `topics.scorelist`.
6. **Place GO first** into the horizon, one day at a time, `POSTS_PER_DAY` per day,
   `MAX_PER_SOURCE_PER_DAY` round-robin across sources (the 53-from-one-source
   feed-fatigue fix — no day ever gets two clips from the same source).
7. **Backfill dark days with HOLD** clips only — a HOLD clip is never dripped ahead
   of a GO clip, only into a day that would otherwise be dark.
8. **`gap_warnings`** — any day still empty after backfill (the dark-gap alarm).

## Output

- `output/_toupload/<YYYY-MM-DD>/` per filled day: the staged clip (copy) +
  `metadata.txt` (lowercased title + `#`-hashtags from the matched GO rule and the
  source slug, plus `#shorts #fyp`).
- `output/_toupload/schedule.json` — `{generated, horizon_days, posts_per_day,
  max_per_source_per_day, days:{date→[clips]}, gap_warnings, backfilled, drops}`.
  `drops` records every `not_schedulable` / `already_posted` /
  `dedupe_near_identical` / `horizon_full` decision.

**Idempotent:** `_toupload` is rmtree'd and rebuilt every run — a re-run yields a
byte-identical plan and never duplicates staging. **Non-fatal:** any error exits 0
without staging.

## Knobs

| Env | Default | Meaning |
|---|---|---|
| `POSTS_PER_DAY` | 1 | clips staged per day |
| `MAX_PER_SOURCE_PER_DAY` | 1 | per-source round-robin cap (feed-fatigue fix) |
| `DRIP_HORIZON_DAYS` | 14 | days to plan ahead |
| `GRADE_MIN_UPLOAD` | 60 | shared with grade-clip; the schedulable grade floor |

## Why new

There is no selection / scheduling step at all. This is the only skill that
directly attacks the dark gap and the backlog rot — it turns "101 produced / 19
uploaded" into a multi-week daily drip with zero new source ingestion.
