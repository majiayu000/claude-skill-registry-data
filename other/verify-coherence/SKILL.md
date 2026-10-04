---
name: verify-coherence
description: Post-pick gate that re-reads each picked span's transcript and either keeps it as-is or tightens its [t0,t1] to cover only the dominant topic. Prevents shorts that feel like two unrelated clips spliced together.
allowed-tools: Bash
user-invocable: true
---

# verify-coherence

Belt-and-suspenders coherence check that runs AFTER `pick-segments`. Claude
re-reads each span's own transcript slice and verdicts `keep` or `tighten`. On
`tighten`, the span's `[t0, t1]` is replaced with a trimmed range covering only
the dominant topic; if the trimmed range falls below `dmin`, the span is
dropped silently.

## Invoke

```
.claude/skills/verify-coherence/verify-coherence.sh <segments.json> <transcript.json> <out.json> [dmin=20]
```

- `segments`: output of `pick-segments`
- `transcript`: full-source transcript JSON
- `out`: validated segments.json (same shape as input, possibly with tightened or dropped spans)
- `dmin`: minimum surviving span duration; spans tightened shorter are dropped

## Output

Same schema as `pick-segments` output, with two possible per-span additions:
- `coherence_verdict`: `keep` | `tightened`
- `coherence_note`: short reason

Dropped spans are simply absent from the output `shorts[]`.

## How

For each span, build a span-local transcript (lines whose midpoint falls in
`[t0, t1]`) and ask Claude:

> Does this span cover ONE topic, or does it pivot to a second unrelated topic
> partway through? If it pivots, return the trimmed `[t0', t1']` that contains
> only the dominant (longer / hookier) topic. Otherwise return `keep`.

A single `claude -p` call handles all spans in one batch to keep latency low.
