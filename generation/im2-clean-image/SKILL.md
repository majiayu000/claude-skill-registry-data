---
name: im2-clean-image
description: "Default material, information-density hierarchy, clean-rendering, negative-prompt hygiene, and evidence-preserving photo-repair layer for IM2 / GPT Image 2 / gpt-image-2 / image_gen. Use for clean generation/redraws, artifact cleanup, focal-detail control, atmospheric depth, physically coherent light paths, air scattering, volumetric light, light ratio, material realism, architecture/terrain/hard-surface scene mass and structural grounding, and 企业/公司活动/门店/团队合影/商品/餐饮/证件文档照片修复. Preserve identity, headcount, placement, product facts, text, logo, QR, date, price, and scene evidence; prefer residual blur over invented restoration detail."
---

# IM2 Clean Image

## Purpose

Apply this as the default finalization layer before any IM2 / gpt-image-2 image prompt. The layer has four inseparable parts:

1. **Material-light layer:** make the image physically believable through hero surfaces, surface response, lighting, exposure, and material separation.
2. **Information-density layer:** protect large calm masses, concentrate fine structure at the focal mechanism, and let nonessential information fall away across depth.
3. **Clean anti-artifact layer:** keep those materials clean and controlled so detail does not turn into dirty latent residue.
4. **Negative-prompt hygiene layer:** keep avoid words targeted and non-contaminating; never let the negative slot become a memory of old failures or a list of concepts that accidentally summon themselves.

Keep the user's subject, composition, style, and mood. Do not simplify the idea just to make it clean. Do not rely on generic `8K`, `high resolution`, `ultra realistic`, or `sharp details` as substitutes for material physics.

## Default Prompt Order

Build IM2 prompts in this order:

1. Subject, identity, pose, action, and setting. Add aspect ratio here only when the target adapter's official syntax requires it as a prompt token; otherwise keep it in invocation/settings.
2. Style or medium, if the user requested one.
3. **Camera, composition, and hierarchy scaffold:** lock camera/spatial relations, visual thesis, dominant masses, focal route, and quiet zones.
4. **Light path and material layer:** source-medium-receiver relations when relevant, then hero surfaces, surface response, exposure, contact shadows, and optics.
5. **Distance and information-density falloff:** reserve fine structure for the focal mechanism and state how support, quiet, and depth zones lose nonessential information.
6. **Controlled-detail clean layer:** clean rendering, selective detail, natural texture only, controlled highlights, minimal repeated patterns.
7. **Negative hygiene layer:** compact targeted avoid block for broad artifact, style-drift, anatomy/structure, and fake-material failures.

## Required Material-Light Pass

Before adding the anti-dirty phrases, add a compact material layer that answers the following. Keep it proportional: a simple portrait may need one sentence; a complex vehicle, product, fantasy scene, or action still may need several.

- **Hero surfaces:** name the main visible materials: skin, hair, fabric, leather, metal, glass, ceramic, wet ground, dust, smoke, paper, plastic, foliage, etc.
- **Surface response:** define matte, satin, glossy, translucent, rough, worn, wet, dry, dusty, scratched, reflective, or absorbing areas.
- **Light behavior:** define key light direction and color temperature; add rim, bounce, practical, or grazing light only when useful.
- **Material separation:** if surfaces share one color, separate them by value, temperature, roughness, highlight width, edge response, translucency, contact shadows, and depth contrast, not random new colors.
- **Exposure architecture:** protect highlight texture, smooth highlight rolloff, readable shadow floor, and intended accent color without clipping.
- **Grounding:** use localized AO/contact shadows only in true seams, overlaps, creases, and contact zones; avoid dirty AO halos.
- **Optics:** choose restrained depth of field, lens diffusion, reflection, motion blur, or atmosphere only when it supports the image.

Material sentence skeleton:

```text
The [hero material] shows [physical behavior] under [lighting condition], with [local imperfections/topology] visible at [camera scale]; [specific areas] remain [matte/dry/absorbing] while [specific edges/surfaces] catch [soft/sharp/specular/anisotropic] highlights.
```

