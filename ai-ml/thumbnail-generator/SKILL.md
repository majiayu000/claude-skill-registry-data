---
name: thumbnail-generator
description: "YouTube thumbnail generator via Higgsfield Nano Banana Pro. Claude reads the video's hook/title (Notion page or raw string), proposes thumbnail concepts with cinematic prompts anchored to your face-ref photo library, you approve the manifest, then submits in parallel and downloads 16:9 PNGs. Optional per-concept extra_refs bake in logos/products/scene refs. A second script burns tilted yellow/white title blocks on top with PIL — no Canva/Photoshop needed. Style-match mode (face_refs: false) lets you mimic an existing thumbnail's no-humans aesthetic. Triggers: make a thumbnail, yt thumbnail, generate thumbnail, youtube thumbnail, design a thumbnail, style-match this thumbnail, add title to thumbnail."
---

> **Video Studio:** this skill lives in `engines/legacy-editor`. Before running anything from it, `cd engines/legacy-editor` and use that folder's copy (`engines/legacy-editor/.claude/skills/thumbnail-generator/`), which has its scripts and reference files. Every path below is relative to `engines/legacy-editor`. This copy only lets Claude find the skill from the Video Studio folder.


# Thumbnail Generator — YouTube Thumbnails via Nano Banana Pro

Generates branded YT thumbnails anchored to a small library of real photos of you at `assets/face-refs/`. Claude reads the video's hook, proposes concepts (composition, expression, lighting, single visual metaphor), then `nano_banana_2` (Nano Banana Pro) renders 16:9 variants. Optional `extra_refs` per concept bake in logos / products / scene refs alongside the face anchors. Two-stage pipeline: `generate.py` produces the base image with empty negative space for type, then `add_title.py` burns tilted yellow/white title blocks on top (no Canva/Photoshop needed). The model never renders text itself — it hallucinates gibberish letters — type always comes from the PIL stage.

## Anchor Library (live)

| Source | Purpose |
|---|---|
| `assets/face-refs/*.{png,jpg,jpeg,webp}` | Real and AI-generated photos of you, varied angles + expressions + lighting. Always passed as `--image <path>` on every generation. |
| `assets/logos/*.png` | Brand marks (Claude, Codex, etc.) — referenced per-concept via `extra_refs`. |

The CLI auto-uploads local paths every run. No upload-id cache to manage. Adding a new file to `assets/face-refs/` takes effect on the next generation automatically.

**Why this approach beats Soul V2:** Soul-trained fine-tunes drift, leak training-image artifacts (UI screenshots, gibberish text), and lock you into the Soul-aware model lineup. `nano_banana_2` with multi-photo `input_images` gives photoreal output, locks identity from 3+ angles simultaneously, and unlocks the SOTA image models. Trade-off: $2/image vs $0.12 for Soul V2 — but Soul V2 results were unusable so this is the actual price.

**Proven settings (codex-vs-claude-code test, 2026-05-17):** 6 face-refs + 2 logo extra_refs + `nano_banana_2` at `16:9 / 2k` produced clean photoreal output, recognizable logos, locked identity, zero hallucinated text. The orange Anthropic brand vs the purple-blue Codex brand creates a natural warm/cool color split — leverage it in prompts.

## When to Use

