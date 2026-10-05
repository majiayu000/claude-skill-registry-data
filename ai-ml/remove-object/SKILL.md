---
name: remove-object
description: Remove one named unwanted object from a supplied image and reconstruct the revealed scene with an AI-native image edit while preserving all untargeted content. Use for people, props, clutter, signs, or distractions when one explicit target must disappear.
---
# Remove Object
## Catalog
- Display name: Remove Object
- Categories: Utility
- Status: Ready
- Route label: GPT Image 2 consistency-sensitive edit
- Tone: red
- Short description: Remove one object and naturally rebuild what was behind it.
- Similar skills: clean-room, restyle-room
## What this skill does
- Lets the image model identify one target from language and infer the hidden background in context.
- Keeps crop, perspective, lighting, texture, people, and unrelated objects stable.
## How to use
Provide image and identify the target by type, position, color, and relation to nearby objects.
#### Remove one distraction
```text
Remove only the red trash bin at lower right and reconstruct the pavement and wall behind it.
```
## Workflow
1. Bind one removal target unambiguously and list all protected neighboring content.
2. Describe the expected continuation behind it from visible scene cues, without inventing a new focal object.
3. Run `gpt-image` v1.0 with `quality: "medium"`, `imageSize: "2K"`, the supplied references, the requested or source-preserving ratio, `batchCount: 1`, and one result.
4. Ask for one contextual edit; forbid crop, relighting, global cleanup, extra people, or unrelated changes.
5. Inspect target absence, boundary residue, repeated texture, geometry, shadows, and protected landmarks; retry the failed region only.
## User-facing output
- Media type: One repaired image
- Default quantity: 1
- Content per image: Source scene with one target removed
- Default layout: Source composition
- Model policy: GPT Image 2 Medium/2K for consistency-sensitive final image editing
- Downstream use: Photo cleanup and commercial retouching
