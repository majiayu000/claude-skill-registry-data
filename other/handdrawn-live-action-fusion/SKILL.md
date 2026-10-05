---
name: handdrawn-live-action-fusion
description: Use for one live-action short where a rough hand-drawn entity visibly contacts a real hand or object, continuously changes form, and is followed through a connected space. Unlike generate-video (relationship 0.68), choose this when contact-led fusion, a traceable entity, and a delayed handheld chase are the deliverable; choose generate-video for an ordinary atomic shot. Do not use for horror, polished CG, static doodles, or multi-scene edits.
---
# Handdrawn Live-Action Fusion

## Catalog

- Display name: Handdrawn Live-Action Fusion
- Categories: Video
- Status: Ready
- Route label: Contact-led live-action drawing fusion
- Tone: orange
- Short description: Create one warm, rough hand-drawn entity that touches reality, morphs continuously, and escapes through a connected space.
## What this skill does

- Plans a single continuous shot with a real/drawn contact beat in its opening seconds.
- Preserves one recognizable entity while it morphs, travels, and expands into a final environmental payoff.
- Keeps rough crayon, chalk, or colored-pencil texture and excludes horror-coded anatomy and jump scares.

## How to use

Provide the real setting, contact object or hand, entity idea, mood, ratio, duration, and any source image. Canvas-capable Agents may save the approved plan there; otherwise the plan stays in chat.

#### Example

```text
在雨后的厨房里，让一只蜡笔小狐狸从手心绕过手指逃到阳台；15 秒 16:9，一镜到底，温暖、不恐怖。
```

## Workflow

1. Lock one connected location, a contact action in the opening beat, one evolving entity, a chase route, and a warm final environmental transformation.
2. Write timed beats for contact, morph, escape, pursuit, and payoff. Require rough hand-drawn texture, delayed handheld reframing, and visible traces from every prior form.
3. Submit one approved atomic shot through `$generate-video`, selecting the current catalog route for the reference roles and motion. Persist one `operationKey` before submission; poll the receipt and reconcile any unknown outcome without resubmission.
4. Check contact realism, continuity, camera delay, texture, ratio, duration, and non-horror tone. Revise only after a known terminal failure or a diagnosed visual miss.

## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: One continuous contact-to-morph chase
- Default layout: 16:9 unless requested otherwise
- Model policy: Current catalog-selected video route; no fixed provider
- Downstream use: Standalone creative short

## Route

- Upstream assets: Optional scene or identity reference
- Downstream handoff: `$combine-videos` only for user-requested accepted-clip assembly
