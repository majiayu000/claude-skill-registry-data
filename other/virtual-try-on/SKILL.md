---
name: virtual-try-on
description: Put one supplied garment on a supplied person or suitable generated model, or replace clothing already worn, while preserving garment construction, material, color, pattern, branding, person identity, pose, unaffected clothing, and the requested scene. Use for virtual try-on, clothes changing, garment-to-model visualization, and e-commerce outfit previews; do not use for outfit invention, pose-only changes, model replacement, multi-garment styling, footwear-only try-on, or physical fit guarantees.
---

# Virtual Try-On

Execute one garment-to-person transformation with a model-plus-Prompt route. Treat `virtualtryon` and `ai-clothes-changer` as optional API implementations, not as the Skill identity.

## Catalog

- Display name: Virtual Try-On
- Categories: Fashion, Commercial Production
- Status: Ready
- Featured: yes
- Route label: GPT Image 2 with capability-matched fallbacks
- Tone: violet
- Short description: Try on or replace a garment with fidelity checks.

- Similar skills: change-pose, fashion-model-replacement
## What this skill does

- Supports scene-aware try-on and person-plus-garment clothes replacement.
- Preflights garment visibility, pose, occlusion, crop, source roles, and scene requirements.
- Starts with GPT Image 2 for best overall quality and uses another route only for a concrete capability, availability, speed, or cost reason.
- Checks garment fidelity, person continuity, dressing plausibility, anatomy, occlusion, scene, and composition before delivery.

## How to use

Attach one person and one garment image, or one garment image for a generated model. A location image is optional only for scene-aware try-on. State any details that must remain unchanged.

#### Try a garment on a model

```text
Put this navy jacket on the supplied model and keep the model, pose, and studio background unchanged.
```

#### Create an on-model garment preview

```text
Create one clean on-model preview of this dress using a suitable generated fashion model.
```

#### Use a location reference

```text
Put this coat on the supplied model and use the attached concrete gallery as the location.
```

#### Replace worn clothing

```text
Replace the model's current top with this supplied shirt and keep the person, pose, trousers, and background unchanged.
```

## Workflow

### 1. Assign source roles and mode

```yaml
mode: scene-aware-try-on | clothes-change
person: optional only when a suitable model should be generated
garment: required
location: optional for scene-aware-try-on; prohibited for clothes-change
garment_category: upper-body | lower-body | dress | other
garment_locks: silhouette | construction | seams | closures | material | pattern | color | logo | markings
person_locks: identity | apparent age | body proportions | hair | pose | hands | crop
scene_locks: supplied or preserved
delivery: count | ratio | resolution | speed-versus-fidelity
```

For GPT Image 2, use `Image 1 = person`, `Image 2 = garment`, and `Image 3 = location` when supplied. For `virtualtryon`, remap garment to `originalImage`, person to `fashionModelImage`, and location to `locationImage`. For `ai-clothes-changer`, send exactly `[person, garment]`; it has no location input. Use actual uploads rather than describing them back into existence. One output contains one person wearing one primary garment.

### 2. Preflight the inputs

Read [references/input-and-acceptance.md](references/input-and-acceptance.md). Prefer a complete, visible garment; a person whose target body region is not heavily occluded; and, when used, a location with a compatible viewpoint.

Do not crop away required garment features to force a pass. Ask for a clearer source when a missing hem, sleeve, closure, pattern, or body region makes faithful dressing impossible. Treat every result as a visualization, never a guarantee of physical size, fit, comfort, drape, or manufacturing accuracy.

### 3. Confirm the boundary

- Use scene-aware try-on when a garment is being visualized on a person or generated model and an optional location may be supplied.
- Use clothes-change when clothing already worn should be replaced using a person plus garment input. Preserve the unaffected person, clothing, pose, crop, and background; do not accept a location source.
- Use Outfit Design when the garment itself should be invented or redesigned.
- Use Fashion Model Replacement when a dressed source should keep the garment while changing the model or scene.
- Use Change Pose when only pose should change.

### 4. Select the model and fallback