- Long-form YT videos before posting (`your posting tool` doesn't generate the thumbnail).
- Standalone — not part of the reels editing pipeline.
- Re-roll freely; cost is ~$6/concept set of 3 variants.

## The Flow

```
1. Claude reads input: a Notion page name/ID OR a raw title string (or a reference thumbnail URL to style-match)
2. Claude writes /tmp/thumbnails/<slug>/thumb.json — concepts + prompts + (optional) extra_refs
3. You review the manifest, edit prompts, drop concepts
4. Run generate.py → uploads new face-refs/logos, submits in parallel, downloads
5. Pick the winner → run add_title.py with title blocks → upload to YT
```

**Manifest review is the safety gate.** No money spent until you say go.

## Style-Matching an Existing Thumbnail

When the input is a YouTube URL or screenshot and you want to mimic that style — especially a flat-illustration / mascot / no-humans look — face-refs will pollute the gen. Disable them and use the reference as a style anchor.

1. Download the reference: `curl -sL "https://i.ytimg.com/vi/<video_id>/maxresdefault.jpg" -o /tmp/thumbnails/<slug>/reference.jpg`
2. Read it to extract style cues (palette, character treatment, composition, negative space).
3. In `thumb.json` set `"face_refs": false` at the manifest level (default is `true`).
4. Add the reference image + any brand logos to each concept's `extra_refs` as style anchors.
5. Write prompts that describe the matched style explicitly — "flat sticker illustration, blocky mascot, no humans, no text".

Validated 2026-05-17 on a "Codex Era" style-match (two terracotta-block mascots on charcoal bg). With face-refs on, the model tried to embed your likeness into the mascot graphic; with `face_refs: false` + reference image as `extra_ref`, it matched the flat sticker aesthetic cleanly.

**Variant: the reference contains a DIFFERENT person but your face must stay locked (validated 2026-06-26).** Don't pass the full reference, and don't turn face_refs off. Two competing human identities in the input set make Nano Banana blend faces, and dropping face_refs loses you entirely. Instead: PIL-crop the reference down to just the objects/composition to replicate (exclude the other person AND any baked-in title text), pass the crop as `extra_ref` with `face_refs: true`. your identity stays anchored while the cropped elements carry the reference's composition.

## Manifest Schema

```json
{
  "topic": "Codex vs. Claude Code",
  "slug": "codex-vs-claude-code",
  "model": "nano_banana_2",
  "aspect_ratio": "16:9",
  "quality": "2k",
  "variants_per_concept": 3,
  "face_refs": true,
  "concepts": [
    {
      "id": "c1",
      "name": "split-verdict",
      "prompt": "...",
      "extra_refs": [
        "assets/logos/claude-icon-color.png",
        "assets/logos/codex-icon-color.png"
      ]
    },
    {
      "id": "c2",
      "name": "shock-vs",
      "prompt": "...",
      "model": "seedream_v4_5",
      "quality": "high"
    }
  ]
}
```

**Defaults** (overrideable per concept):
- `model` — `nano_banana_2`
- `aspect_ratio` — `16:9`
- `quality` — `2k` for nano_banana_2 (no extra cost), `high` for seedream_v4_5
- `variants_per_concept` — `3`
- `face_refs` — `true` (manifest-level only). Set `false` to skip auto-loading `assets/face-refs/` — use for style-match runs with no humans.

**`extra_refs`** — paths relative to project root or absolute. Appended to the auto-loaded face-refs on every variant of that concept. Use for logos, product shots, color palette refs, or scene references.

**Per-model quality flag** (auto-handled by script):
| Model | CLI flag | Valid values |
|---|---|---|
| `nano_banana_2` | `--resolution` | `1k`, `2k`, `4k` |
| `seedream_v4_5` | `--quality` | `basic`, `high` |

`text2image_soul_v2` is **not supported** by this skill — it uses a different schema (`medias` + `custom_reference_id`, not `input_images`) and Soul-fine-tune drift produced unusable results. Pin to `nano_banana_2` unless you specifically need seedream's cinematic flair.

## Prompt Style Guide

Thumbnail prompts ≠ B-roll prompts. Different rules:

| Element | Thumbnail | B-roll |
|---|---|---|
| Subject | "This person" — face fidelity from input_images | Concrete scene |
| Expression | **Critical** — wide-eye, half-smirk, raised brow, mouth-open shock. Locked into prompt. | Often abstract / no face |
| Composition | Rule-of-thirds. Call out negative space for title overlay. | Cinematic motion focus |
| Background | One legible visual metaphor (lightning, smoke, dust, glow, color split) | Environmental texture |
| Color | High contrast, 2-color story (cool/warm split, teal/orange, blue/red) | Mood-driven, varied |
| Lens / lighting | "35mm shallow DOF", "key light from camera-left", "neon practicals" | Same toolkit |
| **Forbidden** | "text on screen", "title overlay", "subtitles", "ChatGPT chat UI", "terminal interface", any text-bearing UI element. Nano Banana Pro will hallucinate gibberish letters wherever you imply text. Use abstract physical metaphors instead. | n/a |

✅ **Good prompt:**
"Photoreal portrait of this person mid-shocked-laugh, eyes wide, mouth open, hands raised palms-up. Background bisected vertically — left half deep electric-blue lightning column, right half warm amber dust storm. Hard-edge color split behind silhouette. Studio key from above, 50mm shallow DOF, photoreal cinematic. Negative space lower-third for title overlay."

❌ **Bad prompt:**
"Claude Code vs ChatGPT thumbnail showing you looking at a terminal screen with code and a chat window"

Why bad: names a screen + terminal + chat window = model renders gibberish text on all three.

## Usage

```bash
# After Claude writes /tmp/thumbnails/<slug>/thumb.json and you've reviewed it:
python3 .claude/skills/thumbnail-generator/scripts/generate.py /tmp/thumbnails/<slug>/thumb.json

# Re-roll one concept:
python3 .claude/skills/thumbnail-generator/scripts/generate.py /tmp/thumbnails/<slug>/thumb.json --only c1

# Dry-run:
python3 .claude/skills/thumbnail-generator/scripts/generate.py /tmp/thumbnails/<slug>/thumb.json --dry-run
```

Output: `projects/<slug>/thumbnails/generated/<concept_id>_v<n>.png`.

## Adding the Title (add_title.py)

After picking a winner, burn the title type on top with `add_title.py`. Renders bold black Helvetica on tilted yellow/white blocks at the top of the image — the "The Codex Era" sticker aesthetic.

```bash
python3 .claude/skills/thumbnail-generator/scripts/add_title.py \
  projects/<slug>/thumbnails/generated/<winner>.png \
  /tmp/thumbnails/<slug>/titled_<winner>.png \
  --blocks '[
    {"text": "CLAUDE", "bg": "#FFFFFF", "fg": "#000000", "rotation": 0, "scale": 0.16},
    {"text": "vs.",    "bg": "#FFD600", "fg": "#000000", "rotation": -8, "scale": 0.10, "offset_y": -0.025},
    {"text": "CODEX",  "bg": "#FFD600", "fg": "#000000", "rotation": 0, "scale": 0.16}
  ]'
```

**Block schema:**
- `text` — string to render
- `bg` — hex color of block (yellow accent `#FFD600`, white block `#FFFFFF`, custom welcome)
- `fg` — hex text color, default `#000000`
- `rotation` — degrees, positive = ccw left tilt. Small accent words ~ -8°; main blocks 0°.
- `scale` — font height as fraction of image height. Main words ~0.16, accent words ~0.10.
- `pad_x` / `pad_y` — block padding in font-height units (defaults 0.35 / 0.20)
- `offset_x` / `offset_y` — per-block nudge as fraction of image dims. Use `-0.025` on accent words to lift them above the main row.

**Global flags:** `--top-margin` (default `0.04` of image height) sets the row's vertical position. `--gap` (default `0.01` of width) sets horizontal block spacing.

Blocks are placed in a horizontal row centered horizontally, anchored at top-margin. Tilted blocks rotate around their own center; use `offset_y` to lift them above the row like the reference aesthetic.

**Proven recipe (Codex Era style):** one small tilted yellow accent block + two large straight blocks (white + yellow). Validated 2026-05-17 on the CLAUDE-vs-CODEX boxing thumbnail.

## CLI Quirks (read before editing)

**Authoritative upstream docs** (canonical source — read these before guessing):
- [`higgsfield-ai/skills/higgsfield-generate/references/media-inputs.md`](https://github.com/higgsfield-ai/skills/blob/main/higgsfield-generate/references/media-inputs.md) — per-model media roles, single-vs-multi-image models, schema mismatch error meanings
- [`higgsfield-ai/skills/higgsfield-generate/references/prompt-engineering.md`](https://github.com/higgsfield-ai/skills/blob/main/higgsfield-generate/references/prompt-engineering.md) — prompt length caps, image-to-image vs image-to-video framing, ip-detect / nsfw rejection avoidance
- [`higgsfield-ai/skills/higgsfield-generate/references/model-catalog.md`](https://github.com/higgsfield-ai/skills/blob/main/higgsfield-generate/references/model-catalog.md) — full model list with use-case mapping

Higgsfield CLI playbook. Notes on the installed CLI `v0.1.40`:

- **No `--output-dir`.** Script runs with `--json --wait`, walks the response for `status: completed` + `result_url`, downloads via urllib.
- **`--image` is the canonical face-anchor flag** — repeat it once per reference: `--image ./a.png --image ./b.png --image <upload_id>`. The CLI auto-uploads local paths (no manual `higgsfield upload create` needed). The `--input_images` JSON-array shape works too but is more brittle and required for advanced types (`image_job`, `nano_banana_2_job` etc. — unused here).
- **Quality flag differs per model** — `nano_banana_2` uses `--resolution`, `seedream_v4_5` uses `--quality`. Script maps via `MODEL_CONFIG`.
- **Multi-image ref cap is per-model** — Nano Banana Pro accepts ~8 images per upstream docs. 6 face-refs + 2 logos = inside the headroom.
- **Result extraction is strict** — only matches nodes with `status: completed` + `result_url`. No regex fallback (would grab echoed `--image` upload URLs).
- **Model schema source of truth:** `higgsfield model get <model>` — NOT `generate create --help` (only shows global flags).
- **Auth check is `higgsfield account status`**, not `auth status` (which is a help menu).

## Cost Math (Higgsfield)

Cost math assumes Higgsfield's **$49/mo Plus plan, 1000 credits/month** (1 credit = **$0.049**); rescale to your plan.

| Model | Credits / image | Real cost |
|---|---|---|
| `nano_banana_2` (Pro) | 2 | **$0.098** (default — best identity from input_images, no cost diff 1k/2k/4k) |
| `seedream_v4_5` | 1 | **$0.049** (cinematic flair, slight identity drift) |

Typical runs (nano_banana_2):
- 1 concept × 3 variants = **$0.29**
- 1 concept × 4 variants = **$0.39**
- 2 concepts × 4 variants = **$0.78**
- 3 concepts × 4 variants = **$1.18**

Marginal cost is $0 until the monthly credit cap — but the per-image price is what the script reports so the math stays correct if the plan changes.

Script prints estimate before submit:
```
[thumb] 3 concept(s) × 4 variant(s) = 12 images ≈ $1.18 total. Continue? [y/N]
```

## Gotchas

- **Generation time** — 30–60s per image, parallel via `--wait`. 6-image batch ≈ 1–2 min wall.
- **Identity fidelity scales with refs** — 6 face-refs > 2 > 1. Add a new pose to `assets/face-refs/` and the next run picks it up automatically (mtime cache invalidates).
- **Logos in extra_refs** — Nano Banana Pro respects brand-mark composition well but doesn't always render them at the size you wrote. If a logo comes out tiny, say "large prominent logo" explicitly in the prompt.
- **Negative space is a request, not a guarantee** — verify on output before paying for type-overlay work.
- **Failed generations** — script reports per-concept failures. Re-run with `--only c2` to retry.
- **Manifest review is mandatory** — never auto-approve. Prompts are the creative work.
- **No text in image** — title type is burned on by `add_title.py` after, never by the model. The model hallucinates gibberish if asked for words.

## What This Skill Does NOT Do

- Pull Notion script content automatically (Claude does that before writing the manifest)
- Upload to YouTube (`your posting tool` handles posting)
- Generate Reels covers / IG carousel covers (different aspect, different rules — out of scope)
- Train Soul IDs or run Marketing Studio workflows (broader Higgsfield surface — this skill is just thumbnails)
