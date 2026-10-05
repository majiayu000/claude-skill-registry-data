---
name: correct-video-color
description: Correct white balance, exposure, contrast, and shot-to-shot color consistency in supplied video without changing its content or intended creative look. Use for technical color correction and clip matching; do not use for stylized restyling, adding effects, repairing objects, or editing the sequence.
---
# Correct Video Color

## Catalog

- Display name: Correct Video Color
- Categories: Video
- Status: Ready
- Route label: Measured deterministic grade; MiniMax H3 only when temporal rewriting is required
- Tone: orange
- Short description: Correct white balance, exposure and shot-to-shot consistency without changing content or creative look.

- Similar skills: add-video-effect, restyle-video, upscale-video
## What this skill does

- Restores plausible neutrals, skin tones, highlight detail and shadow separation over time.
- Distinguishes technical correction from an optional creative grade.

## How to use

Provide footage, lighting issue, neutral or skin references, protected brand colors and delivery space.

#### Example

```text
Correct the mixed green fluorescent and daylight cast; keep skin natural and preserve the blue jacket exactly.
```

## Workflow

1. Preserve the source and inspect representative frames across every shot for exposure, white balance, contrast, saturation, clipping, noise, and temporal shifts.
2. Determine the input transfer/color space from metadata and measurements. If log versus display-referred is ambiguous, ask; never fit Rec.709 black, midpoint, or highlight targets directly to unidentified log footage.
3. Define neutral, skin, reference-shot, and protected brand-color anchors. Treat skin loci and histogram targets as diagnostic evidence, not universal aesthetic truth. Separate technical correction from any optional creative look.
4. Prefer a deterministic correction chain or generated .cube LUT when exposure, balance, contrast, saturation, black level, or shot matching can be expressed without regenerating image content. Apply camera-specific conversion before display-referred correction and validate LUT domain/order.
5. Use MiniMax H3 only when the defect varies within shots or requires temporal video rewriting that deterministic grading cannot solve. Give correction-only instructions and do not regenerate frames independently.
6. Export to the requested color space/codec without overwriting the source. Re-measure and visually inspect representative frames plus the full timeline for neutrals, protected colors, clipping, banding, skin, flicker, shot matching, gamut/transfer tags, audio preservation, and playback.


## User-facing output

- Media type: One MP4 video
- Default quantity: 1
- Content per video: The same footage with technically balanced color
- Default layout: User-requested delivery format
- Model policy: Deterministic measured grading/LUT first; MiniMax H3 only for temporal correction that requires video rewriting
- Downstream use: Video finishing
