---
name: character-toy-grid-motion
description: Use for an uploaded character transformed into an identity-preserved 9:16 designer-toy poster with six irregular rounded panels and a motion version that opens on one panel before returning to the full grid. Unlike character-reference-sheet (relationship 0.73), choose this for the toy-grid motion deliverable; choose character-reference-sheet for broad design reference. Unlike generate-video (0.61), choose this when the six-panel layout is mandatory.
---
# Character Toy Grid Motion

## Catalog

- Display name: Character Toy Grid Motion
- Categories: Character, Video
- Status: Ready
- Route label: Identity-locked six-panel toy poster and motion
- Tone: purple
- Short description: Turn one character image into a vertical designer-toy six-panel poster and an animated grid reveal.
## What this skill does

- Extracts visible character identity, coverage state, props, and color anchors from one supplied image.
- Produces an irregular six-panel 9:16 poster before planning motion.
- Uses the approved poster as the reference for an opening-panel expansion, return transition, and stable grid motion.

## How to use

Upload one mascot, IP character, or original-character image and state any name, copy, duration, or audio preference. A Canvas-capable Agent may group accepted poster and clip artifacts; otherwise it returns them directly.

#### Example

```text
把这张吉祥物做成 9:16 潮玩六宫格动态海报：第四格先全屏表演，再回到不规则圆角六宫格；保留它的围巾和黄色背包。
```

## Workflow

1. Lock character identity, coverage, props, and a six-panel asymmetric rounded layout with black separations. Do not invent text or clothing.
2. Generate and inspect one poster through the current verified image route; correct panel count, identity drift, and geometry before motion.
3. Use the approved poster with `$generate-video` for a vertical clip: selected panel opens first, returns cleanly, and the six stable panels receive restrained independent motion.
4. Persist one `operationKey` per still and clip, poll accepted receipts only, and never regenerate after an ambiguous submission.

## User-facing output

- Media type: One 9:16 poster and one MP4 motion poster
- Default quantity: 1 poster and 1 clip
- Content per video: Opening-panel reveal and stable six-panel motion
- Default layout: 9:16
- Model policy: Current verified image route plus catalog-selected video route
- Downstream use: Character campaign and social presentation

## Route

- Upstream assets: One character image
- Downstream handoff: `$combine-videos` for accepted campaign edits only
