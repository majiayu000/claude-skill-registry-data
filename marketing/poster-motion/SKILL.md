---
name: poster-motion
description: Use for one supplied poster animated as a single continuous motion poster that restores its readable composition, hierarchy, and text as the final lock frame. Unlike generate-video (relationship 0.72), choose this when the poster is a final-frame reference; choose generate-video for a general shot. Do not use for original poster design, slideshows, or narrative multi-shot edits.
---
# Poster Motion
## Catalog
- Display name: Poster Motion
- Categories: Layout & Design, Video
- Status: Ready
- Route label: Final-lock-frame poster animation
- Tone: purple
- Short description: Animate an uploaded poster into one readable, full-frame motion poster.
- Similar skills: brand-stream-mg, dot-matrix-brand-wordmark-motion, make-video-intro
## What this skill does
- Analyzes poster layers, ratio, text hierarchy, and motion carriers.
- Plans one continuous reveal that settles on the supplied poster.
## How to use
Upload a poster and state duration, ratio, motion direction, and audio preference. Canvas-capable Agents may retain the approved plan there; otherwise use chat.
#### Example
```text
把这张 9:16 海报做成 10 秒动态版：标题逐层出现，最后必须锁回原版式。
```
## Workflow
1. Lock poster ratio, core content, text readability, full-frame adaptation, and final lock frame.
2. Approve one timed continuous motion direction; never translate poster text unless asked.
3. Use `$generate-video` with the poster as reference; persist an `operationKey`, poll receipt, and never blind-retry.
4. Check final frame, text, layout, ratio, and unwanted audio.
## User-facing output
- Media type: One MP4 video
- Default quantity: 1
- Content per video: One continuous poster activation and lock frame
- Default layout: Poster ratio or nearest supported full-frame ratio
- Model policy: Current catalog-selected reference-video route
- Downstream use: Social motion poster
## Route
- Upstream assets: One poster image
- Downstream handoff: `$combine-videos` for accepted clips only