- Default both modes to `gpt-image` v1.0 / GPT Image 2 with all sources in `images`, one concise `textDescription`, `batchCount: 1`, the requested ratio, `quality: "medium"`, and `imageSize: "2K"`. Change quality or resolution only when the user explicitly requests another delivery tier.
- For scene-aware try-on, fall back to `virtualtryon` with `weshopPro` when its separate location field is materially useful or GPT Image 2 is unavailable or fails for a demonstrated capability reason. Use `bananaPro` only for a justified resolution need.
- For clothes-change, fall back to `ai-clothes-changer` when inputs are exactly person plus garment, no location is required, and GPT Image 2 is unavailable or mismatched.
- Use `weshopFlash` only when the user explicitly prioritizes speed or lower cost and accepts lower fidelity. It is the last-quality route, not the first rung of a progressive trial.

Do not run Flash, Pro, and GPT Image 2 in sequence to discover quality. Select the best justified route before spending a run. Record the reason for every fallback and never silently downgrade.

### 5. Compile one concise Prompt

Scene-aware try-on:

```text
Dress the person in Image 1 in the garment from Image 2 [using Image 3 as the location]. Preserve [short person, garment, and scene locks]. Show one [framing] image with plausible fabric contact and occlusion. No redesign, extra clothing, extra person, duplicate view, collage, or added text.
```

Clothes change:

```text
Replace only the person's [target clothing] in Image 1 with the garment from Image 2. Preserve [person, pose, unaffected clothing, crop, and background locks]. Make the replacement naturally worn. No location change, body change, extra clothing, accessory, person, duplicate view, collage, or added text.
```

Translate source numbering when a fallback API uses Figure 1/Figure 2 or dedicated fields. Keep the Prompt about operation, indexed sources, observable locks, and exclusions; do not add generic art direction.

### 6. Execute and accept

Upload every original, submit the selected route, poll to terminal state, and inspect the returned image. Keep person, garment, and optional location as separate Original assets.

Accept only when:

1. One requested image shows one person wearing the intended garment; no before/after, grid, extra view, or duplicate appears.
2. Garment category, silhouette, length, neckline, sleeves, panels, seams, closures, material, color blocking, pattern, logo, and visible markings match the source at the promised level.
3. Fabric conforms plausibly with credible drape, folds, tension, openings, layering, shadows, and contact; no pasted edge, halo, floating cloth, or body bleed appears.
4. The supplied person remains recognisable with credible face, hair, body proportions, hands, limbs, pose, crop, and skin; no anatomy break or unwanted reshaping appears.
5. Hair, hands, arms, accessories, unaffected clothing, and the new garment overlap in the correct depth order.
6. The supplied or preserved scene, framing, ratio, and output count are satisfied without invented people, garments, logos, text, props, or unsupported claims.

### 7. Retry one failed property

- garment drift: shorten optional direction and reassert only the lost construction, material, pattern, or marking;
- anatomy artifact: simplify pose/framing language or use a clearer person source;
- bad occlusion: identify the incorrect front/back relationship;
- scene-field requirement: fall back to `virtualtryon` with `weshopPro`;
- person-plus-garment replacement without scene: fall back to `ai-clothes-changer`;
- explicit speed/cost priority: use `weshopFlash` only with the user's stated tradeoff.

Do not resend an identical request or step through a quality ladder. Record model, parameters, Prompt, execution ID, status, error/refund state, fallback reason, and failed acceptance item.

## User-facing output

- Media type: One virtual try-on or clothes-change image plus a compact source and acceptance record
- Default quantity: 1 separate image
- Content per image: One person wearing one supplied primary garment
- Default layout: Preserve person framing when supplied; otherwise use a clean full-body or garment-appropriate crop
- Video output: No
- Model policy: Default to GPT Image 2; fall back by capability to `virtualtryon` or `ai-clothes-changer`; reserve `weshopFlash` for explicit speed/cost priority
- Downstream use: Pose changes, model replacement, photoshoots, lookbooks, product pages, posters, banners, and photo collages
