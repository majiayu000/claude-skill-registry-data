---
name: derive-thesis
description: Name the CENTRAL SUBJECT (spine) of a long-form source so selection can tell on-theme moments from clip-shaped tangents. Claude reads the topic chapter list (topics.json) + source duration and emits thesis.json = {subject, thesis_sentence, key_threads[]} — the one durable source-level "what is this video about" artifact the pipeline lacked. Runs AFTER segment-topics and BEFORE pick-segments; pick-segments feeds it as a theme prior + scores each pick's theme_fit against it, and the confidence-floor backfill is gated on it so a high-standalone but off-spine tangent can no longer be auto-injected. Deterministic fallback (subject from the longest topic) on any failure. Non-fatal, idempotent, DERIVE_THESIS=0 skips.
allowed-tools: Bash
user-invocable: true
---

# derive-thesis

A 2-hour talk wanders through one core throughline plus dozens of entertaining
tangents. Nothing in the pipeline named the throughline, so `pick-segments`
maximized standalone virality per span and shipped clip-shaped asides (a beetle
anecdote, a DoorDash story) that misrepresent the source. `derive-thesis`
computes that missing source-level subject once, as a durable JSON artifact both
`pick-segments` (theme prior + `theme_fit` score + backfill gate) and
`selection-report` read.

## Invoke

```
.claude/skills/derive-thesis/derive-thesis.sh <transcript.json> [topics.json] [out.json]
```

- `transcript`: full-source transcript (for duration; the digest is the topic list)
- `topics`: `segment-topics` output (auto-discovered next to the transcript)
- `out`: `thesis.json` (auto-discovered next to the transcript)

## Output

`thesis.json`:

```json
{
  "subject": "Donald Hoffman on consciousness and reality",
  "thesis_sentence": "Perception is a species-specific interface, not a window onto objective reality.",
  "key_threads": ["conscious agents", "fitness beats truth", "spacetime is not fundamental", "the hard problem"]
}
```

On any Claude/parse failure it writes a deterministic fallback (`subject` from
the longest topic's title, `key_threads` from the leading topic titles,
`"fallback": true`) so downstream always has a subject.

## How

`build_prompt.py` renders the whole chapter list and asks Claude to name the
SPINE (not summarize every chapter) — the guest + core theme, the throughline
sentence, and the on-spine sub-themes. `parse_reply.py` validates and clamps,
falling back to a topic-derived subject when the reply is empty/unparseable.
Idempotent via mtime (`topics.json` → `thesis.json`); `DERIVE_THESIS=0` skips.
