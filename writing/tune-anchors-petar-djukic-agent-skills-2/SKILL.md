---
name: tune-anchors
description: >-
  Sweep anchor selections over a writing-voice corpus and report which tag
  query produces the best register outcome. Runs match-voice then tighten-style
  over (article × arm) combinations, ranks arms on the four-axis register
  composite, and optionally verifies the top candidates with an external
  detector.
  Triggers: tune anchors, sweep anchors, which anchors should I use,
  calibrate writing-voice, onboard corpus.
---

# tune-anchors

## The objective

Given a `writing-voice/` corpus and one or more target articles, answer:
**which anchor-selection rule produces rewrites closest to the author's own
register?**

A rule is an *arm* — a set of filters over the manifest: `role=venue-voice`,
`tags~clipped`, `pre_ai=true`. Different arms produce different anchor sets,
and the model copies the register of whatever it sees. The right arm is the
one whose anchors give the model a register worth copying.

## The pipeline

Each full trial runs two model passes before measurement:

1. **match-voice** (`drive.py`) — voice rewrite using the arm's anchors
2. **tighten-style** (`tighten.py`) — remove AI-register artifacts (passive
   stacks, nominalizations, filler) using the same model family shown
   transformation pairs, not rules
3. **measure** — register markers on the tightened output

The ranking reflects the final output quality, not the raw voice draft.
Tightening is what removes the AI sound; ranking without it would penalize
arms whose raw drafts carry fixable markers and reward arms whose markers
survive tightening unchanged.

`--no-tighten` skips step 2 and measures the raw voice draft instead. Use it
to isolate the voice effect or to compare the tighten delta across arms.

## When to run

- **Writing-voice onboarding.** After the manifest exists and before the first
  real rewrite. Output is the `--anchor-tags` query to use thereafter.
- **After the corpus grows.** Pool sizes change, and guidance hardcoded to
  a count goes stale. The source study's recommendation (idea-factory#355)
  went stale exactly this way.
- **After adding or removing tags.** A tag query that was inert on the old
  corpus may now select a meaningful subset.

## Prerequisites

| What | Required for | Notes |
|------|-------------|-------|
| `writing-voice/` with manifest | all commands | the corpus being tuned |
| Ollama with the target model | `sweep` (full) | `--dry-run` needs no model |
| Pangram key in `.secrets/` | `verify` only | optional; verify is the last step |

## Commands

### sweep

Run match-voice + tighten over (article × arm) pairs, record register markers.

```bash
pixi run python3 tune_anchors.py sweep \
  --voice-dir ../writing-voice \
  --articles article-a.md article-b.md \
  --arms "tags~clipped" "role=venue-voice" "pre_ai=true" \
  [--n 24] [--model gemma4:12b] [--out ledger.yaml] [--dry-run] [--no-tighten]
```

`--dry-run` runs retrieval only (no model, no cost). It records which
anchors would be selected per paragraph — enough to detect the GH-215 shape
(wrong anchors selected, correct ones discarded) without spending compute.

Full mode runs `drive.py` then `tighten.py` per (article, arm), captures
register markers and structural metrics from the tightened output. Requires
Ollama.

`--no-tighten` skips the tighten step and measures the raw voice draft.

### rank

Score arms on the register composite, emit a sorted table.

```bash
pixi run python3 tune_anchors.py rank --ledger ledger.yaml [--blind]
```

`--blind` hides arm labels, replacing them with 8-character hashes, and
shuffles the output. Blindness matters: in the source study the operator
twice guessed wrong about which sources were clipped.

Disagreements — an arm that ranks well on local metrics but poorly on the
detector (or vice versa) — are flagged with a WARNING rather than averaged
away.

### verify

Scan top K with Pangram, record detector results.

```bash
pixi run python3 tune_anchors.py verify --ledger ledger.yaml --top 3 [--budget 10]
```

This is where the money goes, and it is deliberately last. Refuses to exceed
`--budget` total scans. Records results back to the ledger so `rank` can
surface disagreements on the next run.

## Worked example

```bash
# 1. Dry-run: see what retrieval selects (free)
pixi run python3 tune_anchors.py sweep --dry-run \
  --voice-dir ../autogenic-systems/writing-voice \
  --articles posts/2026-07-distributed-scheduling.md \
  --arms "tags~clipped" "role=venue-voice" "tags~economics"

# 2. Full sweep: voice + tighten (requires Ollama)
pixi run python3 tune_anchors.py sweep \
  --voice-dir ../autogenic-systems/writing-voice \
  --articles posts/2026-07-distributed-scheduling.md \
  --arms "tags~clipped" "role=venue-voice" \
  --model gemma4:12b --out calibration.yaml

# 3. Rank: which arm produced the best register after tightening?
pixi run python3 tune_anchors.py rank --ledger calibration.yaml

# 4. Verify top 2 with Pangram (optional, costs 2-4 scans)
pixi run python3 tune_anchors.py verify --ledger calibration.yaml --top 2 --budget 6

# 5. Record the winner into the venue profile (GH-339)
pixi run python3 ../match-structure/scripts/venue_profile.py set-anchors \
  --venue newsletter --voice-dir ../autogenic-systems/writing-voice \
  --arm "tags~clipped" --composite 0.81 \
  --note "swept 1 article, gemma4:12b, verified top-2"
```

### Recording the winner (writeback)

A sweep whose result lives only in a ledger gets re-guessed next quarter.
When the repository carries venue profiles (`writing-voice/venues/`, see the
writing-voice rule), record the winning arm into the profile it was swept
for: `set-anchors` writes the arm as the profile's `anchor_query` and stamps
`provenance` (source, date, composite, note), so the profile always carries
the last calibrated arm rather than a hand-guessed one. Pass the winning
arm expression exactly as `rank` printed it — `set-anchors` parses it with
this skill's own parser.

## The three findings this harness encodes

**Pool size is a confound.** A comparison of two tag queries with different
pool sizes measures size and identity together. The `--n` flag samples arms
to a common size; vary size only as its own arm.

**Local metrics and the external detector can point opposite ways.** A sweep
cannot rank on either signal alone: it needs both, recorded separately, with
disagreement surfaced rather than averaged away. That is why `verify` is a
separate step that records to the ledger rather than a number folded into the
composite.

**Tightening is not optional in the production pipeline.** Ranking on the raw
voice draft over-penalizes arms whose AI-register markers are removable and
under-rewards arms whose markers persist through tightening. The harness
measures what the reader sees, not what the model produced.

## Relationship to other skills

- **match-voice** — the rewrite engine this harness drives. `sweep` calls
  `drive.py` per trial.
- **tighten-style** — the AI-register removal step. `sweep` calls
  `tighten.py` on each voice draft before measuring.
- **filter-tells** — the register measurement this harness reads. `rank`
  scores on the same four-axis composite `register_markers.py` computes.
- **match-structure** — provides `voice_anchors.py`, the retrieval engine
  that `sweep --dry-run` calls directly.