Universal material quality block:

```text
physically distinct material classes, protected highlight texture, smooth cinematic highlight rolloff, readable shadow-side structure, localized contact shadows, distance- and roughness-correct reflections, motivated grazing light, restrained atmosphere, subtle finishing
```

## Real-Scene Light-Path and Atmospheric-Medium Pass

Use this pass for photographic, architectural, landscape, interior, industrial, wet-weather, or otherwise real-world scenes, especially when the user asks for 光比、质感、空气散射、空气透视、雾、湿气、粉尘、烟、体积光、光柱、丁达尔效应、逆光、晨光 or 暮光.

Treat semantic accuracy and aesthetic selection as separate control surfaces:

- Keep subject identity, count, geometry, camera, spatial relations, source position, and physical cause/effect explicit and stable.
- Spend aesthetic freedom on the visual thesis, dominant masses, focal route, light ratio, color relation, atmospheric depth, material response, and intentional information loss.
- Never make isolated patches prettier by breaking the shared light path, perspective, reflection geometry, or wet/dry boundary.

Compile one observable light chain before writing mood language:

```text
source position and size -> aperture/occluder when present -> participating medium -> first receiving surface -> cast-shadow direction -> bounce/reflection path -> exposure limits
```

Lock one dominant source first. Add supporting skylight, bounce, or practicals only when each has a distinct job and does not flatten the hierarchy. Wall light patches, water or floor reflections, rim light, volumetric visibility, and cast shadows must agree with the same source geometry.

Air scattering is physically present but not always visibly dramatic. Stage atmospheric perspective through extinction plus environmental-light in-scattering: distant layers usually lose contrast, chroma, edge definition, and internal structure, tending toward the visible atmospheric-light color only when conditions support it. Do not automatically turn every distance layer pale blue.

Volumetric light is conditional, not a default decoration. Require a participating medium such as localized mist, humidity, salt dust, smoke, steam, pollen, or suspended spray plus a useful source/viewing geometry. An aperture or occluder is optional for scattering itself but normally required for a sharply bounded shaft. Let medium density follow its physical source and spatial falloff; make visible scattering strongest where that medium intersects the illuminated path under a favorable viewing angle. Do not fill the whole frame with uniform fog. Solid objects must interrupt the illuminated path, while visible beam contrast changes according to extinction, source divergence, medium density, viewing angle, and exposure before the light terminates on or passes across credible receivers.

For the full compilation procedure, prompt modules, and output checks, read `references/real-scene-light-atmosphere.md`.

## Information-Density Hierarchy and Controlled Information Loss

Treat uniform detail density as a structural failure, not a request for global blur. Before adding texture language, assign every major region one role:

- **Focal zone:** keep the highest edge contrast, most complete contours, and the few meaningful fine details needed to read identity, action, contact, or the hero material.
- **Support zone:** use medium-size shapes and only enough internal structure to explain space, balance, or narrative context.
- **Quiet / depth zone:** organize broad color or value masses; reduce small-shape count, texture frequency, edge contrast, and contour completeness. Let selected forms merge into light, haze, shadow, or neighboring color.

Use atmospheric perspective as staged information loss: distant layers become progressively lower-contrast, softer-edged, simpler, and partly obscured. Reduce chroma when haze or scattered light is visible; otherwise preserve the hue family while reducing edge contrast and internal structure. Keep enough landmark silhouette or overlap to preserve depth; do not sharpen every mountain, building, tree, cloud, or river valley merely because it exists.

Build the image from large masses to small accents:

1. Lock 3–7 dominant shape groups and at least one continuous calm area before describing local texture.
2. Name one or two focal mechanisms; concentrate fine lines and texture there.
3. State explicitly how information decreases across space or away from the focal mechanism.
4. Add material texture only where camera scale, light, and narrative importance can reveal it.

Acceptance check at thumbnail size:

- one clear high-information cluster is visible;
- at least one broad quiet mass survives without filler texture;
- background edge frequency and contrast are lower than the focal zone;
- the scene reads as intentionally selective, not uniformly sharp and not globally blurred.

Practical prompt block:

```text
clear information-density hierarchy, large calm shape masses first, fine detail concentrated at [focal mechanism], supporting forms simplified, non-focal contours selectively incomplete, distant layers progressively lower-contrast and softer, becoming paler only where haze or scattered light supports it, selected background forms dissolving into haze/light/shadow, intentional loss of nonessential information while the hero silhouette remains readable
```

## Default IM2 Clean Workflow

1. Lock the user's intent. When a source image exists, receive the approved edit/rebuild classification from `$constraint-input-router` if that optional companion Skill is installed; otherwise use the local classification fallback below.
2. Compile the image transaction before descriptive styling: one principal `CHANGE`, source-proved facts to `PRESERVE EXACTLY`, and the regions/relations that must `REBUILD` because of the change.
3. For architecture, interiors, terrain, megastructures, or hard-surface scenes where scale, structural weight, opening depth, support, overlap, or grounded mass matters, read `references/heavy-scene-structure-and-mass.md`. Build its structure lock before styling and use its output-inspection loop after generation.
4. For real-world scenes or any request involving light ratio, atmosphere, scattering, fog, dust, steam, smoke, humidity, backlight, or volumetric light, compile the source-medium-receiver chain in `references/real-scene-light-atmosphere.md` before adding mood language.
5. Add the material-light layer first. Clean images still need physical material behavior; otherwise they become flat, plastic, or posterized.
6. Build the information-density hierarchy. Lock focal, support, and quiet/depth zones; require large calm masses and explicit falloff of nonessential information before adding texture.
7. Scan for dirty-risk wording. Treat these as risk signals: `ultra detailed`, `hyper detailed`, `insanely detailed`, `micro detail everywhere`, `highly textured`, `wet glossy`, `cinematic bokeh everywhere`, dense dark background, busy fantasy architecture, ink/oil hybrid, character sheet, repeated ornaments, or many small marks.
8. Replace risky detail language. Prefer controlled detail phrases instead of stacking more detail.
9. Add the clean rendering layer after material language and density hierarchy.
10. Build the avoid block with negative hygiene. Keep it short, targeted, and current-risk based.
11. Use clean-slate regeneration for dirty outputs. If an output already has ghost texture, dark watermark feel, hidden marks, or low-contrast residue, rewrite and regenerate cleanly. Avoid repeated image-to-image cleanup unless the user explicitly asks, because iterative passes often amplify latent grime.

## Image Edit Transaction Compiler

Use this only when a source image is being edited or used as the base of a reconstruction:

If `$constraint-input-router` is unavailable, classify locally before writing the transaction:

- **EDIT:** the requested change is bounded and the camera, crop, subject count, topology, major placement, and untouched regions can remain stable.
- **REBUILD:** the request changes viewpoint, framing, major geometry, topology, pose, occlusion, environment completion, or relationships that force coupled regions to be recalculated.
- **MIXED:** name one principal `CHANGE`, preserve only source-proved invariants, and list every coupled region under `REBUILD`. Route exact local pixels, registered text/layout, or measurable geometry to masks, deterministic reconstruction, comparison, compositing, or 3D rather than relying on generative preservation.

```text
CHANGE:
[one principal visible change]

PRESERVE EXACTLY:
[source-proved identity, count, copy, logo, product geometry, placement, palette/material relation, or other approved invariants]

REBUILD:
[regions and coupled relations that must be recalculated: new visible surfaces, perspective, occlusion, edges, contact shadows, reflections, background completion]
```

`PRESERVE EXACTLY` is a target and acceptance contract, not a claim of pixel-perfect generative control. Route exact text, logos, UI, signatures, registered layouts, or local pixel preservation to masks, deterministic reconstruction, compositing, or comparison when needed.

If the view changes, make the new arrangement visible in the transaction: subject scale, left/right occupancy, depth layer, body/object orientation, occlusion, landmark relation, and newly exposed surfaces. Do not preserve the old composition and request an incompatible new view in the same contract.

