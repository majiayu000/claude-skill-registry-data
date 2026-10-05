---
name: change-pose
description: Change the pose of one already-dressed person while preserving identity, body proportions, complete outfit, branding, accessories, background, lighting, and commercial image continuity. Use for fashion reposing, pose variants, catalog stance changes, walking or seated poses, and pose-reference requests; do not use for changing the model, changing clothing, creating a new photoshoot, animating video, or editing only an expression or hand.
---

# Change Pose

Create one requested pose or three useful choices from one dressed-person image. Define the Skill by pose transfer and preservation, not by a specific engine.

## Catalog

- Display name: Change Pose
- Categories: Portrait, Commercial Production
- Status: Ready
- Featured: yes
- Route label: WeShop AI Pose pro or GPT Image 2
- Tone: blue
- Short description: Change a person’s pose without changing their look.

- Similar skills: fashion-model-replacement, virtual-try-on
## What this skill does

- Changes only the pose of one already-dressed person.
- Returns three deliberately different commercial choices when the target pose is unspecified.
- Preserves the source identity, body proportions, complete outfit, branding, accessories, footwear, and scene locks.
- Routes text poses to WeShop AI Pose pro and supplied pose references to GPT Image 2.
- Validates pose accuracy, identity, garment fidelity, anatomy, scene continuity, and output count.

## How to use

Provide one clear dressed-person image and describe the new pose; if you do not specify one, the Skill returns three different commercial pose options.

#### Create three pose options

```text
Give this model a different pose.
```

#### Create one described pose

```text
Turn the model three-quarter to camera with one hand at the hip and weight on the back leg.
```

#### Follow a pose reference

```text
Make the dressed model follow the supplied pose reference while keeping the original person, outfit, and studio.
```

## Workflow

### 1. Bind the sources and locks

Require one image containing one already-dressed person. Record the requested pose, output count, framing, and these default locks:

```yaml
preserve: identity | hair | body proportions | complete outfit | construction | color | pattern | branding | accessories | footwear
scene_locks: background | lighting | camera | crop
allowed_change: body pose | natural garment folds caused by the new pose
```

Read [references/input-and-acceptance.md](references/input-and-acceptance.md) when the source is cropped, occluded, low-resolution, multi-person, or the target pose is extreme.

Do not route garment replacement, model replacement, a new photoshoot, animation, or local hand/expression repair here.

### 2. Resolve an underspecified request

If the user only asks to change the pose without defining a pose or quantity, return exactly three separate images:

1. relaxed front-facing catalog stance with open garment visibility;
2. confident three-quarter weight-shift stance with one hand at the hip;
3. natural mid-step walking pose with arms clear of the garment.

Compile and execute each pose separately with `batchCount: 1`. Do not use one three-image batch, a grid, collage, or three near-duplicate random generations.

If the user names one pose, return one image unless they request another quantity. Explicit user instructions override the default trio.

### 3. Select the route

- **Text-described pose:** use `aipose` v1.0 with `generateVersion: "pro"` and `batchCount: 1`. Do not consider `lite` as the normal fallback.
- **Supplied pose-reference image:** the verified `aipose` contract has no pose-image input. Use GPT Image 2 with the dressed source and pose reference, `quality: "medium"`, `imageSize: "2K"`, and one result per run.
- **Fallback:** switch only for a demonstrated capability mismatch or failed acceptance, never as a progressive quality ladder.

Read [references/api-and-routing.md](references/api-and-routing.md) before execution.

### 4. Compile an atomic pose Prompt

Describe pose in this order: overall action, torso orientation, weight, limbs, head/gaze. Include only observable geometry required to distinguish the result.

```text
Repose the same model into [overall pose], [weight and torso], [limbs], and [head/gaze]. Preserve the exact person, face, hair, body proportions, complete outfit, garment construction, colors, patterns, branding, accessories, footwear, background, lighting, crop, and camera.
```

Avoid generic fashion adjectives, exhaustive joint angles, contradictory limb directions, or claims that invisible source details can be exactly preserved.

### 5. Execute and inspect

Submit one run per pose and poll every accepted execution to terminal state. A returned result URL is not sufficient if the execution remains pending or running.

Apply the checks in [references/input-and-acceptance.md](references/input-and-acceptance.md). API success is not visual acceptance.

### 6. Retry only the failed property

- incorrect pose: simplify to overall action, weight, and the failed limb;
- hidden garment: move the arm or hand away from the product instead of regenerating randomly;
- identity drift: shorten pose language and strengthen face, hair, and body locks;
- garment drift: restate only the lost construction, color, pattern, or branding anchors;
- anatomy failure: reduce crossing or self-occlusion and request a natural joint relationship;
- crop or scene drift: restate the original crop, background, lighting, and camera.

Never resend an identical request. Record route, parameters, Prompt revision, execution ID, terminal state, and failed acceptance item.

## User-facing output

- Media type: Separate pose-change images plus a compact acceptance record
- Default quantity: 3 when no pose is specified; otherwise 1
- Content per image: One model in one pose
- Default layout: Preserve source scene and framing; no collage
- Model policy: `aipose` pro for text poses; GPT Image 2 medium/2K for supplied pose references
- Downstream use: Lookbooks, collages, product pages, photoshoots, posters, and banners
