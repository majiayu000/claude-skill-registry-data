---
name: chunk-captions
description: Group a clip's word-timed transcript into phrase-sized caption chunks via Claude. Replaces the rolling 4-word window in burn-subtitles. Each chunk is one self-contained phrase that swaps in as a whole unit.
allowed-tools: Bash
user-invocable: true
---

# chunk-captions

Claude reads a clip-local transcript and returns an ordered list of caption
chunks. Each chunk is what one breath/clause would naturally hold (typically
3–6 words) and the chunks together cover every word in the transcript exactly
once, in order.

## Invoke

```
.claude/skills/chunk-captions/chunk-captions.sh <clip_transcript.json> <out.json>
```

- `clip_transcript`: per-clip transcript with `words[]` (clip-local timestamps)
- `out`: path for the chunks JSON

## Output

```json
{
  "chunks": [
    {
      "text": "I saw a car today",
      "t0": 0.0,
      "t1": 1.42,
      "words": [{"w": "I", "t0": 0.0, "t1": 0.15}, ...]
    },
    {
      "text": "and it was red",
      "t0": 1.42,
      "t1": 2.55,
      "words": [...]
    }
  ]
}
```

## Rules

- Every word in `transcript.words` appears in exactly one chunk, in source order.
- Chunk `t0` / `t1` derive from the first/last word in the chunk.
- Chunks are monotonic and non-overlapping.

## How

`build_prompt.py` indexes every word `0..N-1` and asks Claude to return ordered
groupings (lists of word indices). `parse_reply.py` reconstructs each chunk
from its word indices, validates full coverage, and emits `chunks.json`. On
malformed/missing reply it falls back to a deterministic 5-word grouping so
the pipeline never stalls.