Keep model/platform controls—dimensions, UI switches, sampling, reference weights, seeds, upload handles, and output format—in the invocation/settings layer unless the target adapter officially requires a prompt token. They are not image content.

## Negative-Prompt Hygiene

Use this layer every time an IM2 prompt includes an `Avoid`, `Negative prompt`, or `no ...` list.

Core rule: **the negative slot is not a memory of old failures.** It is only a compact constraint slot for likely broad failure classes that cannot be expressed better as positive visible facts.

1. Positive lock first. Before writing `no X`, ask what should visibly appear instead.
2. Keep negatives broad and reusable: artifact classes, extra-body/extra-object failures, style drift, text/watermark, material fake-look, composition clutter.
3. Do not name old failed props, characters, locations, colors, actions, or styles in the negative block. Old-specific negatives can contaminate the new image.
4. Avoid denied nouns that are not part of the target shot. If the forbidden object is not already likely, describing it may summon it.
5. Keep essential negatives in the constraint slot only, never scattered through the positive prompt.
6. Prefer one compact line over a long laundry list. Too many negatives dilute the positive image and create associations.

Safe default avoid block:

```text
Avoid: dirty texture buildup, random micro-pattern noise, hidden watermark-like marks, ghost texture, latent artifacts, muddy shadows, noisy bokeh, low-contrast residual textures, over-sharpened grime, uniform plastic gloss, pasted-on texture, milky reflections, clipped highlights, crushed blacks, dirty AO halos, malformed anatomy when people are present, stray text or logo unless requested.
```

Use narrower blocks when possible:

```text
Avoid: ghost texture, latent artifacts, hidden watermark-like marks, repeated micro-pattern noise, muddy shadows, noisy bokeh, pasted-on texture.
```

## Default Add-ons

Full cleanup add-on:

```text
clean rendering, clear focal/support/quiet detail hierarchy, selective focal detail, broad calm masses, realistic detail only, natural texture only, controlled material rendering, clean gradients, soft diffused lighting, controlled highlights, subtle reflections only, matte or natural surfaces, organized low-frequency background with selectively softened depth layers, minimal repetitive patterns, no watermark, no signature, no ghost texture, no latent artifacts, no repetitive micro-pattern noise, no hidden marks, no low-contrast residual textures
```

Short cleanup add-on for tight prompts:

```text
clean rendering, clear focal/support/quiet detail hierarchy, selective focal detail, broad calm masses, realistic detail only, natural texture only, controlled highlights, organized low-frequency background with selectively softened depth layers, minimal repetitive patterns, no watermark, no ghost texture, no latent artifacts, no low-contrast residual textures
```

## Risky Phrase Replacements

Use these substitutions before adding more prompt length:

| Replace | With |
|---|---|
| `ultra detailed` | `clear focal/support/quiet detail hierarchy` |
| `hyper detailed` | `selective fine detail` |
| `insanely detailed` | `realistic detail only` |
| `micro detail everywhere` | `detail concentrated only on meaningful surfaces` |
| `highly textured rendering` | `controlled material rendering` |
| `wet glossy` | `subtle reflections with strict wet/dry boundaries` |
| `glossy reflective` | `controlled highlights and roughness-correct reflections` |
| `cinematic bokeh background` | `organized low-frequency background with selectively softened depth layers` |
| `dark atmospheric background` | `smooth dark tones with low texture background` |
| `beautiful lighting` | `motivated key light, controlled bounce, protected highlight texture` |
| `realistic texture` | `physically distinct material response with natural texture only` |
| `no blur` | `sharp hero silhouette with clean intentional depth of field` |
| `no clutter` | `clean negative space and organized background shapes` |
| `no extra people` | `single clearly framed subject, empty surrounding space` |
| `no weapon` | `empty relaxed hands visible, no held objects` only when weapons are already likely |

## Conditional Material Modules

Add only the modules that match the image:

