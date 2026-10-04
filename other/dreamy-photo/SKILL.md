---
name: dreamy-photo
description: Transform an existing user-provided image or photo into a premium dreamy motion-editorial image. Use only when the user asks for 图片梦幻化、照片梦幻化、把图片或照片变梦幻, or a semantically equivalent transformation of an existing image using haze, slow-shutter motion, soft focus, film texture, reflection, or restrained light bloom. By default, edit through the active platform's image-generation route and return the finished image using Codex image_gen, OpenClaw image_generate, or another explicitly available reference-image editing tool or image-capable model. Show prompts only when the user explicitly asks; if the user requests prompts only or says not to generate, return prompts without calling an image-generation route. Do not use for general image generation, article covers without a source image, ordinary retouching, or unrelated prompt writing.
---

# Dreamy Photo

Transform an existing image into a visibly re-composed dreamy motion-editorial photograph. Preserve a ranked semantic core, deliberately dissolve lower-priority detail, and let one primary physical mechanism control the frame's motion, light, and palette.

## Product Contract

- Require an existing source image. If none is available, ask the user to attach or provide the image and stop.
- Default to `generate-and-return`: build the prompt internally, call the active platform's supported image-generation route, and return the finished image.
- Before generation, show a compact process card with `照片诊断`, `构图提炼`, and `视觉方案`, then write `质量检查通过，开始生成：`. Use equivalent labels in the user's language when appropriate.
- Do not show the internal prompt, negative prompt, preflight scorecard, or hidden rendering constraints by default.
- If the user explicitly asks to see the prompt, generate the image and also show the requested prompt material.
- If the user explicitly asks for prompts only, or says not to generate an image, return the prompt package and do not call any image-generation route.
- Keep the default reply compact: the image plus one short sentence naming the chosen direction and strength.
- Honor any narrower user constraint on identity, composition, aspect ratio, text, or output location.

## Platform Tool Routing

Detect the current platform and available image capability before generation. Keep the art-direction and QA workflow identical; adapt only the final tool call.

- **Codex:** call the built-in `image_gen` tool. For a local source, pass `referenced_image_paths`. For an image available only in the conversation, use `num_last_images_to_include` with the smallest count that includes it. Never provide both input mechanisms.
- **OpenClaw:** call the built-in `image_generate` tool and pass the source photo through its reference-image `image` parameter. Use the configured image-generation model; do not fall back to a text-only model.
- **Other compatible agents:** generate only when the selected model or tool explicitly supports image output and reference-image editing. Adapt to documented parameters rather than inventing a tool name or schema.
- **No compatible image route:** tell the user that the current model or environment cannot generate the edited image. Offer the prompt package or ask them to switch to an image-capable model; do not claim that an image was generated.

Put the desired ratio, preservation constraints, and art direction in the prompt unless the active tool documents corresponding parameters.

## Core Art Direction

Default to `semantic-core`, not full-scene fidelity.

- Write a ranked preservation priority plus short Keep / Fade / Remove lists before prompting.
- Keep only two to four hero-critical items in `dream-haze`: one hero or structural path, one essential gesture/object/rhythm, one defining relation or perspective cue, and at most one identity color.
- When people carry the emotion, treat their identity, count, anatomy, pose, relationship, clothing, and essential shared object as the invariants. Do not promote scenery, landmarks, background architecture, or the source crop to invariants unless the user explicitly asks.
- When any human skin is visible, lock its source-relative complexion lightness, undertone, age impression, and softness as identity invariants. Re-author the environment palette around the skin; do not darken, tan, redden, gray, age, or coarsen the person to match the new grade.
- Lock a **hero exposure floor** for every hero type. For people, preserve source-relative skin brightness plus readable light- and dark-garment planes unless silhouette is source-supported or requested. For objects, flowers, structures, and landscapes, preserve one source-relative midtone or material plane so the anchor does not become a crisp but unreadable dark cutout. Backlight may rim the hero but must not underexpose it to manufacture mood.
- Preserve product geometry, labels, architecture, or landscape silhouette only when that object, structure, or landscape is itself the hero or the user requests documentary fidelity.
- Turn selected secondary forms into two to four broad directional motion or color masses. A Fade element must lose small-detail readability: windows, branches, leaves, signs, distant structures, and textures may retain direction and mass but not crisp contours or grids.
- Keep bokeh, light leaks, negative space, and reflected highlights optically irregular, amorphous, and non-semantic. Phrase this positively in generation prompts; do not enumerate forbidden icon names because lexical priming can cause the model to draw them. Reserve named examples for result QA only.
- Define a **hero sharpness island** before designing motion: the hero silhouette, face or gesture, product body, structural path, or other semantic anchor plus a small safety margin. Preserve its defining contours and one appropriate material texture. For human skin, clarity means anatomy and gesture—not extra pores, wrinkles, veins, age spots, or gritty micro-contrast. Motion may frame, pass behind, or originate beside this island, but must not wash across it.
- Maintain a sharpness hierarchy: one readable anchor inside the hero sharpness island, atmospheric softness around it, then directional motion in secondary or peripheral layers. `45% kinetic atmosphere` describes visual weight, not permission to blur 45% of every subject.
- Permit reframing, aspect-ratio changes, hero enlargement, edge cropping, and background reconstruction unless the user requests `identity-lock`, the original ratio, or documentary fidelity. Choose the ratio from the hero's dominant spatial axis: horizontal subjects may remain landscape, vertical subjects may use portrait, and balanced subjects may preserve the source ratio. Never force 4:5 merely because a wide source contains a small hero.
- For an unqualified request to dreamify a photo, default to `dream-haze`. The transformation must be visibly stronger than a warm color grade or global soft-focus filter, and its dominant palette must be visibly re-authored rather than left at the source white balance. Diagnose mood and palette separately from lighting; backlight does not automatically mean honey-gold, sunset, memory, or nostalgia.
- Translate a named artist or Pinterest reference into transferable visual principles; do not imitate a named living artist or one creator.

