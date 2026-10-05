---
name: line-doodle-explainer
description: Use for a diagram-first educational short that turns a topic or lesson material into concise narration, sparse line-doodle visuals, and approved storyboard beats. Unlike make-explainer-video (relationship 0.82), choose this when minimalist line figures and explanatory diagrams are required; choose make-explainer-video for a general visual treatment. Unlike make-infographic (0.52), choose this when timed motion and narration are part of the result.
---
# Line-Doodle Explainer

## Catalog

- Display name: Line-Doodle Explainer
- Categories: Video
- Status: Ready
- Route label: Diagram-first line-doodle teaching production
- Tone: blue
- Short description: Explain one topic with sparse line figures, narration beats, diagrams, and an approved animated storyboard.
- Similar skills: make-explainer-video, editorial-cutout-explainer
## What this skill does

- Extracts one learning outcome and a clear explanatory structure from source material.
- Designs simple line figures and diagrams that carry teaching logic instead of decorative motion.
- Plans and generates approved shots without forcing unverified audio or subtitles.

## How to use

Provide the topic, audience, duration, ratio, factual source material, and whether you want a plan, storyboard, or finished shots. Canvas-capable Agents may retain approved plan documents and gates there; otherwise they use chat or local delivery.

#### Example

```text
用极简线条小人解释通货膨胀为什么会让同样的钱买得更少；30 秒竖版，面向高中生，先出旁白和分镜。
```

## Workflow

1. Lock topic, factual boundaries, audience, duration, ratio, and output scope. Write one memory sentence and a diagram-led explanation structure.
2. Draft narration and a storyboard in which each shot teaches one relationship. Use line figures only to clarify scale, contrast, or human stakes.
3. Continue to the supported media API without a client-side payment or publication confirmation. Use `$generate-video` for each approved atomic shot and `$combine-videos` only when an ordered final cut is requested.
4. Persist an `operationKey` per planned output, poll accepted runs, and check factual clarity, visual hierarchy, ratio, and unwanted text/audio.

## User-facing output

- Media type: Approved plan/storyboard and requested MP4 clips or assembly
- Default quantity: One compact explainer
- Content per video: One diagram-led knowledge path
- Default layout: 16:9 unless requested otherwise
- Model policy: Current catalog-selected video route; no standalone audio claim
- Downstream use: Educational and knowledge shorts

## Route

- Upstream assets: Topic, source facts, optional images
- Downstream handoff: `$combine-videos` for accepted shots
