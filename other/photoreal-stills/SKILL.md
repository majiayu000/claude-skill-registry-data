---
name: photoreal-stills
description: >-
  Org pack for ultra-realistic stills: model routing, camera/lens prompting,
  multi-reference identity (incl. dogs/animals), upscale step, and a reject
  checklist so Layer B assets read as photographs — not AI CGI.
---

# Photoreal Stills (org pack)

Use for brand, page, email, social, and paid **still** production when the claim is photoreal / photography-first (e.g. Blacksage Working-Dog Cinema).

**Does not replace** Plane B render skills — it **gates** how seats prompt, render, upscale, and accept stills.

## Read with

| Pack | Role |
|------|------|
| `skills/community/openmontage/.claude/skills/flux-best-practices/` | FLUX.2 T2I/I2I, hex, multi-ref, no negatives |
| `skills/community/visual-skills/image/` | Prompt templates / model pick (prompt craft) |
| `skills/integrations/ai-toolkit-local/` | **Mac primary:** local [FLUX.2-dev](https://huggingface.co/black-forest-labs/FLUX.2-dev) via Ostris ai-toolkit |
| `skills/integrations/fal-media/` | fal FLUX.2 max/pro commercial/API upgrade |
| `skills/community/inference-sh/flux-image/` | inference.sh FLUX path |
| `skills/community/inference-sh/ai-image-generation/` | Multi-model still render |
| `skills/community/inference-sh/image-upscaling/` | Final megapixel / print pass |
| `skills/org/packs/production-artifacts/` | Paths + `production_status` |

## Prerequisite: Design brief

Do **not** call image generation until a Design brief exists (see `production-artifacts` **Design-before-production gate**). The brief must include the exact generation prompt(s), brand hex/lighting locks, crop/aspect, and cited design packs (`visual-skills/image`, brand, email-design for headers, etc.). Production stills are rendered **from the brief**, not freestyled.

## How “indistinguishable from reality” is achieved

Research + BFL guidance converge on a **pipeline**, not a magic adjective (“8k”, “ultra realistic”):

1. **Right final model** — On Mac: **FLUX.2-dev** local (`generation_used: local/flux-2-dev`) via ai-toolkit when `HF_TOKEN` is set. Commercial API upgrade: **FLUX.2 [max]/[pro]** via fal. Use klein only for speed drafts. Cursor built-in image gen is **draft / concept** — not client-final. Local commercial Layer B requires `license_basis: bfl-self-hosted-commercial` or fal re-render.
2. **Photographic language** — Prose subject + action + environment, then **camera body, lens, aperture, film/sensor, lighting**. BFL: camera/lens/film references outperform vague “professional photo” ([FLUX.2 prompting guide](https://docs.bfl.ml/guides/prompting_guide_flux2)).
3. **One job per image** — Do not mix watercolor + cinematic + cyberpunk in one prompt; focus collapses realism ([Artlist FLUX 2 practices](https://artlist.io/blog/best-practices-flux-2/)).
4. **Positive-only** — FLUX has no negatives; describe sharp focus, natural skin/fur, empty scene instead of “no blur / no CGI”.
5. **Multi-reference for identity** — Lock dog/person/product with reference images; name each image’s role (identity / pose / lighting / environment). FLUX.2 supports multi-ref; use for kennel lines and recurring subjects ([FLUX.2 product](https://bfl.ai/models/flux-2)).
6. **Resolution ladder** — Draft low → final high (up to ~4MP on FLUX.2 commercial) → optional **upscale** pack for print/retina.
7. **Human reject pass** — Zoom 100%; fail plastic fur, wrong anatomy, CGI sheen, impossible DOF, text glitches (see checklist).

### Prompt skeleton (FLUX finals)

```text
[Subject with breed/age/markings] [pose/action]
[Environment — materials, time of day]
[Lighting — key direction, quality, color as hex when brand-locked]
Shot on [camera body], [focal length]mm at f/[aperture], [film stock or sensor look]
[Framing], shallow/deep DOF as needed
Photorealistic documentary photography, natural detail
```

Brand hex example (Blacksage): tan key `#C4A35A` on markings; void `#070707`.

### Model routing (Plane B)

| Stage | Prefer | Avoid as final |
|-------|--------|----------------|
| Ideation / mood | FLUX.2 klein, Cursor GenerateImage | Claiming production complete |
| Brand / page / email hero (Mac) | FLUX.2-dev local via `ai-toolkit-local` + `scripts/render-blacksage-stills.sh` | Unspecified “AI art” models |
| Brand / page / email hero (API) | FLUX.2 max or pro via fal or inference.sh | Draft-only gens |
| Paid stills | Local FLUX.2-dev (licensed) or fal pro/max / GPT Image per `ad-creative` | Cursor drafts |
| Upscale | `image-upscaling` (Topaz / FLUX upscaler / Real-ESRGAN as pack allows) | Stretching draft PNG in CSS |

Record `generation_used` e.g. `local/flux-2-dev` or `fal/flux-2-max` + upscaler id + `license_basis` when local.

### Dog / animal identity (kennel ventures)

Human character sheets are **not** enough. For recurring dogs:

1. Collect 3–8 real or approved reference photos (angles: front, three-quarter, side; markings clear).
2. Prompt with **explicit markings** (chest blaze, eyebrow dots, muzzle tan) + age/sex/build.
3. Multi-ref: image 1 = identity lock; image 2 = pose; image 3 = lighting/environment.
4. Reject if markings drift, eyes look glass/CGI, coat looks wet plastic, or proportions cartoonize.
5. Same seed + refs when iterating a locked hero.

## Photoreal reject checklist (required before `production_status: complete`)

Zoom to 100% on the delivery file:

- [ ] Reads as a **photograph**, not illustration / 3D render / AI poster
- [ ] No plastic/waxy skin or fur; natural micro-texture visible
- [ ] Eyes: catchlights plausible; no dead “glass” or doubled pupils
- [ ] Anatomy OK (limbs, ears, teeth if visible) — no melted digits/claws
- [ ] Lighting physics consistent (one key story; shadows match)
- [ ] Depth of field matches stated aperture (background blur not fake smear)
- [ ] No random text, watermarks, or logo glitches
- [ ] Brand hex / grade not purple glow / cream terracotta AI defaults
- [ ] For recurring subject: markings match refs
- [ ] Resolution suitable for lease (email header ≥1200px wide; heroes ≥1920 on long edge or upscaled)

Fail any → regenerate or I2I fix; do not ship.

## Seat duties

| Seat | Duty |
|------|------|
| `brand-designer` | Owns photoreal stills; runs checklist; upscales finals |
| `web-designer` | UI stills via same pack when leased |
| `paid-media-manager` | Ad stills; same checklist |
| `creative-director` | Prompt + photoreal QA before merge |
| `verifier` | Spot-check checklist + files on disk for claimed complete stills |

## Handoff fields (add when stills produced)

```yaml
generation_used: fal/flux-2-max   # or inference-sh/...
photoreal_qa: pass | fail
photoreal_notes: ""               # what was checked / why fail
reference_paths: []               # multi-ref inputs if any
```

## Anti-patterns

- Shipping Cursor draft gens as Layer B finals
- “8k ultra detailed masterpiece” keyword salad
- Negative-prompt habits on FLUX
- Completing production without zoom QA
- Treating Figma mock as the still (export required — see production-artifacts)