- Faces / portraits: `natural facial planes, matte skin with soft specular highlights, subtle pores and peach fuzz only where visible, clean eye highlights, no waxy gloss, no dirty pore noise`.
- Fabric / clothing: `geometry-aware weave or knit structure, fibers following folds, grazing light revealing raised texture, no flat printed texture`.
- Metal / weapons / machinery: `roughness variation, worn edges catching narrow anisotropic highlights, oxidized or matte flats absorbing light, no uniform chrome gloss`.
- Glass / water / glossy product: `strict reflection boundaries, distance- and roughness-correct reflections, transparent or glossy surfaces only where physically motivated, no milky global mirror floor`.
- Stained glass / mosaic / repeated-unit physical media: treat the reference as a medium-and-light anchor, not a mandate for uniform texture density. Lock a coarse-to-fine unit hierarchy: broad quiet panes dominate, medium panes support structure, and small panes/lead intersections appear only near the focal mechanism. Keep shadow panes low-frequency rather than sterile-flat: selected broad panes may retain slow clouding, uneven pigment density, faint flow lines, age bloom, and handmade thickness variation. Confine sharper bubbles, striations, patina, crackle, grout, stitching, oxidation, or other craft irregularities to selected lit units and structural seams. Preserve clean negative space and simplified architectural silhouettes; never cover the whole frame with equally dense lead lines, mottling, micro-windows, or repeated cells. Clean means controlled patina with clear ownership, not polished plastic, flat vector color, or the total removal of material evidence.
- Stone / ceramic / architecture: `matte porous response, chipped or worn edges only where exposed, contact shadows in seams, no random dirty speckle`.
- Wet street / rain: `strict dry/wet boundaries, dry asphalt stays dark and absorbing, shallow puddles carry controlled specular reflections, no global wetness`.
- Dark or black backgrounds: `smooth dark tones, readable shadow floor, clean value separation, low texture background, controlled rim light, no noisy bokeh`.
- Fantasy / dense concept art: `large readable shape groups, one or two focal detail clusters, continuous calm masses, distant terrain simplified and partly dissolved by atmospheric perspective, no repeated micro ornaments`.
- Ink, oil, painterly, NPR: `intentional brush edges, clean negative space, controlled pigment texture, readable silhouette, no random speckle, no muddy texture buildup`.
- Products / posters / covers: `clean silhouette, protected logo/text area, polished spacing, smooth gradients, realistic detail only on hero surface, premium clean finish`.

## Output Shape

For prompt rewrites, return:

```text
Prompt:
[subject/style/composition]
[material-light layer]
[controlled-detail clean layer]

Avoid:
[targeted negative block]
```

For diagnosis or iteration, return:

```text
Material + dirty-risk + negative diagnosis:
- Missing material controls:
- Risk words:
- Negative contamination risk:
- Risk surfaces/background:
- Cleanup strategy:

Rewritten IM2 prompt:
...

Avoid:
...
```

## References

- Read `references/clean-prompt-recipes.md` when doing a substantial IM2 prompt rewrite, building a prompt batch, diagnosing a dirty output, or adapting the material-clean layer to portraits, dark scenes, fantasy scenes, posters, or product images.
- Read `references/negative-prompt-hygiene.md` when a request includes a negative prompt, many `no ...` constraints, a failed-output retry, old project contamination, or any prompt where denied words may summon unwanted content.
- Read `references/evidence-preserving-photo-restoration.md` when repairing documentary, company, event, store, team, product, food, social, or evidence/document photos where factual preservation matters more than beautification.
- Read `references/heavy-scene-structure-and-mass.md` for architecture, interiors, terrain, megastructures, or hard-surface scenes that need explicit structure locks, believable mass, grounded support, output-based acceptance, or a recorded single-variable retry loop.
- Read `references/real-scene-light-atmosphere.md` for photographic or physically grounded scenes that need strong light ratio, coherent source/receiver geometry, air scattering, atmospheric perspective, fog/humidity/dust/smoke/steam, volumetric light, wet-surface reflections, or a light-path failure diagnosis.
