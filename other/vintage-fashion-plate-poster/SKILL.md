---
name: vintage-fashion-plate-poster
description: Transform a supplied model, portrait, outfit, product, or full-body fashion photo—or a written fashion concept—into a generated vertical vintage fashion-plate poster with aged ivory paper, a centered editorial subject, a restrained double-line frame, high-contrast serif masthead typography, symmetrical microcopy, muted two-ink print color, and flat scanned-catalog texture. Use when the user asks for a retro fashion catalogue cover, heritage lookbook poster, old fashion advertisement without modern commercial gloss, vintage editorial portrait plate, or a poster matching this formal centered paper-and-frame visual language.
---

# Vintage Fashion Plate Poster

Create both:

1. a decisive image-generation prompt; and
2. the matching generated bitmap poster.

Use the built-in image-generation capability by default. Stop at prompt-only only when the user explicitly asks. Follow explicit user requirements over all defaults.

Before composing the prompt, read [references/visual-system.md](references/visual-system.md). It defines the stable visual grammar, variation axes, proportions, and failure corrections.

## Operating Modes

Choose one mode:

- **Photo Transformation**: Default when the user supplies a person, outfit, or product photo. Preserve identity, pose, garment construction, silhouette, accessories, and styling unless the user requests changes.
- **Concept Generation**: Use when the user supplies only a theme or fashion brief. Invent one editorial subject and one coherent outfit; do not create a crowded campaign scene.
- **Copy-Led Plate**: Use only when the user explicitly prioritizes a supplied title or slogan. Keep the person or object present but subordinate.

## Reference and Privacy Rules

- Inspect every local reference image with `view_image` before prompting.
- Treat a supplied image plus a transformation request as permission to use it for image generation; do not ask again.
- Send only the final prompt and required reference images to the generation service.
- Do not browse for, upload, save, or redistribute the source image elsewhere.
- Do not copy a visible brand name, logo, watermark, or campaign phrase from a style reference unless the user explicitly asks and has supplied it as approved copy.
- Use a style reference for layout, print behavior, color logic, and mood—not for duplicating a particular model, garment, brand, or exact wording.

## Build the Subject Card

For a supplied photo, identify:

- **Identity anchors**: face, hair, body proportions, and distinguishing features to preserve.
- **Pose geometry**: stance, hand positions, gaze, weight shift, and silhouette.
- **Wardrobe anchors**: garment type, cut, length, closures, texture, trim, footwear, jewelry, and held objects.
- **Priority detail**: the single styling feature that deserves the sharpest attention.
- **Safe simplifications**: background, minor wrinkles, tiny accessories, and incidental clutter that may disappear.
- **Crop requirement**: full body with visible feet by default; use three-quarter or portrait crop only when requested or when the source cannot support full body.

For concept generation, define the same fields deliberately rather than filling them with random detail.

## Text Intent Gate

Separate user words into **subject matter** and **approved in-image copy**.

- Treat a theme, mood, brand-adjacent reference, or quoted concept as subject matter unless the user explicitly asks to print it.
- Reproduce supplied copy exactly. Do not translate, expand, or add a subtitle without permission.
- If the user supplies no copy, author only a short fictional, non-branded masthead of 3–9 letters and an optional bottom descriptor of 1–3 words. Avoid names or marks visible in a reference image.
- Never invent dates, prices, URLs, issue numbers, locations, collection years, or calls to action.
- Build one explicit `allowed in-image text` list for the generation prompt. Require no other legible words, letters, or numerals.
- If exact spelling matters, keep wording short and inspect the result carefully. Report remaining text defects honestly.

## Composition Compiler

Resolve these visible decisions in order:

