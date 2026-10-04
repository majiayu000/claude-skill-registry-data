---
model_tier: inherit
name: video-director
description: "Use when a live-action beat becomes the 11-block cinematic prompt — lens, lighting, negatives. Triggers 'cinematic prompt', 'film-grade scene'. Animated → pixar-storyteller; 12-block → scene-expander."
personas:
  - hollywood-director
domain: product
workspaces:
  - small-business
packs:
  - ai-video
lifecycle: experimental
trust:
  level: experimental
install:
  default: false
  removable: true
---

# video-director

> Turn a scene idea into the **11-block cinematic prompt** the
> `hollywood-director` persona ships. Output is provider-agnostic
> prose; provider-specific tuning is handed off to
> [`motion-choreographer`](../motion-choreographer/SKILL.md).

## When to use

- A scene idea, beat, or script line needs to become a cinematic
  prompt ready to feed an image+video pipeline.
- A draft prompt reads as "AI video" — flat, centered, generic
  golden-hour — and needs directorial choices on the page.
- Live-action / photoreal scenes. For animation acting beats, route
  to [`pixar-storyteller`](../pixar-storyteller/SKILL.md).

Do NOT use when:

- The deliverable is a still graphic or poster → `canvas-design`.
- The work is provider-specific token tuning →
  `motion-choreographer` after this skill has produced the blocks.
- A character identity must be re-used across scenes → run
  [`character-consistency`](../character-consistency/SKILL.md) first
  to lock identity tokens, then call this skill.

## Procedure

### Step 0: Inspect

1. Confirm the input is a live-action / photoreal beat (not animation).
2. If a `character.json` exists under `agents/reference/ai-video/<project>/characters/`,
   read the identity tokens — they are reused verbatim.
3. Read the scene's intent in one sentence — what is the camera
   witnessing, and why now?

### Step 1: Draft the 11 blocks

Emit each block on its own labeled line. Blocks are mandatory and
in this order:

1. **SCENE** — location, time-of-day, weather, era.
2. **CHARACTER** — verbatim identity tokens from `character.json`
   when present; otherwise silhouette + wardrobe + signature prop.
3. **ACTION** — verbs and beats. Anticipation → action → reaction
   named separately. No "doing things" prose.
4. **CAMERA** — position, height, distance, move (lock-off, dolly,
   handheld, push, pull). Off-axis when on-axis is the AI default.
5. **LENS** — focal length in mm (24 / 35 / 50 / 85 / 200) and
   aperture intent (deep / shallow). "Cinematic" alone fails.
6. **LIGHTING** — key, fill, back, practical sources named. "Golden
   hour" requires an angle (low-east 15°, etc.).
7. **ENVIRONMENT MOTION** — what the world does (wind, water,
   crowd, traffic) and on which beat.
8. **SECONDARY MOTION** — hair, cloth, dust, breath. Names the
   reactive layer that sells the primary action.
9. **MOOD** — one emotional read; no compound moods.
10. **DURATION** — seconds. Integer or one decimal.
11. **NEGATIVE CONSTRAINTS** — clichés to reject, in load-bearing
    order (top survives truncation). Always names: centered framing,
    symmetric composition, generic "cinematic", soap-opera contrast.

### Step 2: Self-review

1. Lens length present? "Cinematic" without mm → fail.
2. Lighting direction present? "Golden hour" without angle → fail.
3. ACTION names beats, not adjectives?
4. NEGATIVE block has at least 4 entries, load-bearing on top?
5. CHARACTER block reuses identity tokens verbatim when a lock exists?

Any "no" → revise that block before handing off.

### Step 3: Validate

1. Output is plain text, one labeled block per line, ready for
   `scripts/ai-video/lib/parse-blueprint.sh` (Phase 3 Step 5).
2. No provider tokens (no `--aspect`, no `--model`). That is
   `motion-choreographer`'s job.

## Output format

1. **`scenes/<id>/prompt.txt`** — 11 labeled blocks, one per line,
   ready for the blueprint parser.
2. **`scenes/<id>/review.md`** — one-paragraph rationale per
   non-obvious directorial choice (lens, light angle, camera move).

## Gotcha

- The model defaults to centered, on-axis, symmetric — name an
  off-axis or rule-of-thirds camera or it will silently center.
- "Golden hour" alone reads as a sunset GIF; require a sun angle.
- ACTION written as a paragraph of adjectives ("dynamically", "powerfully")
  fails — adapters need verbs with beat counts.
- When `character.json` exists, paraphrasing identity tokens breaks
  Character Lock — copy them verbatim.
- Negative constraints in the truncated tail get dropped — load-
  bearing ones go first.

## Do NOT

- Do NOT emit provider-specific tokens (aspect ratio, model id,
  duration flags) — that is `motion-choreographer`'s scope.
- Do NOT collapse anticipation / action / reaction into one verb.
- Do NOT use "cinematic" without lens + lighting + camera move.
- Do NOT invent character details when a `character.json` exists.

## Policies

Paths, enforcement model, and the full set: the
[media policy preamble](../../../agents/settings/policies/media/README.md).

The 11-block cinematic prompt is live-action shape — real-person and brand-impersonation risks are the highest in the cluster. Before emitting:

- **`likeness`** — when the prompt names or visually identifies a real person on camera.
- **`public-figures`** — when the subject is a recognised public figure.
- **`brand-impersonation`** — when the prompt copies a journalism / broadcaster / regulated-industry visual identity.
- **`style`** — when LIGHT / LENS choices are anchored to a named living cinematographer's signature.
- **`disclosure`** — every distributed live-action AI clip carries the non-removable AI-generation disclosure.

Refuse-and-surface at the directorial layer; live-action realism amplifies every policy gap downstream.

