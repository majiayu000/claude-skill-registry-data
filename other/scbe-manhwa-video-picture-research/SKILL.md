---
name: scbe-manhwa-video-picture-research
description: "Research manhwa recap video and image workflows and emit story-first, source-traceable scene packets for production, narration, and publishing."
---

# SCBE Manhwa Video Picture Research

Run a deterministic research-to-production loop for manhwa recap and webtoon-derived content with explicit source lanes, story-locked scene packets, and publish-ready outputs.

This skill complements `multi-model-animation-studio-notes`:

- use that skill to organize notes, model comparisons, and handoff packets
- use this skill to operationalize sourcing, scene-packet assembly, narration prep, and publish-path outputs

## Core Rule

Story first.

Do not freeze the entire production into one rigid visual style. Keep the arc coherent, keep the world believable, and spend detail where the beat deserves it.

## Use When

Trigger this skill when the work involves any of the following:

- turning recap videos, webtoon chapters, or chapter text into production-ready scene packets
- extracting reference frames and subtitles into image, video, and narration lanes
- preparing TTS-ready narration from recap subtitles or chapter beats
- building prompt packs that keep world continuity stable while allowing deliberate per-panel style shifts
- packaging source-traceable artifacts for downstream render, edit, and publish steps

## Quick Start

1. Run research packet synthesis:

```bash
python C:/Users/issda/.codex/skills/scbe-manhwa-video-picture-research/scripts/run_manhwa_video_picture_research.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --topic "Marcus Chen Protocol Handshake Arc"
```

2. Add internet workflow baseline + tuning before packaging:

```bash
python C:/Users/issda/.codex/skills/scbe-manhwa-video-picture-research/scripts/run_manhwa_video_picture_research.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --topic "Marcus Chen Protocol Handshake Arc" \
  --run-internet-synthesis
```

3. Generate storyboard and prompt packets from chapter text:

```bash
python C:/Users/issda/.codex/skills/scbe-manhwa-video-picture-research/scripts/run_manhwa_video_picture_research.py \
  --repo-root C:/Users/issda/SCBE-AETHERMOORE \
  --topic "Marcus Chen Protocol Handshake Arc" \
  --chapter-file docs/stories/the-six-tongues-protocol.md \
  --chapter-title "Protocol Handshake" \
  --build-scenes
```

## Workflow

1. Establish the story frame.
- Record the topic, chapter scope, target format, audience, and delivery goal.
- Decide whether the output is a recap video, webtoon adaptation, teaser, animatic, or reference packet.

2. Collect and label sources.
- Read `references/source-lanes.md` and collect benchmark URLs, timestamps, panel IDs, and policy sources.
- Keep official or platform rule sources separate from creator-style examples.
- Keep source title or URL attached to every extracted reference.

3. Extract reference beats, not copies.
- Pull frames from recap videos or representative webtoon panels.
- Record shot type, characters present, environment anchor, text overlay or subtitle state, palette, and emotional function.
- The goal is legal, intentional technique extraction rather than imitation.

4. Split `Arc Locks` from `Panel Flex`.
- `Arc Locks` are the worldbuilding, environment, costume, prop, and character-anchor details that should remain stable inside the active arc.
- `Panel Flex` is where deliberate style variation is allowed for comedy, emphasis, flashback, memory, impact, or dramatic compression.
- Preserve world continuity while allowing effect-level overrides on purpose.

5. Build scene packets story-first.
- Start every scene with the narrative purpose and what the audience should understand or feel.
- Include camera plan, visible action, narration or text, source references, `Arc Locks`, `Panel Flex`, and model-lane notes.
- Use high-detail spikes on key beats and let bridge panels stay simpler when that improves readability and throughput.

6. Build the narration lane from subtitles or scene text.
- Treat recap subtitles as narration candidates unless they are clearly spoken dialogue.
- Mark what becomes TTS narration, what stays as on-screen text, what is dialogue, and what should remain silent.
- Preserve tone and timing so downstream voice or edit lanes do not flatten the beat.

7. Validate prompt and production packs.
- Validate prompts and cadence against `references/prompt-pack-patterns.md`.
- Check that worldbuilding remains stable across the arc.
- Check that any style shift has a narrative reason.
- Check that every production claim remains source-traceable.

8. Hand off to render and publish.

```bash
python scripts/publish/build_story_video_series.py --input <story.md> --output artifacts/youtube
python scripts/publish/mix_story_bgm.py --queue artifacts/youtube/story_series_upload_queue.json --music-file <track.wav>
python scripts/publish/post_to_youtube.py --queue artifacts/youtube/story_series_upload_queue.json --privacy unlisted
```

## Output Contract

Persist these artifacts under `artifacts/manhwa_video_picture_research/<run_id>/`:

- `research_lane_packet.json`
- `production_checklist.md`
- `manifest.json`
- `scene_packets/manifest.json` (when `--build-scenes`)
- `scene_packets/storyboard.json` (when `--build-scenes`)
- `scene_packets/image_prompts.jsonl` (when `--build-scenes`)
- `scene_packets/video_prompts.jsonl` (when `--build-scenes`)
- `scene_packets/voice_script.txt` (when `--build-scenes`)

Artifact expectations:

- `research_lane_packet.json`: source inventory, benchmark references, policy lane, and topic frame
- `production_checklist.md`: readiness gates, traceability checks, cadence checks, and narration checks
- `scene_packets/storyboard.json`: story beat, purpose, source references, `Arc Locks`, `Panel Flex`, and narration intent per scene
- `scene_packets/image_prompts.jsonl`: stable world anchors first, with style overrides only when justified by the beat
- `scene_packets/video_prompts.jsonl`: shot timing, camera intent, motion guidance, and narration alignment
- `scene_packets/voice_script.txt`: TTS-ready narration derived from approved recap subtitles or scene beats, with dialogue separated when needed

## Invariants

- Keep story beat clarity above raw stylistic uniformity.
- Keep source traceability per production claim.
- Keep `Arc Locks` stable across the active arc.
- Keep `Panel Flex` intentional and beat-specific.
- Keep recap subtitles separated into narration, dialogue, text overlay, or silence rather than merging blindly.
- Keep official docs above creator opinion for platform rules.
- Keep narrative cliffhanger and cadence constraints explicit in storyboard packets.
- Keep audio mix targets bounded to narration clarity defaults.
- Keep internet-workflow synthesis optional but recommended before large batch publishing.
- Keep secrets out of artifacts and skill outputs.

## Resource Guide

- `scripts/run_manhwa_video_picture_research.py`: orchestrate source lanes and emit the research packet
- `scripts/build_scene_packets.py`: convert chapter text into storyboard and prompt JSONL files
- `references/source-lanes.md`: source quality lanes and benchmark seeds
- `references/manhwa-recap-playbook.md`: recap production defaults, pacing, motion, and subtitle handling
- `references/prompt-pack-patterns.md`: prompt schema, cast-locking patterns, and scene-packet conventions
- `C:/Users/issda/.codex/skills/multi-model-animation-studio-notes/SKILL.md`: companion note and handoff model for `Arc Locks`, `Panel Flex`, and multi-lane comparisons