1. **Canvas and paper**: vertical 3:5 flat paper poster by default; warm ivory or pale cream stock with gentle age and no surrounding app UI.
2. **Frame system**: one restrained inset double-line or line-plus-shadow frame, comfortably inside the paper edge.
3. **Subject geometry**: one centered full-body figure or isolated fashion object; clear silhouette; feet and head fully contained; generous open paper around it.
4. **Editorial hierarchy**: masthead first or subject first depending on the brief; frame and microcopy remain subordinate.
5. **Typography**: high-contrast display serif masthead, tiny balanced side notes, and one optional bottom imprint using only approved wording.
6. **Color system**: paper plus near-black subject tones, one faded warm display ink, and one cool line ink; derive alternatives from the outfit when requested.
7. **Print material**: matte paper, slightly uneven ink, soft halftone, faint registration drift, edge wear, and a flat scan rather than a photographed mockup.
8. **Mood**: poised, reserved, cultivated, archival, and quietly theatrical—not glamorous, cinematic, or contemporary e-commerce.

State each decision concretely in the final prompt. Do not paste theory, file paths, analysis notes, or checklist language into it.

## Prompt Shape

Write four compact paragraphs:

1. canvas, paper, frame, margins, and overall hierarchy;
2. subject identity/pose/outfit preservation or invented concept, scale, crop, and placement;
3. exact approved copy, typography placement, ink colors, and print imperfections;
4. flat-scan mood, source-reference role, and hard avoids.

For Photo Transformation, explicitly state what must remain recognizable and which background elements must disappear. For Concept Generation, describe one complete but controlled fashion look rather than a collection of unrelated props.

End the prompt with:

`Render only this allowed in-image text: [exact list]. Do not render any other words, letters, numerals, logos, signatures, or watermarks.`

If the user requests a textless result, use:

`Completely textless; no typography, letters, numerals, logos, signatures, or watermarks.`

## Generation Workflow

1. Inspect supplied references.
2. Select the operating mode.
3. Build the Subject Card.
4. Run the Text Intent Gate.
5. Choose a coherent recipe from the visual system.
6. Compile the four-paragraph prompt.
7. Generate the image.
8. Inspect it at full size and thumbnail size.
9. Regenerate at most once with a targeted correction when a hard failure appears.
10. Return the final image, prompt, recipe, and a brief rationale.

## Inspection Gate

Treat these as hard failures:

- altered identity, pose, garment silhouette, or important accessory in Photo Transformation mode;
- cropped head, feet, hands, or frame collision when a full-body plate was intended;
- a modern studio, runway, storefront, app screenshot, or e-commerce background;
- duplicated people, malformed hands, extra limbs, or unstable held objects;
- copied reference-brand text, invented factual metadata, misspelled approved copy, or any text outside the allowlist;
- a heavy decorative border, ornate Victorian clutter, dense collage, glossy mockup, drop shadow, or visible 3D paper depth;
- bright multicolor advertising, cinematic lighting, fashion-magazine glamour, or high-resolution digital polish that erases the aged print character.

On failure, name only the observed defect and reinforce the relevant invariant. Do not redesign unrelated parts. Regenerate once; if the second result still fails, return the better result and disclose the defect.

## Output Format

````markdown
**生成图**

![Vintage fashion plate poster](absolute-image-path-or-rendered-image)

**最终 Prompt**

```text
[final prompt]
```

**说明**

- Mode: [Photo Transformation / Concept Generation / Copy-Led Plate]
- Recipe: [subject scale / frame / hierarchy / typography / warm ink / cool ink / paper / print texture]
- Allowed in-image text: [exact list or none]
- [one sentence explaining the central visual decision or a remaining defect]
````

## Final Review

- Does the poster read as a flat vintage fashion plate before it reads as a generic portrait?
- Is there exactly one dominant fashion subject with a clean, readable silhouette?
- Does the subject occupy a confident central scale without crowding the frame?
- Are the paper, frame, masthead, side notes, and bottom imprint aligned to one coherent grid?
- Is the palette restrained and materially printed rather than digitally colorful?
- Is every visible character on the allowlist?
- Is reference imagery used for visual grammar without copying unapproved brand content?
- Does the image remain elegant at thumbnail size?
- Was the image actually generated?

## Example Requests

- "用 $vintage-fashion-plate-poster 把这张模特图做成复古时装画报封面"
- "做一张旧服装目录风的全身人物海报，标题写 LUNE"
- "用这个穿搭生成一张奶油旧纸、砖红刊名、青绿细框的时装 plate"
- "只要 prompt，不要出图"
