---
name: cinematic-storyboard-sheet
description: Generate professional Hollywood-caliber vertical storyboard sheet images from cinematic storyboard text, shot lists, scripts, or character reference images. Use when Codex must call image_gen to create an image-only black-background storyboard layout with 3:2 cinematic frames on the left, aligned production text on the right, exact Action / Camera / Lens / Movement / Lighting / Color / optional Dialogue sections, and strict exclusion of calendar dates from the sheet. Never use this skill for text-only prompts, plans, summaries, or non-image outputs.
---

# Cinematic Storyboard Sheet

## Overview

Create a polished vertical storyboard sheet image as a continuous top-to-bottom cinematic timeline. This skill is image-only: when it is invoked, call `image_gen` with the completed prompt and do not return a text prompt, plan, explanation, markdown sheet, or any non-image artifact.

Prioritize production-design clarity: widescreen frame thumbnails, precise shot metadata, bordered text blocks, restrained black-and-grey styling, and no calendar dates anywhere in the rendered sheet.

## Output Contract

- Always use the `image_gen` tool to generate the final storyboard sheet image.
- Do not use file generation, SVG/HTML composition, plain text, or prompt-only output as the final result.
- Do not ask clarifying questions before generation; make reasonable cinematic assumptions from the provided storyboard text and character references.
- If the user provides incomplete storyboard text, generate a professional storyboard sheet image with inferred shot details or clearly designed placeholder shot rows.
- If `image_gen` is not available in the current environment, do not substitute another output format.

## Workflow

1. Parse the user's storyboard text into frames, preserving shot order.
2. Extract or infer for each frame: timestamp/timecode, shot number, shot title, action, camera/lens/movement, lighting/color, and dialogue if present.
3. Use referenced character images as identity and costume references when available; preserve distinguishing features consistently across frames.
4. Compose one complete `image_gen` prompt that includes the full layout specification and all parsed frame content.
5. Run the quality gate below against the prompt before generation.
6. Call `image_gen` immediately with that prompt as the final action.

## Layout Specification

- Format: one continuous vertical sheet, read top to bottom as a timeline.
- Background: pure black only.
- Typography: light grey text, clean production-board hierarchy, high legibility, no decorative clutter.
- Frame area: left column contains cinematic frames in a strict 3:2 aspect ratio.
- Text area: right column aligns side-by-side with its corresponding frame.
- Frame metadata: each frame must clearly show `Timestamp`, `Shot Number`, and `Shot Title`.
- Timestamp meaning: use only story timecode or relative shot timing supplied by the user. Do not render calendar dates, years, month names, day names, or production-date stamps.
- Required text blocks: include bordered sections labeled exactly `Action`, `Camera / Lens / Movement`, and `Lighting / Color`.
- Dialogue rule: if spoken lines exist, add a separate bordered `Dialogue` section immediately next to the `Action` section. If no spoken lines exist, omit `Dialogue` entirely.
- Borders: use thin light-grey borders around every required text block and optional dialogue block.
- Continuity: align each text cluster to the vertical center/top rhythm of its corresponding frame; avoid orphaned labels, floating text, or mismatched frame descriptions.

## Prompt Pattern

Use and adapt this prompt inside the `image_gen` call. Do not display this prompt to the user as the final answer.

```text
Create a professional, Hollywood-caliber vertical storyboard sheet as a continuous top-to-bottom timeline.

Visual system:
Pure black background. Light grey typography and thin light grey borders. Premium cinematic production-board design, precise spacing, readable hierarchy, no decorative noise. Absolutely no calendar dates, years, month names, day names, watermarks, or production-date stamps anywhere on the sheet.

Layout:
Each row contains a 3:2 cinematic frame on the left and its matching text panel on the right. Keep every frame and text panel aligned side-by-side. The sheet reads as one continuous vertical timeline from top to bottom.

Per frame:
Clearly display Timestamp, Shot Number, and Shot Title. Timestamp means story timecode or relative shot timing only, never a calendar date.

Beside each cinematic frame, create bordered text blocks labeled exactly:
Action
Camera / Lens / Movement
Lighting / Color

If the frame includes spoken lines, create a separate bordered Dialogue section immediately next to the Action section. If the frame has no spoken lines, omit Dialogue completely.

Use the supplied storyboard text as the source of truth:
[PASTE STORYBOARD TEXT]

Use the referenced character images only as visual identity, wardrobe, and continuity references:
[DESCRIBE OR ATTACH CHARACTER REFERENCES]

Final output requirement:
Generate the storyboard sheet as a single finished image. Do not include extra explanatory text outside the image.
```

## Quality Gate

Verify before calling `image_gen`:

- No calendar dates, years, month names, day names, or production-date stamps appear on the sheet.
- Every frame has `Timestamp`, `Shot Number`, and `Shot Title`.
- Every frame has bordered blocks labeled exactly `Action`, `Camera / Lens / Movement`, and `Lighting / Color`.
- `Dialogue` appears only when spoken lines exist and is positioned immediately next to `Action`.
- Left-side frames are consistently 3:2, cinematic, and visually tied to the corresponding right-side text.
- The final sheet uses black background, light grey typography, and light grey block borders.
