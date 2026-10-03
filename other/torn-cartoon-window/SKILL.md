---
name: torn-cartoon-window
description: Tear, peel, split, or puncture a natural paper opening in a supplied photograph and reveal a coordinated hand-drawn 2D cartoon layer underneath. Preserve the real photo while using believable paper fibers, thickness, curl, shadows, and a photo-specific tear shape; reveal either the subject, the surrounding scene, a continuous alternate world, or a subject crossing between real and illustrated layers. Use when the user wants a torn-paper cartoon reveal, ripped-photo portal, peel-away illustration, virtual-real collage, zine-like reality break, or playful photo-and-cartoon composition where the tear itself should feel natural, intentional, and fun.
---

# Torn Cartoon Window

Transform one supplied photograph into a virtual-real hybrid containing:

1. the protected photographic surface;
2. one physically believable torn or peeled opening; and
3. a coordinated hand-drawn cartoon world revealed beneath that opening.

Generate the edited bitmap by default. Stop at prompt-only only when requested. Use the built-in image-generation capability unless the user requests another path.

Read [references/tear-system.md](references/tear-system.md) before writing the final prompt. It defines tear anatomy, reveal modes, archetypes, illustration recipes, and targeted corrections.

## Core Contract

- Keep the original photo as the factual top layer. Do not globally stylize or replace it.
- Add one primary tear or peel by default. Use secondary cracks only when they belong to the same tear event.
- Make the tear physically readable as paper: irregular fiber edge, exposed thickness, curl or lifted flap where appropriate, short contact shadow, and restrained wrinkle tension.
- Make the tear shape and placement respond to a real scene hook such as a pose, path, ridge, window, wheel, cloud, facade, shadow, or motion line.
- Reveal more than a generic cartoon sticker. The underlayer may contain a subject, environment, or small scene, but it must connect meaningfully to the photograph.
- Let the tear itself carry part of the joke through its direction, shape, flap, nesting, or apparent cause. Avoid random decoration.
- Preserve faces, hands, important text, signage, product details, and focal silhouettes unless crossing the tear is the explicit concept.
- Keep the result playful and tactile rather than glossy, cinematic, or heavily AI-rendered.

## Inspect and Normalize the Source

Inspect every local image with `view_image`. Trust the displayed orientation, not the extension or raw pixel dimensions. When the source carries EXIF rotation, MPO data, or an unsupported encoding, create an orientation-correct standard raster with metadata removed, give it a new filename, and inspect that exact copy again.

Build an internal **Reveal Card**:

- **Photo plane**: crop, aspect ratio, perspective, light, grain, and apparent paper color.
- **Dominant subject or rhythm**: person, animal, object, vehicle, building, landmark, landscape, repeated forms, or spatial tension.
- **Protected regions**: faces, hands, existing text, key details, horizons, and focal contours.
- **Continuity anchors**: contours, roads, limbs, buildings, clouds, waterlines, shadows, or color blocks that can continue across the tear.
- **Scene hooks**: at least three structures that could plausibly cause, hold, frame, or interact with a tear.
- **Underlayer scope**: subject only, local scene, alternate scene, or real-to-cartoon crossover.
- **Palette anchors**: two to four source colors shared by photo and illustration.

## Choose What the Tear Reveals

Choose one reveal mode:

- **Subject underlayer**: reveal a complete cartoon translation of the main subject behind the photo surface.
- **Scene underlayer**: reveal a coordinated illustrated version of the local environment, including multiple scene elements when useful.
- **Continuous alternate world**: extend roads, ridges, rooms, skylines, clouds, or landscapes into a playful drawn reality beneath the paper.
- **Crossover seam**: let one complete subject or scene element transition across the torn edge from photographic to illustrated form while keeping geometry aligned.

Do not force a subject-only reveal. Prefer the mode that creates the strongest photo-specific continuity and one-glance idea.

## Design the Tear

Choose one tear archetype from the reference. Define:

- **entry point**: where the tear begins;
- **tear path**: direction and irregular contour;
- **opening**: frame-relative box or polygon and target area, normally 15–35% of the image;
- **flap behavior**: absent, curled, rolled, folded, or hinged;
- **paper anatomy**: fiber edge, thickness, underside color, wrinkle tension, and shadow direction;
- **scene relationship**: the visible element that the tear follows, frames, opens, crosses, or appears to be caused by.

Keep the silhouette asymmetric and materially plausible. Avoid perfect circles, smooth vector waves, rectangular windows, symmetrical bursts, thick white sticker borders, and multiple unrelated holes.

