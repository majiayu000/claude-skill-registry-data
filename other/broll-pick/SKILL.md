---
name: broll-pick
description: Claude picks CONTEXTUAL/scene-level anchors from a clip transcript (literal objects, establishing shots, evocative concept footage matched to the story's tone — not just keyword nouns) and sources full-bleed B-roll cutaways via keyless yt-dlp YouTube search + mcptube frame-sampling + Claude vision verify. The verify step gets the spoken context and rejects literal-but-wrong matches (e.g. a cat laser toy for a tense "red dot" beat). Aims dense (8-12 windows, targeting cutaway footage on ~60%+ of the runtime; emits cutaway_coverage in the plan and WARNs below BROLL_MIN_COVER, default 0.6). Emits broll_plan.json with per-cutaway placement [t0,t1] and source metadata; clip files are namespaced per-clip. Windows snap to whole chunk-captions boundaries; vision calls capped by BROLL_VISION_CAP (default 16).
allowed-tools: Bash
user-invocable: true
---

# broll-pick

Selects B-roll cutaways for one short. Claude reads the clip transcript +
`chunks.json` (from chunk-captions) + the source `ingest.json`, picks the 3-5
strongest visualizable nouns/topics (NOUN/VERB/EMOTION/PIVOT), and spawns
multiple short cutaway windows per topic — each intercut with the speaker, each
preferring distinct footage. Windows are expressed as whole chunk-index ranges
so no cut lands mid-word.

Per window: keyless YouTube discovery via the mcptube-bundled `yt-dlp`
(`ytsearchN:<query>` — `mcptube discover` is NOT used, it requires an LLM API
key the stack doesn't have), then `mcptube add` the candidate, sample 3 frames
via `mcptube frame`, and show Claude the frame grid (`claude -p` vision) to pick
the best on-subject shot or reject. On reject, the query is rewritten once
(literal↔metaphorical) and retried; a second miss drops the window — no fallback
footage. Chosen segments download via `yt-dlp --download-sections` into
`work/<id>/broll/broll_NN.mp4`.

## Invoke

```
.claude/skills/broll-pick/broll-pick.sh <clip_transcript.json> <chunks.json> <ingest.json> <out_broll_plan.json>
```

- `clip_transcript`: per-clip transcript with `words[]` (clip-local times)
- `chunks`: chunk-captions output (`chunks[]` with `t0/t1/text`)
- `ingest`: `work/<id>/ingest.json` (title + source url)
- `out`: path for `broll_plan.json`; b-roll clips land in `<ingest_dir>/broll/`

## Env

- `BROLL_VISION_CAP` (default 10) — max Claude vision calls per clip.
- `BROLL_PICK=0` — disable; emits an empty plan.
- `MCPTUBE_BIN`, `MCPTUBE_YTDLP` — override binary paths.

## Output (broll_plan.json)

```json
{
  "picks": [
    {"t0": 4.31, "t1": 6.02, "topic": "hippopotamus", "anchor_word": "hippo",
     "query": "hippo swimming underwater", "clip_path": "/abs/work/<id>/broll/broll_03.mp4",
     "source": {"video_id": "abc123XYZ", "title": "...", "url": "https://youtu.be/abc123XYZ",
                "t0_src": 12.4, "t1_src": 14.1},
     "verified": true}
  ],
  "ingested_video_ids": ["abc123XYZ"],
  "vision_calls_used": 4,
  "vision_cap": 10,
  "chunks_mtime": 1746000000.0
}
```

No anchors / all queries miss → `{"picks": [], "ingested_video_ids": []}`, exit 0.

## Idempotency

Caches on transcript+chunks+ingest mtimes via `<out>.pickmeta`.

## Notes

- Records every `mcptube add`-ed `video_id` in `ingested_video_ids` for
  broll-cleanup. Never the podcast source (filtered by ingest url id).
- CPU: 3 frames per candidate, reuses `_lib/encode.sh` thread caps downstream.
