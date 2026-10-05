---
name: live-sketch-motion
description: Use for a real photo, video, or approved realistic preview where a foreground marker visibly and progressively converts one still-moving subject into a colored-pencil sketch. Unlike animate-image (relationship 0.75), choose this when marker-tip synchronization and live-to-sketch conversion are required; choose animate-image for ordinary still motion. Unlike generate-video (0.64), choose this when source composition and ongoing subject motion must be preserved through the reveal.
---
# Live Sketch Motion

## Catalog

- Display name: Live Sketch Motion
- Categories: Video
- Status: Ready
- Route label: Marker-synchronized live-to-sketch conversion
- Tone: blue
- Short description: Animate a real scene while a visible marker progressively redraws one moving subject as a lively colored-pencil sketch.
## What this skill does

- Preserves source composition, identity, support surfaces, and plausible background micro-motion.
- Specifies a natural marker hand, tip-synchronized reveal, and a three-layer white-border, black-line, hatched-fill sketch.
- Prevents frozen subjects, pre-reveals, sticker pop-ins, and generic overlay effects.

## How to use

Provide a photo, a motion reference, or a text scene; include target subject, ratio, duration, sketch style, and sound preference. Text-only scenes receive a realistic preview gate. Canvas-capable Agents may store plan and prompt documents there; otherwise they deliver them in chat or locally.

#### Example

```text
把这张跑步小狗照片做成 7 秒横版视频：蓝色马克笔从右下进入，边画边把小狗变成彩铅涂鸦，小狗全程继续跑。
```

## Workflow

1. For text-only requests, create and approve a realistic source preview. For supplied media, lock composition, identity, subject path, support contact, and camera compatibility.
2. Plan marker entry, natural grip, tip contact, upper-left-to-lower-right reveal, hand exit, and continuous subject motion.
3. Send one approved clip to `$generate-video` with source roles explicit. Persist an `operationKey`, poll only the accepted receipt, and stop to reconcile unknown outcomes.
4. Inspect the opening, reveal, and ending frames for no pre-reveal, no freeze, correct layer order, plausible occlusion, ratio, and audio policy.

## User-facing output

- Media type: One MP4 video and optional approved preview
- Default quantity: 1
- Content per video: One continuous marker-driven subject conversion
- Default layout: Source ratio or 16:9
- Model policy: Verified image route for text-only preview; catalog-selected video route for clip
- Downstream use: Social and creator visual effects

## Route

- Upstream assets: Real photo, reference video, or approved preview
- Downstream handoff: `$combine-videos` only for accepted clips
