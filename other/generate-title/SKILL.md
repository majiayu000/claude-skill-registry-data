---
name: generate-title
description: Generate a per-clip third-person engagement-driven title card text. Claude reads the clip's transcript, the source ingest.json metadata, and (optionally) pick-segments' per-span judgment (topic, rationale, suggested title) so it reads the speaker's register — sincere vs ironic vs joking — before titling. Emits a hook-driven ALL-CAPS title (<=7 words).
allowed-tools: Bash
user-invocable: true
---

# generate-title

One title per clip. Third-person, names the subject, promises a specific
moment, ALL CAPS, ≤7 words. Designed for the title-transition skill.

## Invoke

```
.claude/skills/generate-title/generate-title.sh <clip_transcript.json> <ingest.json> <out.txt> [title-context.json]
```

- `clip_transcript`: clip-local transcript with `words[]` and/or `segments[]`
- `ingest`: the source video's ingest.json (provides title, uploader, url —
  helps name the subject when the transcript doesn't say it explicitly)
- `out`: text file with the title (single line, ALL CAPS, ≤7 words)
- `title-context` (optional): pick-segments' per-span judgment —
  `{topic, rationale, title_suggestion}` — sliced out of `segments.json` by
  the orchestrator. The clip-local transcript alone can't carry the
  speaker's register, so a line read literally can invert the meaning (an
  ironic "what he refuses to think about" titled as a sincere confession).
  When present, the model reads tone from this context FIRST (Step 0:
  sincere / ironic / joking / provocative) and titles the actual point, not
  the surface words. Never shown to the viewer; omitting it falls back to
  the old clip-only behavior.

## Output

A single-line text file. Example contents:

```
WATCH SPEED RAGE AT STREAM SNIPERS
```

## Prompt principles (enforced)

- Third person — never "I", "me", "my", "we".
- Name the subject (inferred from clip transcript + ingest.json).
- Promise ONE specific moment, behavior, or reaction — not a vague topic.
- ≤7 words, ALL CAPS, no emoji, no clickbait punctuation (no "?" / "!" / "..." / quotes).
- No "Watch X..." filler when it doesn't add a hook; only use opener verbs
  when they sharpen the promise.

## Fallback

If `claude -p` fails or the model returns something unusable (empty, >7 words,
contains banned punctuation), `parse_reply.py` falls back to the first 5
non-filler words from the clip transcript, uppercased.