## Strategy Axes

Use the axes below as diagnostic evidence, not as equal-strength effects. Read `references/style-system.md` only when the source is ambiguous, the user names a visual direction, or the normal rules do not identify a credible route.

1. **Fidelity**
   - `semantic-core`
   - `identity-lock`
   - `experimental-abstraction`
2. **Composition**
   - `source-led-asymmetry`
   - `geometry-preserving-frame`
   - `low-angle-color-field`
3. **Motion**
   - `crowd-drift`
   - `passing-gesture`
   - `source-layer-drift`
4. **Optical layer**
   - `none`
   - `floral-diffusion`
   - `glass-memory`
5. **Lighting**
   - `source-light-bloom`
   - `backlit-halation`
   - `night-color-glow`
6. **Strength**
   - `restrained-premium`
   - `dream-haze`
   - `experimental-memory`
7. **Mood / palette**
   - `source-led`
   - `summer-breeze`
   - `golden-memory`
   - `blue-hour`
   - `night-solitude`
   - user-specified direction
8. **Hero spatial axis**
   - `horizontal`
   - `vertical`
   - `balanced`

After diagnosing the axes, name exactly one **primary mechanism** and at most one **support mechanism**. The primary mechanism must create most of the visible transformation; the support mechanism only deepens it. Do not let a conservative axis fallback override a stronger source-supported art direction. A low-angle composition may diagnose source-layer drift, glass memory, and backlit halation, but the final brief still declares one dominant mechanism and no more than one support.

## Workflow

1. **Resolve intent and source.** Determine whether the user wants the default generated image, generated image plus visible prompts, or prompts only. Confirm that a source image is available.
2. **Inspect the source visually.** For a local image, load it with `view_image` before editing. Identify the hero, invariants, pose, light, depth, reflective or floral assets, plausible motion, native colors, structural risks, and—when skin is visible—the observed complexion lightness, undertone, age impression, and texture softness.
3. **Rank the semantic core and draw the sharpness boundary.** Write a descending preservation priority, then Keep / Fade / Remove. Define the hero sharpness island and the zones where motion is permitted. Apply the counterfactual test: if changing an element changes who the hero is or what the essential relationship/action/path is, keep it; if it only identifies the location, fade it; if it is tiny clutter, remove it. Do not protect all visible geometry equally, but do not place hero-surface texture in Fade.
4. **Choose the art direction, mood, and crop.** Diagnose fidelity, composition, motion, optical, lighting, mood or palette, hero spatial axis, and strength; then choose one primary mechanism and at most one support mechanism. Prefer source-supported features over invented objects, but permit implied movement from a corridor, walkway, repeated lights, or public passage without inventing people. Treat passage architecture and standalone structures differently. Change ratio only when the chosen portrait, landscape, or balanced crop improves hierarchy without clipping the hero's defining direction.
5. **Use the helper when useful.** Convert observed traits into a structured recommendation:

   ```bash
   python3 scripts/analyze_photo.py --subject portrait --light backlit --motion walking --depth layered --background street --mood source-led --subject-axis vertical --strength dream-haze --json
   ```

   The helper analyzes supplied observations; it does not inspect pixels and never replaces visual judgment.
