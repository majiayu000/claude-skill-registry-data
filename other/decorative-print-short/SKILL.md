---
name: decorative-print-short
description: Use for a decorative print-illustration short with fine closed linework, flat restrained color, dense ornament, a wide-establishing then close-follow shot rhythm, and sparse synchronized material SFX. Unlike generate-video (relationship 0.66), choose this when the print grammar and paired-shot structure own the result; choose generate-video for a general clip. Do not use for protected designs, logos, dialogue, or automatic music.
---
# Decorative Print Short
## Catalog
- Display name: Decorative Print Short
- Categories: Video
- Status: Ready
- Route label: Decorative print paired-shot production
- Tone: orange
- Short description: Produce an elegant flat-print short with paired wide and close shots.
## What this skill does
- Plans generic decorative print art direction without copying protected designs.
- Creates key art and paired wide/close action shots with optional native SFX.
## How to use
Provide theme, ratio, duration, supplied references, and any requested audio. Canvas plan storage is used only when supported.
#### Example
```text
做一支 16:9 装饰印刷风茶席短片：每个场景先全景再手部近景，只要茶水与瓷器轻响。
```
## Workflow
1. Lock generic line, flat-color, ornament, and material rules; exclude protected patterns and logos.
2. Approve scene key art and two-shot order before video.
3. Generate approved shots through `$generate-video`, persist per-shot keys, then use `$combine-videos` only for requested assembly.
4. Check print consistency, one action per close shot, hard-cut order, and no unrequested audio/text.
## User-facing output
- Media type: Approved plan, key art, and requested MP4 clips or assembly
- Default quantity: One short sequence
- Content per video: Wide establish plus close follow-up per scene
- Default layout: User-requested ratio
- Model policy: Current image and catalog-selected video routes; no standalone audio claim
- Downstream use: Decorative creative advertising
## Route
- Upstream assets: Theme and optional supplied reference
- Downstream handoff: `$combine-videos` for accepted clips
