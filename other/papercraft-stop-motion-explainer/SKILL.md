---
name: papercraft-stop-motion-explainer
description: Use for a knowledge explainer built as a layered physical-paper world with dioramas, visible paper edges and shadows, practical paper mechanisms, and stepped stop-motion movement. Unlike make-explainer-video (relationship 0.79), choose this when tactile papercraft and layered staging are essential; choose make-explainer-video for a general treatment. Unlike generate-video (0.57), choose this when one shot belongs to a coherent papercraft explanation plan. Do not use for flat vector, smooth CG, live-action, or generic animation.
---
# Papercraft Stop-Motion Explainer

## Catalog

- Display name: Papercraft Stop-Motion Explainer
- Categories: Video
- Status: Ready
- Route label: Layered physical-paper education production
- Tone: orange
- Short description: Turn a topic into an approved paper-diorama explainer with tactile stills, stop-motion shots, and optional assembly.
## What this skill does

- Translates one learning goal into a paper visual metaphor, characters, props, scenes, and staged depth.
- Requires visible fibers, folds, cut edges, thickness, physical shadows, and paper mechanisms rather than a superficial paper texture.
- Supports a full production plan or an explicitly requested single asset without forcing unnecessary phases.

## How to use

Provide topic or source material, audience, ratio, duration, and whether you want a plan, still, storyboard, short shot, or full explainer. Canvas-capable Agents may retain plan, storyboard, and approvals there; otherwise use chat or local delivery.

#### Example

```text
用分层纸雕和拉杆机关解释火山喷发：面向小学生，30 秒横版。先给三个视觉隐喻和一个四层纸艺布景方案，不要旁白或音乐。
```

## Workflow

1. Lock learning outcome, factual scope, audience, delivery scope, and a visual metaphor. Build a material system with foreground, midground, background, far background, shadows, and practical paper mechanisms.
2. For a complete package, propose directions and continue to detailed assets through the supported API. For a requested single asset, produce only the relevant plan or prompt while retaining the paper contract.
3. Generate approved stills with the current verified image route, then hand off each approved atomic shot to `$generate-video`. Require stepped movement, parallax, pulls, hinges, slides, or settling; forbid smooth CG transformation and plastic surfaces.
4. Persist one `operationKey` per output, poll accepted receipts, and use `$combine-videos` only for requested accepted-clip assembly. Inspect depth, material, clarity, and unwanted audio/text.

## User-facing output

- Media type: Approved production plan, requested stills/storyboard, and MP4 shots or assembly
- Default quantity: One compact explainer package
- Content per artifact: Learning beat, physical-paper staging, motion contract, and QA
- Default layout: 16:9 unless requested otherwise
- Model policy: Current verified image route for stills and catalog-selected video route for shots; no standalone audio claim
- Downstream use: Science, education, and knowledge shorts

## Route

- Upstream assets: Topic, source facts, optional visual references
- Downstream handoff: `$combine-videos` for accepted shot assembly
