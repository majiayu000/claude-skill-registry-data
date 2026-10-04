---
name: segment-topics
description: Split a transcript into topical chapters. Claude reads the full transcript and emits a list of {t0, t1, title, summary} regions where each region covers one coherent subject. Used by pick-segments to ensure picked spans don't cross topic boundaries.
---

# segment-topics

Claude-driven topical chunking. No keyword heuristics — Claude judges where the subject changes.

## Inputs
- `transcript`: path to `transcribe` output JSON (must have segments or words with timestamps)
- `out` (optional): output JSON path. Default: `<dir>/topics.json` next to the transcript.

## Output
```json
{
  "source": "/path/to/source.mp4",
  "topics": [
    {
      "t0": 0.0,
      "t1": 87.4,
      "title": "Intro and channel pitch",
      "summary": "Greets viewers, teases the compilation."
    },
    {
      "t0": 87.4,
      "t1": 213.1,
      "title": "Soccer challenge fail",
      "summary": "Tries to juggle a ball, eats the field, screams."
    }
  ]
}
```

Boundaries are contiguous (`topics[i].t1 == topics[i+1].t0`). Together they cover `[0, duration]`.

## How
1. Build a compact transcript view (timestamped lines).
2. Send to Claude with the instruction "partition this transcript into contiguous topical regions; emit ~5–20 segments depending on length; favor longer regions over choppy ones; each region must be self-contained (one subject, one bit, one anecdote)".
3. Validate: monotonic non-overlapping spans, full coverage, snap edges to the nearest transcript segment boundary so spans align with sentence breaks.

## Why not just include this in pick-segments
Topic boundaries are reusable. Other consumers (chapter markers, retrieval, future skills) want the same partition. Keeping it separate also lets `pick-segments` cache-hit even when N or duration changes.

## RLM-assisted path (long sources)
On long sources (`RLM_TOPICS=1`, or auto when duration ≥ `RLM_TOPICS_MIN_SEC`=1500s) the
single-prompt compression loses back-half detail, so it runs an rlm map-reduce instead:
`build_rlm_prompt.py` chunks the FULL transcript on natural seams (with overlap), the
orchestrator dispatches one `rlm-segment-subcall` (Sonnet) per chunk, verifies coverage,
and synthesizes `topics.json` + `candidates.hint.json` (ranked by confidence, including
cross-chunk THREAD candidates). Per-chunk results cache under `work/<id>/rlm/`. Falls back
to the single-prompt path on any failure. **Full design + the adopted/rejected tactic
ledger: [`RLM.md`](RLM.md).**

## Status
Implemented (single-prompt + rlm-assisted). Tested on `work/<id>/transcript.json`.
