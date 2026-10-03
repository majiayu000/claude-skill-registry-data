---
name: liminal-journey-film-photo
description: Transform supplied photographs or written scene concepts into quiet, wistful, soft-focus journey photography with cinematic framing, anonymous or distant subjects, windows and mirrors, fog or sea spray, foreground occlusion, muted teal-gray shadows, warm amber highlights, film grain, halation, and believable optical imperfection. Use when the user asks for poetic travel photography, nostalgic film stills, liminal transit imagery, a view through a train/car/ferry window, a solitary figure in landscape, dreamy but natural photos, or the visual language of fleeting memories seen while travelling.
---

# Liminal Journey Film Photo

Create photographs that feel discovered between departure and arrival: observational, slightly imperfect, emotionally restrained, and grounded in a believable camera situation. The style comes from composition and distance first; grain and color are finishing layers, not the main effect.

## Required Tool Behavior

- For a supplied image, inspect it first and treat it as an edit target. Use the built-in image generation/editing tool with the image attached.
- For a written concept without an image, generate a new photographic scene.
- Preserve the source aspect ratio unless the user requests another format.
- Do not copy watermarks, usernames, logos, advertisements, captions, or readable text from references. Do not invent them in the output.
- Never bundle or reuse third-party reference images as assets. Use them only to infer abstract visual principles.

## Workflow

### 1. Read the User's Intent

Identify:

- the subject and its essential action;
- which identities, clothing, objects, architecture, or scene geometry must remain unchanged;
- the requested emotional temperature, such as lonely, tender, ominous, warm, or dreamlike;
- any explicit preference for clarity, subject size, color, crop, or camera position.

Explicit user direction overrides every default in this skill.

### 2. Find the Photographic Story

Analyze the source or concept on five axes:

1. **Anchor** — the one person, object, vehicle, building, or horizon that carries the image.
2. **Gesture** — the small action that makes it feel observed rather than staged.
3. **Distance** — close witness, medium candid, or distant solitary figure.
4. **Barrier** — glass, fog, rain, a doorway, mirror, seat, railing, foliage, or foreground blur.
5. **Light path** — window glow, reflected sunset, platform lights, wet road, sea glare, or pale sky.

Do not add a barrier merely as decoration. It must plausibly sit between camera and subject or define the viewpoint.

### 3. Choose One Composition Engine

Use one dominant engine and, at most, one supporting engine:

- **Portal view:** frame the scene through a window, doorway, vehicle interior, mirror, or architectural opening.
- **Distant witness:** keep the subject small against sea, sky, fog, hills, or infrastructure.
- **Foreground veil:** use a soft observer, seat, hand, glass reflection, spray, foliage, or bokeh to partially conceal the view.
- **Luminous path:** organize the frame around converging rails, road markings, train lights, reflections, or a bright horizon.
- **Quiet gesture:** center an unperformed action such as walking, reading, waiting, looking out, carrying flowers, or holding a mirror.

Composition must remain legible at thumbnail size. Keep one clear visual anchor even when much of the image is soft or dark.

### 4. Choose One Atmosphere Mode

- **Cool fog transit:** gray-teal air, low visibility, dark infrastructure, one line of amber light.
- **Storm witness:** cool neutral gray, sea spray, distant event, blurred foreground observers.
- **Warm cabin:** dark interior, softly clipped exterior window, tungsten skin and paper, intimate everyday action.
- **Pastoral memory:** muted olive slopes, cream clothing, rust or flower accent, long-lens softness.
- **Blue-hour portal:** cyan/slate exterior, dusty pink horizon, black framing, sparse warm points of light.

Read [references/style-language.md](references/style-language.md) when selecting composition, palette, optics, or subject scale.

### 5. Build the Edit or Generation Prompt

Write the scene truth before the style vocabulary. A prompt should state, in this order:

1. use case and image type;
2. subject, action, and setting;
3. protected source invariants;
4. composition engine and camera viewpoint;
5. atmosphere and lighting;
6. optical behavior and focus hierarchy;
7. palette and film texture;
8. exclusions.

Use [references/prompt-recipes.md](references/prompt-recipes.md) for templates, intensity modes, and personalization rules.

### 6. Preserve Reality During Edits

Unless the user asks for changes, preserve:

- identity and recognizable facial features;
- pose, gesture, body proportions, and gaze;
- clothing design and main colors;
- object count and important object completeness;
- architecture, terrain, perspective, and spatial relationships;
- the original moment and plausible physical lighting.

Style the photograph instead of redesigning its content. If a source has no natural portal or obstruction, prefer distance, leading lines, or negative space rather than fabricating a large window frame.

### 7. Apply Believable Optical Imperfection

Every soft effect needs a physical cause:

- foreground defocus from shooting past a nearby object;
- diffusion from mist, spray, rain, glass, or flare;
- shallow focus from a long lens;
- slight subject or camera motion;
- halation only around bright highlights;
- fine-to-medium film grain and gently reduced microcontrast.

Do not blur the entire image uniformly. Maintain a crisp-enough anchor, edge, light, or focus plane so the result still reads as a photograph.

### 8. Review and Refine Once

After generation, inspect the result and make one targeted revision when needed. Prioritize, in order:

1. subject and scene fidelity;
2. composition and subject scale;
3. natural depth and occlusion;
4. emotional light and color;
5. grain, halation, and surface texture.

## Non-Negotiable Style Rules

- Make the viewpoint feel inhabited: the camera is on a train, ferry, roadside, shore, room, or path—not floating nowhere.
- Favor candid backs, profiles, silhouettes, or partially obscured faces over fashion posing by default.
- Use negative space deliberately; it should create distance, weather, silence, or anticipation.
- Keep colors restrained. Reserve warm amber, rust, red, or cream as small emotional accents.
- Allow mild underexposure, clipped window light, motion, and imperfect focus when narratively useful.
- Keep people anatomically natural and environments physically coherent.
- Produce no watermark, username, platform badge, fake signature, decorative caption, or illegible text.

## Avoid

- a generic orange-and-teal preset with no compositional reason;
- HDR clarity, oversharpening, glossy commercial polish, or plastic skin;
- uniform heavy blur, excessive bloom, or grain that destroys the subject;
- cyberpunk neon, fantasy effects, surreal extra objects, or dramatic VFX unless requested;
- a centered large portrait when the scene calls for distance and observation;
- reproducing a reference photograph's exact person, location, arrangement, or branding.

## Completion Checklist

- Is there one readable anchor and one quiet narrative action?
- Does the camera have a plausible position and optical cause for softness?
- Is the composition doing more work than the filter?
- Are subject identity and scene geometry preserved where required?
- Are color and grain restrained enough to remain photographic?
- Is all unwanted text, branding, and watermarking absent?
