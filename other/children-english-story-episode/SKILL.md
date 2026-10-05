---
name: children-english-story-episode
description: Use for an original, child-safe English-learning story episode with recurring characters, reusable scene assets, a target expression, short vertical story beats, and an optional song outline. Unlike character-reference-sheet (relationship 0.69), choose this when the deliverable is a complete learning episode; choose character-reference-sheet for only design views. Do not use source characters, source worlds, studio-style imitation, stored voice IDs, or automatic song generation.
---
# Children’s English Story Episode
## Catalog
- Display name: Children’s English Story Episode
- Categories: Film, Video
- Status: Ready
- Route label: Original recurring-character learning episode
- Tone: green
- Short description: Plan an original children’s English story episode with reusable character and scene anchors.
## What this skill does
- Turns an original chapter and target expression into child-safe story beats and natural repetition.
- Plans reusable character, scene, and scale references before shot keyframes.
## How to use
Provide original story material, focus character, target expression, age range, duration, and existing supplied sheets. Canvas asset registry is optional when supported.
#### Example
```text
用原创小动物角色教 4–7 岁孩子 “May I join?”：45 秒 9:16，先做故事分镜和角色/场景资产计划。
```
## Workflow
1. Lock original-world rights, learning objective, age suitability, focus character, and short beat structure.
2. Approve script and reusable character/scene/scale assets before keyframes.
3. Use existing image routes and `$generate-video` for approved clips; keep each durable operation key and do not claim voice or song generation.
4. Check consistency, repetition quality, child safety, ratio, and source independence.
## User-facing output
- Media type: Episode plan, requested sheets/keyframes, and MP4 clips or assembly
- Default quantity: One episode plan
- Content per video: One short original learning-story beat
- Default layout: 9:16 unless requested otherwise
- Model policy: Existing character/image routes and catalog-selected video route; no standalone audio claim
- Downstream use: Children’s learning series
## Route
- Upstream assets: Original chapter and supplied recurring assets
- Downstream handoff: `$combine-videos` for accepted clips