6. **Build the internal prompt.** Use the order below. Read `references/prompt-recipes.md` only when the user asks to see prompts, the source has recognition-sensitive people, text, products, or architecture, or a worked pattern is needed.

   `ranked source invariants → skin identity lock when applicable → hero sharpness island and motion boundary → Keep/Fade/Remove → composition and ratio → three-layer motion → primary/support mechanisms → light → palette reconstruction → analog texture → emotional tone → rendering constraints`
7. **Run preflight QA.** Fix any zero-score preservation, skin identity, hero exposure, semantic compression, physical motivation, palette reconstruction, Fade destruction, transformation visibility, hero-island sharpness, semantic-light invention, or other invention risk before generation. Reject a prompt that protects more background than hero semantics, lets motion cross the hero sharpness island, applies the environment grade directly to skin, crushes a readable hero into an unreadable silhouette without a source or user reason, allows recognizable icon-like bokeh, enumerates forbidden symbol names in the generation brief, leaves the source white balance essentially unchanged outside protected skin, or describes `dream-haze` mainly with weak modifiers such as `subtle`, `gentle`, or `mild`. Read `references/quality-rubric.md` for recognition-sensitive sources, complex geometry, or any failed first result.
8. **Honor prompt-only intent.** If the user explicitly requested prompts only or no generation, return the requested prompt package and stop.
9. **Show the process card.** Before calling the active image-generation route, present the observed hero, preservation set, usable light/motion/foreground, risks, Keep/Fade/Remove decisions, skin identity lock when applicable, hero exposure floor, hero sharpness island, motion boundary, motion and quiet-space targets, three depth treatments when supported, hero scale and placement, primary and support mechanisms, light, color, optical texture, mood, output ratio, strength, ranked fidelity priority, and a short physical reason. End with `质量检查通过，开始生成：`. Keep each field to one compact line; omit inapplicable optional fields rather than exposing a long checklist. This is an art-direction summary, not the generation prompt.
10. **Generate through the platform route.** Follow `Platform Tool Routing`: use Codex `image_gen`, OpenClaw `image_generate`, or another explicitly available reference-image editing route. Put the desired aspect ratio and preservation constraints in the prompt instead of inventing unsupported tool parameters.
11. **Inspect the result.** Compare the generated image with the source against the result gates in `references/quality-rubric.md`. In `dream-haze`, treat source-like color, readable Fade elements, a near-literal full-scene reconstruction, uniform softness, or tiny decorative streaks as hard failures. If the result has a hard failure, make one targeted revision through the same active image-generation route, then check again.
12. **Return the deliverable.** Render the final image. Show prompts only if the user explicitly requested them. Report a saved path only when the user named a destination or the image is project-bound.

## Visual Allocation

Treat these as approximate, non-overlapping visual shares rather than precise geometry:

- `identity-lock`: hero 45%, kinetic atmosphere 25%, quiet space 30%.
- `restrained-premium`: hero 40%, kinetic atmosphere 30%, quiet space 30%.
- `dream-haze`: hero 30%, kinetic atmosphere 45%, quiet space 25%.
- `experimental-memory`: hero 20%, kinetic atmosphere 65%, quiet space 15%.

Use `identity-lock` allocation whenever recognition or geometry preservation overrides the requested strength.

## Selection Rules

- Use `crowd-drift` when visible people, walking, traffic, or the implied movement of an empty public corridor, walkway, platform, bridge, or repeated perspective-light sequence makes slow-shutter flow plausible. Implied movement changes existing light and structure into trails; it never adds people.
- Use `passing-gesture` only with a real nearby hand, fabric, hair, paper, foliage, or light edge.
- Use `source-layer-drift` as the safe motion fallback: stretch existing background edges, color, light, or architecture without inventing new objects.
- Use `floral-diffusion` only when flora exists or is explicitly requested.
- Use `glass-memory` only when a reflection, window, mirror, or believable glass surface exists.
- Use `backlit-halation` with existing backlight, hard sun, window light, rim light, a credible bright sky opening, or visible practical fixtures such as path, edge, or ground lamps. The visible fixture may be the luminous source even when it is not behind a person.
- Use `geometry-preserving-frame` only when a product, structure, label, or landscape is the actual hero, or when the user requests documentary fidelity. For architecture, classify the hero as a passage, standalone structure, or background context before defining invariants; only passage architecture inherits a path and vanishing-point priority. Do not choose it merely because a people photo contains mountains or buildings.
- Use `low-angle-color-field` only when the source viewpoint and open sky or wall can support it without anatomy distortion.
- Use `source-led-asymmetry` for emotional people photos by default. Preserve relative body positions while allowing a new crop, larger hero scale, or a different output ratio.
- Default a simple `梦幻化` request to `dream-haze`; reserve `restrained-premium` for explicit subtlety, products, brands, architecture, or identity-lock work.
- In `dream-haze`, make directional atmosphere visibly occupy about 45% of the visual weight. Do not weaken the main motion effect with repeated `subtle`, `gentle`, `mild`, or `restrained` wording.
- Keep the primary subject materially readable. For a path or bridge hero, preserve the central walking surface, inner railing boundaries, fixture cores, and one continuous lamp rhythm; keep motion outside that corridor or behind it. For a standalone structure, preserve its defining silhouette, structural midtones, and one material plane without inventing a vanishing path. For a person, protect the full body or relationship silhouette, not only the face.
- Local halation expands around a light source while its luminous core remains legible. Do not turn every lamp, face, hand, structural edge, or hero surface into a smear merely because the strength is `dream-haze`.
- Isolate human skin from the environment grade. Preserve the source's perceived complexion brightness and undertone even under blue, amber, or colored night light. Keep skin softly photographic; never use sharpening language that increases pores, wrinkles, veins, creases, or apparent age.
- Preserve subject exposure independently from background atmosphere. Unless silhouette is source-supported or explicitly requested, keep visible skin and key light/dark garment planes tonally readable; do not crush the hero to near-black to intensify backlight.
- Treat light as optical energy, not decoration. In generation prompts, ask only for asymmetrical, irregular, amorphous, non-semantic optical forms physically tied to source lights. Do not name forbidden symbols. If a result invents one, target revisions by location, color, and geometry rather than repeating its semantic name.

