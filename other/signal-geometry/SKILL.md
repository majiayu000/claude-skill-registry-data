---
name: signal-geometry
description: Create Signal Geometry abstract illustrations and posters from concepts or briefs. Use when the user asks for sparse geometric visuals, editorial posters, spatial systems, or prompt-only image recipes.
---

# Signal Geometry

Translate one idea into one precise spatial behavior, then render it as a sparse geometric system on clean matte paper. Generate the image by default when the required capabilities are available; otherwise return the compiled prompt and recipe.

## Visual identity

Build every image from these invariants:

- **One event:** express one relationship such as orbit, convergence, divergence, compression, deflection, propagation, oscillation, filtering, enclosure, or release.
- **Quiet field:** let the motif span the composition when useful while keeping actual mark density low. Aim for roughly 70%-95% quiet background and 2%-8% line, dot, hatch, or mesh coverage.
- **Equal polarity:** treat light and dark as equal modes. Use clean neutral off-white stock for light mode and charcoal-dyed stock for dark mode.
- **Material surface:** render a full-frame, flat, uncoated matte paper surface with fine irregular grain and faint fibers. Keep it visible at full size and quiet at thumbnail size. Present the paper without borders, mockup depth, edge shadows, stains, tears, or vintage distress.
- **Precision marks:** use hairlines, arcs, dots, nodes, particles, restrained hatching, grids, or wireframe meshes. Use a three-step contrast hierarchy: faint scaffold, readable structure, and very few bright anchors.
- **Restrained color:** stay grayscale by default. When color carries meaning, use one pin-sized coral, orange-red, or cobalt accent covering less than about 0.2% of the canvas.
- **Text gate:** include no text by default. When text is explicitly necessary, use only the user's exact wording as one short phrase or up to three micro-labels, with no more than six words total.
- **Editorial finish:** keep the rendering crisp, orthographic, calm, analytical, and slightly speculative. Let topology, rhythm, scale, and transformation create interest.

Use the reference set to anchor geometry, spacing, hierarchy, restraint, and matte material. Treat its light and dark examples as equal modes.

## Formats

- Use `16:9` for a default illustration.
- Use `4:5` for a poster request. Recompose vertically instead of cropping a landscape layout.
- Use approximately `2.2:1` only for an explicit ultrawide request.
- Honor exact dimensions supplied by the user.

When polarity is unspecified, choose the mode that gives the spatial event the clearest contrast and record the choice in the recipe.

## Grammar families

Choose one primary family. Add at most one subordinate mark language when the relationship needs it.

| Family | Best for | Primary marks |
| --- | --- | --- |
| Orbital field | cycles, gravity, recurrence, scale, mutual influence | circles, arcs, radial ticks, loops, spherical meshes |
| Flow transformation | emergence, routing, filtering, pressure, change | streamlines, particles, arrows, gates, obstacles |
| Signal strip | rhythm, cadence, phases, comparison, accumulation | waveforms, lanes, bars, repeated measures, faint grids |
| Topology map | relationships, context, systems, dependencies | nodes, edges, frames, sparse modules |
| Layered field | tension, thresholds, overlap, latent depth | ruled planes, hatching, contours, wireframe surfaces |

## Workflow

### 1. Lock the brief

Identify the concept, emotional temperature, output format, polarity, text policy, and execution mode. Infer only values the user left open, using the defaults above.

Set execution mode to `rendered` only when image generation and image inspection capabilities are both available. Use `prompt-only` when the user requests it or either capability is unavailable.

Completion criterion: all six values are explicit before composition begins, and any unavailable capability is recorded for delivery.

### 2. Distill the spatial proposition

Turn the concept into one transformation verb and one primary grammar family. Write one internal visual sentence that states what moves, changes, or relates to what. Prefer abstract relations over illustrated nouns.

Completion criterion: the image can be described in one sentence without listing unrelated objects or multiple events.

### 3. Lock quality anchors

Read [references/example-index.md](references/example-index.md) and select one or two matching entries. Inspect each linked image when image inspection is available; otherwise use the entry description as the quality anchor. For every selected anchor, record one anchor delta:

- three invariants to preserve;
- three axes to change across format, topology, composition, viewpoint, polarity, motion, scaffold, or accent.

