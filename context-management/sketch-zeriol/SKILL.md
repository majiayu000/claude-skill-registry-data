---
name: sketch-zeriol
description: "Transform any supplied photograph—especially travel, landscape, road, lake, mountain, desert, salt-flat, or environmental portrait—into the fixed Sketch Zeriol vertical 3:5 travel-sketchbook poster style: warm flax-ivory paper, graphite drawing, restrained source-colored washes, natural erased transitions, a scene-following cinnabar thread, and one relevant typewriter caption. Use whenever the user invokes sketch-zeriol, asks for a Zeriol sketchbook or travel-sketch poster, or supplies a photo with no further instruction in a Sketch Zeriol context. Generate the edited bitmap by default; never introduce torn paper, collage windows, hard frames, or photographic people."
---

# Sketch Zeriol

Turn supplied photographs into one recognizable visual language rather than offering style variants. Generate the image immediately by default. If the user only attaches a photo and says nothing, treat the attachment itself as the request.

Use the built-in image-generation/editing capability. Do not stop at prompt-only unless the user explicitly asks for a prompt.

Read [references/style-system.md](references/style-system.md) completely before analyzing the source or writing the generation prompt. It defines the invariant palette, drawing language, composition, cinnabar-thread behavior, captions, sequence continuity, correction strategy, and hard failures.

## Non-Negotiable Contract

- Produce a vertical 3:5 poster, even when the source is horizontal. Recompose or extend around the truthful scene; do not amputate the essential subject or landform merely to fill the ratio.
- Keep the source photograph as the factual authority for subject, geography, pose, perspective, road, shoreline, ridge, horizon, and light direction.
- Translate the scene into graphite drawing, erased highlights, dry-brush smudges, and restrained translucent watercolor on warm flax-ivory paper.
- Preserve source colors selectively. Let distinctive lake, salt, desert, grass, rock, sky, or clothing colors remain recognizable but quiet.
- Render every person completely as a hand-drawn figure. Preserve identity cues, pose, scale, and placement, but retain no photographic skin, clothing, or face pixels.
- Add one continuous cinnabar-red hand-painted thread that follows a real scene contour. It must be visible, organic, and structurally meaningful.
- Add one small, exact, scene-relevant typewriter caption in available lower whitespace.
- Blend image and paper through graphite fade, erasure, dry brush, and watercolor diffusion only.
- Never use torn paper, peeled edges, ripped openings, collage windows, picture frames, rectangular photo blocks, sticker borders, portals, black blocks, or hard masks.
- Never use a script or post-processing overlay to draw the cinnabar thread. Generate the art, thread, and transitions together in one image-generation pass.

## Inspect the Source

Inspect every local source with `view_image`; trust displayed orientation rather than filename metadata. For each image, determine:

- protected geometry: subject, face, pose, road, shoreline, ridge, horizon, building, or landmark;
- dominant color memory: two to four colors worth retaining;
- truthful continuity anchors: contours the cinnabar thread can inhabit;
- quiet paper zones: areas that can dissolve into drawing or hold the caption;
- crop risk: details that would become awkward or incomplete in 3:5;
- people: every human region that must be fully redrawn.

Do not invent a different landscape. Adding a faint sketched continuation, distant ridge, or horizon is allowed only when it completes the vertical composition without contradicting the source.

## Select Style Anchors

Use the supplied source plus two or three bundled anchors in `assets/style-anchors/` on the first generation call:

- `danxia-road.png`: warm earth, dense mountain drawing, road-led thread;
- `grassland-gully.png`: dark green wash, graphite fade, depth-following thread;
- `dune-wind.png`: broad paper field, restrained ochre, ridge-led thread;
- `blue-salt-lake.png`: luminous water color without loud saturation.

Choose anchors by subject, but always include at least one land anchor and one color anchor. Treat anchors only as art-direction references. The source remains the sole authority for content and geometry.

## Compose the Generation Prompt

Write the prompt in five compact parts:

1. **Source lock** — identify the source as the only factual authority and lock orientation, subject, pose, perspective, scene geometry, and essential color relationships.
2. **Paper and drawing** — request the exact warm flax-ivory paper, graphite construction, erased highlights, cross-hatching, dry-brush smudge, and restrained watercolor defined in the style reference.
3. **Transition and people** — define natural fade zones and require complete hand-drawn conversion of all people.
4. **Cinnabar thread** — name its entry, scene-following route, exit or vanishing behavior, visibility, pigment texture, and protected regions.
5. **Caption and prohibitions** — provide the exact caption and explicitly ban every hard failure.

State that all parts must be generated together. Do not ask the model to paste the photo onto paper or apply a global sketch filter.

## Single-Image Workflow

1. Inspect and orientation-normalize the original when needed.
2. Build the source analysis above.
3. Choose a source-specific composition and cinnabar path.
4. Derive one exact caption from the visible place, object, weather, journey, or mood. Never fabricate a precise location.
5. Generate from the original source plus selected anchors.
6. Inspect full-size and phone-size views.
7. Regenerate from the original source for any hard failure. Supply the failed result only as a layout/path reference, never as the new factual source.
8. Save a versioned output without overwriting the original.

## Carousel Workflow

When given multiple photos, first create an internal sequence plan before generation:

- use only vertical 3:5 outputs;
- order frames by color, scale, geography, and emotional rhythm;
- establish a left and right cinnabar endpoint for every non-terminal slide;
- let the thread vary through roads, ridges, gullies, shores, wind lines, or horizon marks while keeping adjacent edge heights compatible;
- use the first slide as the style and paper-tone anchor after it is approved;
- keep captions geographically accurate and emotionally specific;
- preserve approved frames; do not redraw them merely to normalize thread height;
- generate each frame once from its own original source, selected anchors, and at most one adjacent approved frame for continuity.

The thread may enter or leave at different heights. Continuity means compatible edge endpoints, not a dead-straight horizontal stripe. On the final slide, the thread may follow a road or contour into the vanishing point instead of exiting the right edge.

## Correction Discipline

- Always return to the original photograph when correcting clarity, subject geometry, person rendering, or paper tone.
- Use the prior result only to preserve successful composition, caption, or thread intent.
- Correct one observed defect at a time and explicitly protect everything already approved.
- Keep paper-tone correction inside image generation; do not recolor the old bitmap repeatedly.
- Keep thread correction inside image generation; do not draw it afterward with a vector, script, or mask.

## Quality Gate

Regenerate before delivery when any answer is no:

- Is this unmistakably the same source scene rather than a substituted landscape?
- Is the output vertical 3:5 with complete, intentional subject geometry?
- Does the paper match the bundled warm flax-ivory anchors without turning white or yellow?
- Do graphite lines, erased light, and watercolor washes read as hand-made at phone size?
- Are distinctive source colors visible but restrained?
- Are all people fully hand-drawn and free of photographic patches?
- Does the cinnabar thread follow a real contour, remain clearly visible, and feel hand-painted?
- Does the caption relate to the actual scene, place, or feeling and render exactly once?
- Are all transitions natural smudges or fades rather than tears, frames, masks, or blocks?
- Is the image free of honeycomb embossing, cellular texture, plastic relief, generic AI haze, extra text, logos, and watermarks?

## Delivery

Return the generated bitmap, the saved absolute path, and a concise summary of the source lock, retained colors, cinnabar route, and exact caption. Mention any remaining image-model limitation plainly.