## Connect the Two Worlds

- Align at least two continuity anchors across the torn boundary.
- Preserve pose, direction, perspective, horizon, or structural rhythm where photo and drawing meet.
- Keep the underlayer clearly flat hand-drawn 2D: visible line variation, two to four flat colors, and at most one simple cel-shadow, halftone, or pencil-hatch region.
- Let the exposed paper fibers and curl sit above both layers; let the short shadow fall from the lifted photographic paper onto the cartoon layer below.
- Use a limited source-derived palette so the reveal belongs to the scene without becoming photorealistic.
- Keep the photographic layer dominant by default. Let the illustrated reveal occupy about 15–35% of the frame unless the user asks for a dramatic rupture.
- Add no new readable text, pseudo-writing, logos, signatures, emojis, or watermarks.

## Pass the Tear Interest Gate

Invent at least three concepts that differ in both tear behavior and underlayer content. For each, state internally:

- why the tear begins exactly there;
- what visible scene structure controls its path;
- what the opening reveals;
- how photo and cartoon connect at the boundary;
- why moving the tear elsewhere would weaken the idea.

Reject a concept when the tear is only a decorative frame, the underlayer could belong to any photo, the opening covers protected content, or the joke needs explanation. Require one photo-specific hook, one primary tear gesture, and one reveal idea.

## Prompt Shape

Write four compact paragraphs:

1. identify the source as the protected photographic top layer and lock crop, orientation, lighting, text, and focal content;
2. define the tear archetype, exact target region, tear path, flap geometry, paper fibers, thickness, curl, tension, and shadow;
3. define the reveal mode, complete underlayer content, illustration recipe, continuity anchors, and cross-boundary alignment;
4. define visual hierarchy, palette harmony, physical integration, and hard avoids.

Use direct edit language: `Keep the source photograph unchanged outside the one torn opening and its physically necessary curled paper edge and shadow.`

## Workflow

1. Inspect and orientation-normalize the source when needed.
2. Build the Reveal Card and protect important regions.
3. Create three photo-specific tear-and-reveal concepts.
4. Select one concept through the Tear Interest Gate.
5. Verify the opening can contain the intended underlayer at phone-readable size.
6. Choose one tear archetype, one reveal mode, and one illustration recipe.
7. Compile the four-paragraph prompt and generate the edit.
8. Inspect full-size, ordinary phone-view, and thumbnail previews.
9. Regenerate at most once with one targeted correction for a hard failure.
10. Return the image, final prompt, tear archetype, reveal mode, and a one-sentence explanation of the interaction.

## Hard Failures

Regenerate when:

- the source orientation, crop, photo content, lighting, existing text, or color grade changes materially;
- the tear looks like a white sticker outline, smooth frame, portal glow, plastic peel, or pasted collage shape;
- fibers, paper thickness, curl, flap logic, wrinkle tension, or contact shadow are missing or contradictory;
- the opening is arbitrary, covers protected content, or has no visible relationship to the source scene;
- the underlayer is photorealistic, unrelated, generic, too small to read, or merely a duplicated icon;
- continuity anchors do not align across the boundary;
- a subject crossing the seam becomes incomplete, malformed, duplicated, or geometrically discontinuous;
- the whole photograph becomes illustrated instead of remaining the top layer;
- extra text, symbols, logos, speech bubbles, decorative clutter, or watermarks appear.

Correct only the observed defect. Preserve successful tear physics, placement, and reveal content. If one correction still fails, return the stronger result and disclose the remaining issue.

## Output Format

````markdown
**生成图**

![Torn cartoon window](absolute-image-path-or-rendered-image)

**最终 Prompt**

```text
[final prompt]
```

**说明**

- Tear: [archetype / location / paper behavior]
- Reveal: [mode / content]
- Continuity: [two boundary anchors]
- Style: [recipe / palette / line / shading]
- [one sentence explaining why the tear is fun in this specific photo]
````

## Quality Gate

- Is the original photo preserved outside the tear?
- Does the tear look physically possible and tactile?
- Is the torn-paper display itself interesting rather than merely framing content?
- Does the tear path belong specifically to this photograph?
- Is the revealed layer clearly hand-drawn and readable at phone size?
- Can the underlayer include enough of the scene to feel like another world rather than a sticker?
- Do at least two contours, directions, structures, or colors connect across the edge?
- Are protected faces, hands, text, and focal details safe?
- Is the idea understandable without a caption?
- Is the result free of glossy AI effects, malformed geometry, and unwanted text?
- Was the edited bitmap actually generated?