Use the examples as quality anchors, not layouts. Do not pass sample filenames, provenance, or sample-specific content into the image prompt.

Completion criterion: every selected anchor has a three-invariant, three-axis anchor delta, and the planned composition satisfies each delta.

### 4. Declare the recipe

Choose exactly one value for each axis:

- format: `16:9`, `4:5`, `2.2:1`, or supplied dimensions;
- polarity: light or dark;
- family: orbital, flow, signal, topology, or layered;
- transformation: one active verb;
- geometry: radial, bilateral, directional, paired, distributed, or vertically staged;
- scaffold: open field, faint grid, framed region, or baseline;
- anchor: off-white endpoint, central node, contrast line, structural void, or none;
- accent: none, coral, orange-red, or cobalt;
- text: none or the exact supplied wording.

Completion criterion: all nine axes have one declared choice and support the same spatial proposition.

### 5. Compile the image prompt

Write four compact paragraphs containing only information that should become pixels:

1. State canvas, ratio, polarity, matte paper material, and quiet-space target.
2. State the spatial proposition, family, transformation, geometry, and focal placement.
3. State mark vocabulary, three-tier contrast, optional micro-accent, and exact text policy.
4. State the flat editorial finish and the rejection constraints below.

Make the prompt decisive about position, scale, line density, and hierarchy. Keep analysis notes, recipes, filenames, and provenance outside the prompt.

Completion criterion: the prompt answers all four fields, contains one visual event, and obeys the text gate.

When execution mode is `prompt-only`, stop here. Return the exact compiled prompt and the complete recipe from Step 4 with status `PROMPT_ONLY`; skip generation and image QA. Add one concise capability note outside the prompt only when the mode is a fallback.

### 6. Generate one candidate

Use the built-in image generation capability. Generate a raster image at the selected ratio. If the user supplied an image, use it only for the requested content or structural cue while preserving Signal Geometry's visual identity.

Completion criterion: one inspectable candidate exists at the requested ratio.

### 7. Inspect and repair

View the candidate at full size and thumbnail size before presenting it. Check every critical gate below. Treat the first render as a candidate, not an automatic final.

If any gate fails, read [references/repair-playbook.md](references/repair-playbook.md), identify the single largest defect, tighten only the relevant prompt fields, and regenerate once.

Completion criterion: every critical gate passes. If the repaired candidate still misses a gate, label the result `DONE_WITH_CONCERNS` and name the remaining defect.

### 8. Deliver

Show the accepted image first, followed by the exact final prompt and the complete recipe from Step 4 plus status. Include a saved path only when the image was saved into the user's workspace. Return no attribution or provenance note.

Completion criterion: the user receives the accepted image, its exact prompt, and its recipe.

## Critical gates

Require all of the following:

- Correct requested ratio and a composition designed for that ratio.
- One legible spatial event and one primary family.
- Quiet background remains dominant even when the motif spans most of the frame.
- Clean matte paper grain is visible up close without becoming distressed or decorative.
- Light or dark polarity has three distinct contrast levels.
- Fine marks remain coherent, separated, and intentional.
- Color, when used, is one tiny semantic event.
- The text gate is obeyed with no stray letters, numerals, watermarks, or pseudo-text.
- The image reads at thumbnail size and rewards full-size inspection.
- Every recorded anchor delta passes.

Reject candidates that resolve into a dashboard, infographic, product screen, sci-fi HUD, colorful data visualization, generic gradient blob, photographic scene, character illustration, collage, aged zine, glossy 3D render, or recognizable copy of a reference composition.

## Output shape

For `PROMPT_ONLY`, omit the Image section.

````markdown
**Image**

![Signal Geometry illustration](absolute-image-path-or-rendered-image)

**Final prompt**

```text
[exact prompt used for the accepted image]
```

**Recipe**

- Format: [ratio]
- Polarity: [light/dark]
- Family: [family]
- Transformation: [verb]
- Geometry: [choice]
- Scaffold: [choice]
- Anchor: [choice/none]
- Accent: [choice/none]
- Text: [none/exact supplied wording]
- Status: [DONE/DONE_WITH_CONCERNS/PROMPT_ONLY]
````
