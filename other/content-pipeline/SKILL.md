---
name: content-pipeline
description: >-
  Non-interactive content-production toolkit: mine quotable moments from podcast
  RSS feeds and meeting notes, discover clip-worthy moments in video transcripts,
  repurpose long-form source into platform-native drafts (X, LinkedIn, YouTube
  Shorts, newsletter), and batch-score/gate those drafts before publish. Use when
  asked to "mine quotes from this podcast", "find clips in this video", "repurpose
  this into a thread / LinkedIn post / Short", "turn this transcript into posts",
  "extract viral moments", or "gate this batch of drafts". Runs Python scripts end
  to end. For interactive expert-panel scoring of a single artifact see content-ops.
when_to_use: |
  Use when running the content-production pipeline as scripts — ingesting raw source (podcast RSS, meeting notes, video transcripts), repurposing it into platform-native drafts, and batch-filtering those drafts through an automated quality gate before publish. Triggers on "mine quotes from this feed", "find clip-worthy moments", "repurpose this long-form into X/LinkedIn/Shorts/newsletter", "transform these content atoms", or "run the publish gate on these drafts".

  Not when: you want to interactively score, rate, or quality-gate a single piece of content or strategy against an assembled panel of domain experts — use `content-ops` (the expert-panel scorer this pipeline reuses for its optional in-loop gate). Not when the goal is pre-launch variant generation and multi-round optimization of conversion copy — use `autoresearch`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Content Pipeline

Script-driven content production: ingest raw source, repurpose it into platform-native drafts, and gate the drafts before publish. All steps are non-interactive Python; chain them or run any stage standalone.

```
quote-mining ─┐
              ├─► content atoms ─► content-transform ─► drafts ─► quality-scorer ─► quality-gate ─► publish
editorial-brain ┘                       │
                          (optional in-loop expert panel from content-ops)
```

## Setup

```bash
pip install -r requirements.txt      # anthropic, feedparser
cp .env.example .env                 # set ANTHROPIC_API_KEY; configure optional feeds/voice
```

All scripts read/write a data directory (default `./data/`, override with `CONTENT_OPS_DATA_DIR`). Each stage writes a `*-latest.json` the next stage picks up.

## Stages

1. **Ingest — quote mining.** Scan podcast RSS feeds + local meeting notes for quotable, contrarian, viral-worthy moments; emit scored candidates.
   ```bash
   python scripts/quote-mining-engine.py --days 90 --top 50 --min-score 60 \
     --feeds config/feeds.json --notes-dir ./notes/ --speaker "Name"
   ```
   Feeds come from `--feeds <json>`, `QUOTE_MINING_FEEDS_FILE`, or inline `QUOTE_MINING_FEEDS`. See `config/feeds.example.json`.

2. **Ingest — editorial brain.** Two-pass LLM clip discovery on a video transcript: pass 1 finds candidate hook→build→payoff moments, pass 2 deep-scores each on hook/build/payoff/clean-cut (0–100). Only clips at/above `--min-score` (default 90) are cut. Needs `ANTHROPIC_API_KEY`; video cutting needs `yt-dlp` + `ffmpeg` (see `requirements.txt`).
   ```bash
   python scripts/editorial-brain.py --url "https://youtube.com/watch?v=..." --max-clips 5
   python scripts/editorial-brain.py --vtt file.vtt --video-id ID --skip-cut   # analysis only
   ```

3. **Transform.** Repurpose long-form "content atoms" into platform-native drafts — X threads/posts, LinkedIn posts, YouTube Short scripts, newsletter sections. LLM mode is default; `--template-only` runs without the API. The optional in-loop expert panel (`--no-expert-panel` to disable) reuses `content-ops`'s `experts/` and `scoring-rubrics/content-quality.md` — see Cross-skill dependency below.
   ```bash
   python scripts/content-transform.py --atoms atoms.json --top-n 10
   python scripts/content-transform.py --atoms atoms.json --template-only
   ```

4. **Score (batch, heuristic).** Score a batch of drafts on five dimensions — voice similarity, specificity, AI-slop penalty, length appropriateness, engagement potential — and emit pass/fail per draft. No LLM; purely heuristic and fast. Default threshold 60; tune weights via `--init-weights` then edit `data/quality-scorer-weights.json`.
   ```bash
   python scripts/content-quality-scorer.py --input drafts.json --verbose
   python scripts/content-quality-scorer.py --threshold 75 --input drafts.json
   ```

5. **Gate (publish filter).** CI-style gate that runs the scorer and filters drafts below threshold; nothing publishes without passing. `--conservative` passes everything but annotates quality flags instead of dropping.
   ```bash
   python scripts/content-quality-gate.py --input drafts.json --threshold 75
   ```

## Input formats

Content atoms (transform input):
```json
{ "atoms": [ { "id": "atom-001", "content": "Long-form source…", "tags": ["AI"], "platforms_missing": ["x","linkedin"], "repurpose_score": 8 } ] }
```

Drafts (scorer/gate input):
```json
{ "drafts": [ { "id": "draft-001", "platform": "x", "draft": "Content text…" } ] }
```

## Cross-skill dependency

`content-transform.py`'s optional in-loop expert panel does not duplicate the rubric — it reads the sibling `content-ops` skill's `experts/` panels and `scoring-rubrics/content-quality.md`. The path resolves to `../content-ops/` by default; override with `CONTENT_OPS_SKILL_DIR` if the skills live elsewhere. `content-ops` remains the single source of truth for panel definitions.

## Related skills

- [content-ops](../content-ops/SKILL.md) — interactive expert-panel scorer; the canonical quality gate for a single artifact, and the source of the panels this pipeline reuses in `content-transform`
- [autoresearch](../autoresearch/SKILL.md) — pre-launch variant generation + multi-round optimization for conversion copy
