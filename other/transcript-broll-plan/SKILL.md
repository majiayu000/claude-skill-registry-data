---
name: transcript-broll-plan
description: Use for a transcript, voiceover, or talking-head script that must become a reviewable B-roll plan with semantic beats, A-roll retention, evidence flags, missing-material checks, and only then approved visual shots. Unlike make-explainer-video (relationship 0.72), choose this when supplied narration governs the plan; choose make-explainer-video for a new explainer. Do not use for subtitle export, trimming, or one-off generation.
---
# Transcript B-Roll Plan
## Catalog
- Display name: Transcript B-Roll Plan
- Categories: Text
- Text category: yes
- Status: Ready
- Route label: Transcript-led B-roll planning
- Tone: blue
- Short description: Turn narration into a reviewable A-roll, evidence, and B-roll plan before generating approved shots.
## What this skill does
- Segments transcripts by meaning and selects the simplest visual support.
- Flags exact claims, missing assets, and text that needs evidence or deterministic handling.
## How to use
Provide the transcript plus available footage, screenshots, charts, and ratio/style constraints. Canvas-capable Agents may save the approved plan there.
#### Example
```text
把这段市场分析口播拆成 A-roll、数据证据和 B-roll 镜头，标出我还要提供哪些截图。
```
## Workflow
1. Segment semantic units and label A-roll, evidence, reuse, typography, or pure B-roll.
2. Produce an approval-gated shot plan; exact facts or copy never become invented imagery.
3. Submit only approved atomic visuals to `$generate-video` with one durable key each.
4. Check claim fidelity, asset roles, continuity, and no unwanted readable text.
## User-facing output
- Media type: Reviewable plan and requested MP4 shots
- Default quantity: One plan per transcript
- Content per video: One approved semantic beat
- Default layout: User-requested ratio
- Model policy: Current catalog-selected video route
- Downstream use: Talking-head and knowledge editing
## Route
- Upstream assets: Transcript and evidence assets
- Downstream handoff: `$combine-videos` for accepted clips
