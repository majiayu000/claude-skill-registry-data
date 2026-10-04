---
name: trim-filler
description: Semantic dead-air / filler removal. Claude reads a clip-local word-timed transcript and marks filler words, trail-offs, false starts, repeated re-starts, and short digressive asides for removal. Emits keeps.json (ranges to keep) and transcript.trimmed.json (kept words with shifted timestamps). Pairs with cut-filler, which applies the cuts to the clip's video.
allowed-tools: Bash
user-invocable: true
---

# trim-filler

Tightens a podcast clip by stripping low-value words, not just silence. Where `tighten-pace` cuts inter-word gaps `> gap_max`, `trim-filler` cuts whole spans of speech that don't carry the point — "uh", "um", "you know what I mean", false starts, and the brief tangents speakers fall into mid-sentence.

Example: `"I opened a restaurant that was like uhm — I love restaurants haha — yeah me too anyways it sold burgers"` → `"I opened a restaurant that sold burgers"`.

## Invoke

```
.claude/skills/trim-filler/trim-filler.sh <in_transcript> <out_keeps> <out_transcript> [pad=0.05]
```

- `in_transcript` — clip-local word-timed transcript JSON (output of `transcribe` rebased to the clip)
- `out_keeps` — written `keeps.json` containing the keep ranges and removal rationale
- `out_transcript` — written clip-local transcript JSON with only kept words and shifted timestamps
- `pad` — kept padding around each retained span (sec)

## Output shape — keeps.json

```json
{
  "source": "<original transcript path>",
  "keeps": [[0.0, 4.21], [5.83, 12.04], ...],
  "removed": [
    {"t0": 4.21, "t1": 5.83, "words": "uhm — I love restaurants haha — yeah me too anyways", "reason": "filler + digression"}
  ],
  "removed_total": 1.62
}
```

## How

1. Build a numbered transcript (one word per line: `<idx>\t<t0>\t<t1>\t<word>`).
2. Ask Claude (`claude -p`) which index ranges to REMOVE because they are filler, trail-offs, false starts, or short asides that don't carry the speaker's point. Speech that delivers the actual content stays.
3. Parse Claude's JSON reply, build the complement (keeps), pad each kept span, merge overlaps, write both outputs.

Re-runs are idempotent via an mtime+pad signature in `<out_keeps>.tfmeta`.

## Pairs with

- `cut-filler` — consumes `keeps.json` and re-encodes the clip's video+audio.

## Caveats

- Operates per-clip after `cut-clip + rebase`. Don't run on the full source transcript — Claude context budget.
- If Claude returns "no cuts", outputs are pass-through.
