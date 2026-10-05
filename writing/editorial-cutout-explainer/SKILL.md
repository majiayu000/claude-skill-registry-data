---
name: editorial-cutout-explainer
description: Use for an approval-first knowledge explainer with generic editorial cutouts, framed information labels, torn-paper texture, shallow 2D parallax, and evidence-led beats. Unlike paper-collage-explainer-generator (relationship 0.76), choose this for information-design cutouts and shallow motion; choose paper-collage-explainer-generator for tactile halftone paper assembly. Do not use for named-publisher imitation, external APIs, automatic voice/music/subtitles, or long fiction.
---
# Editorial Cutout Explainer
## Catalog
- Display name: Editorial Cutout Explainer
- Categories: Video
- Status: Ready
- Route label: Evidence-led editorial cutout production
- Tone: orange
- Short description: Plan and create a generic editorial cutout explainer with shallow 2D motion and approved evidence beats.
- Similar skills: make-explainer-video, line-doodle-explainer
## What this skill does
- Builds a thesis, beat plan, and key visual system before paid media.
- Uses readable evidence and generic cutout grammar without copying any publisher style.
## How to use
Provide a topic, article, or report; include evidence, ratio, duration, and any explicitly supported narration/subtitle need. Canvas storage is optional.
#### Example
```text
把这份气候报告做成 45 秒剪报拼贴科普：先出论点、关键视觉和分镜，使用浅视差和信息标签。
```
## Workflow
1. Lock factual scope, thesis, beat budget, evidence roles, and generic cutout visual rules.
2. Approve plan and keyframes before using image/video routes.
3. Hand each accepted visual beat to `$generate-video`; use `$combine-videos` only for requested assembly and persist keys/receipts.
4. Check evidence clarity, shallow 2D motion, and no unwanted audio/text.
## User-facing output
- Media type: Approved plan, key visuals, and requested MP4 clips or assembly
- Default quantity: One short explainer
- Content per video: One evidence-led editorial beat
- Default layout: User-requested ratio
- Model policy: Current verified image and catalog-selected video routes
- Downstream use: Knowledge and report explainers
## Route
- Upstream assets: Topic and evidence materials
- Downstream handoff: `$combine-videos` for accepted clips