## Prompt Visibility

### Default

Before generation, return the process card in this order:

1. `照片诊断`: subject, must preserve, usable light/motion/foreground, risks;
2. `构图提炼`: Keep, Fade, Remove, skin identity lock when applicable, hero sharpness island, motion boundary, motion coverage, quiet space, foreground sweep, midground drag, background light/color flow, hero share and placement;
3. `视觉方案`: primary mechanism, support mechanism when useful, strength, reason;
4. `质量检查通过，开始生成：`.

After generation, return:

- the generated image;
- one short sentence naming the strategy and strength;
- a saved path only when relevant.

Do not include the full prompt, negative prompt, preflight scorecard, or long parameter block.

### When the user asks to see prompts

Add only the requested items from:

- Chinese image-to-image prompt;
- English image-to-image prompt;
- negative prompt;
- preservation constraints;
- aspect-ratio and strength guidance.

### When the user asks for prompts only

Return the prompt package without calling an image-generation route. Do not attach a placeholder image.

## Failure Modes

Reject or revise a prompt or result that:

- changes the hero's identity, body structure, pose, relationship, product geometry, or label;
- changes source-relative skin lightness, undertone, perceived ethnicity, or age impression; or increases wrinkles, veins, pores, creases, spots, and coarse texture;
- turns a source-readable person into a featureless or near-black silhouette, loses the light garment identity, or removes tonal separation between skin, clothing, and the surrounding shadow without an explicit silhouette request;
- preserves every background object with equal clarity;
- gives every visible structure equal preservation priority instead of ranking the few hero-critical cues;
- leaves Fade elements readable as window grids, building outlines, individual branches, leaves, signs, or surface texture;
- preserves the source crop, aspect ratio, hero scale, and full background by default when a stronger reframe would improve editorial hierarchy;
- looks like the original scene with only warmer color, lower contrast, global softness, or a generic film filter;
- leaves the dominant color balance essentially unchanged in `dream-haze` instead of visibly rebuilding the selected mood-appropriate palette family;
- produces a static empty background with no directional atmosphere;
- erases every secondary form instead of transforming selected forms;
- applies uniform blur to the whole image;
- lets directional blur, light trails, diffusion, or halation cross and soften the hero sharpness island;
- preserves the hero's rough geometry but erases its defining contour, repeated rhythm, or one readable material texture;
- interprets `sharpness` as high-definition human skin texture instead of clear anatomy with soft natural skin rendering;
- invents flowers, glass, people, clothing, jewelry, props, or text;
- invents heart-shaped bokeh, stars, wings, halos, butterflies, letters, logos, or other semantic light and negative-space symbols;
- uses unexplained magical haze, global white fog, plastic skin, extreme teal-orange grading, or generic social-media filtering;
- stacks incompatible effects or lets typography cover the hero.

## Resource Map

- Read `references/style-system.md` only for ambiguous routing, named visual directions, or deeper color and strength guidance.
- Read `references/prompt-recipes.md` only for visible prompt requests, recognition-sensitive sources, or matching worked examples.
- Read `references/quality-rubric.md` for high-risk identity or geometry, detailed preflight, or targeted revision after a failed result.
- Run `scripts/analyze_photo.py` when structured route recommendations improve consistency.
