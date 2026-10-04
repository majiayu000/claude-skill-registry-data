---
name: image-prompt-engineer
description: "Methodology for writing high-quality image generation prompts across any generator — Midjourney, DALL-E/GPT-Image-2, Stable Diffusion, Flux, Higgsfield, Leonardo, Ideogram. Covers prompt structure, per-generator parameters, style modifier vocabulary, negative prompts, multi-subject composition, and iterative refinement. Use when writing, improving, or troubleshooting an image generation prompt for any tool or any subject (not just photography, not just UI mockups). Triggers on: 'write an image prompt', 'Midjourney prompt', 'DALL-E prompt', 'Stable Diffusion prompt', 'image generation prompt', 'improve this prompt', 'negative prompt'."
---

# Image Prompt Engineer — Prompt Methodology Skill

Teaches HOW to write a great image-generation prompt, for any generator and any subject.
This is a methodology skill, not a lookup library — it gives the structure, vocabulary,
and per-generator parameter syntax needed to construct a prompt from scratch or fix one
that isn't producing the right result.

**Not in scope here:** a curated database of ready-made prompts (see `gpt-image-prompts`
skill for 476+ examples you can browse/search/adapt), and not UI-screenshot-specific
composition rules (see `imagegen-frontend-web` / `imagegen-frontend-mobile` for those).
This skill is the general-purpose methodology underneath all three.

## When to use this skill

- Asked to write an image prompt and no existing curated prompt fits the need
- Asked to improve, debug, or extend an existing prompt that isn't producing the right output
- Building a prompt for a generator not covered by another skill (Stable Diffusion, Flux,
  Higgsfield, Leonardo, Ideogram, etc.)
- Any agent (Image Prompt Engineer, AI Video Producer, content writers, design agents)
  needs to produce or QA an image-generation prompt

## Core Methodology — The Five-Layer Prompt Structure

Every effective image prompt is built in layers, ordered most-important-first. Most
generators weight earlier tokens more heavily, so put what matters most up front.

1. **Subject** — who/what is in frame, with concrete (not vague) descriptors
   - Bad: "a woman"  →  Good: "a woman in her 30s with curly red hair, wearing a tailored navy blazer"
2. **Action / Composition** — pose, framing, what's happening, where elements sit
   - Subject position (centered, rule-of-thirds, foreground/background), interaction with environment
3. **Environment / Setting** — location, time of day, weather, background treatment
4. **Lighting** — source, direction, quality, color temperature (this is the single highest-leverage
   lever for photorealism and mood — never leave it implicit)
5. **Style / Technical** — art style or photography genre, camera/lens specs if photoreal,
   color grade, quality boosters, generator-specific parameters (always last)

**Template:**
```
[Subject, concrete details] + [action/pose/composition] + [environment/setting] +
[lighting: source, direction, quality, color temp] + [style/medium] +
[technical: lens/camera OR art-style specifics] + [quality boosters] + [generator params]
```

Concrete beats vague every time. "Shallow depth of field, f/1.8 bokeh" beats "blurry
background" — name the mechanism, not the visual effect, because generators were trained
on photography/art captions that use mechanism-language.

## Per-Generator Parameter Reference

### Midjourney
Parameters go at the end of the prompt, each prefixed `--`.
| Param | Purpose | Common values |
|---|---|---|
| `--ar` | Aspect ratio | `16:9`, `1:1`, `9:16`, `3:2` |
| `--v` | Model version | `6.1`, `6`, `niji 6` (anime) |
| `--style` | Style preset | `raw` (less opinionated/more literal), `cute`, `scenic` (niji) |
| `--stylize` (`--s`) | How strongly MJ's house aesthetic is applied | `0`–`1000`, default `100` |
| `--chaos` (`--c`) | Variation between the 4 grid outputs | `0`–`100` |
| `--weird` (`--w`) | Unusual/experimental aesthetics | `0`–`3000` |
| `--no` | Negative prompt (exclude elements) | `--no text, watermark` |
| `--seed` | Reproducibility | any integer |
| `::` weighting | Emphasize/de-emphasize a term | `red hair::2 blue eyes::1` |

### DALL-E / GPT-Image-2
No bracket-parameter syntax — everything is natural language. Precision comes from
explicit, plain-English description rather than tokens.
- Specify aspect/composition in words: "wide cinematic shot," "square product photo on white background"
- Specify lighting and perspective explicitly — the model follows literal descriptions well
- Style is steered by naming a medium/genre directly: "isometric vector illustration,"
  "35mm analog film photo," "studio Ghibli-style animation still"
- No native negative-prompt field — exclusions must be phrased positively
  ("clean background" instead of "no clutter") or stated as a constraint in the sentence
  ("no text or logos anywhere in the image")
- See `gpt-image-prompts` skill for 476+ tested examples across 5 categories in this exact style

### Stable Diffusion (and forks: SDXL, SD3, Automatic1111/ComfyUI workflows)
Token-weighted, supports a true negative-prompt field.
| Param | Purpose | Notes |
|---|---|---|
| CFG Scale | How strictly the output follows the prompt | `7`–`12` typical; higher = more literal, less creative |
| Sampler | Denoising algorithm | `DPM++ 2M Karras`, `Euler a`, `DDIM` — affects detail/speed tradeoff |
| Steps | Denoising iterations | `20`–`40` typical; diminishing returns past ~40 |
| Negative prompt | Separate field listing what to avoid | `blurry, deformed hands, extra fingers, watermark, low quality` |
| `(token:1.3)` weighting | Emphasize a term | Higher number = stronger pull |
| LoRA / embedding tags | Style or subject fine-tune reference | `<lora:name:0.8>` |

### Flux (FLUX.1, Flux Pro/Dev)
Natural-language-first like DALL-E, but rewards longer, highly detailed descriptive
paragraphs over keyword-stacking. Strong photorealism — lean on real photography
vocabulary (lens, film stock, lighting setup) rather than generic quality tags.

### Higgsfield
Built for motion/video-adjacent generation — prompts need a motion/camera-move layer
in addition to the static-image layers above.
| Concept | Purpose | Examples |
|---|---|---|
| Motion style | How the subject/scene moves | `subtle parallax`, `slow zoom in`, `dynamic action` |
| Camera move | Virtual camera behavior | `dolly in`, `orbit left`, `static lockoff`, `handheld shake` |
| Reference image/motion | Anchor to an uploaded asset | use `motion_control` for recast/puppeteer/motion-transfer |
- Use `models_explore(action:'recommend')` to pick the right Higgsfield model for the goal before generating.

### Leonardo AI
Preset-driven — prompt is plain language, but model/preset choice carries a lot of the
style weight (PhotoReal, Illustration, Anime presets each interpret the same prompt differently).
Supports negative prompt field and an "Elements" (LoRA-like) system for style consistency.

### Ideogram
Strongest of the mainstream generators at rendering legible text-in-image — if the
deliverable needs accurate on-image typography (posters, signage, logos with text),
prefer Ideogram and state the exact text in quotes within the prompt.

## Style Modifier Vocabulary

**Lighting terms:** golden hour, blue hour, overcast diffused light, hard direct sunlight,
softbox key light, rim/edge light, Rembrandt lighting, butterfly lighting, split lighting,
volumetric light/god rays, neon practical lighting, chiaroscuro, backlit silhouette,
high-key (bright, low contrast), low-key (dark, high contrast)

**Camera/lens terms:** 35mm/50mm/85mm focal length, wide-angle distortion, telephoto
compression, shallow depth of field (f/1.4–f/2.8), deep focus (f/8–f/16), bokeh, macro,
low angle / high angle / bird's-eye / worm's-eye, Dutch tilt, tilt-shift, anamorphic
lens flare, long exposure, motion blur

**Art style terms:** isometric, flat vector illustration, watercolor, oil painting,
cel-shaded anime, photorealistic, hyperrealistic, claymation, low-poly 3D, brutalist,
art nouveau, cyberpunk, vaporwave, minimalist, maximalist, editorial photography,
documentary photography, fine art print

**Quality boosters (use sparingly — generator-dependent, can be redundant on newer models):**
"highly detailed," "8k," "sharp focus," "professional photography," "award-winning" —
on modern models (Midjourney v6+, GPT-Image-2, Flux) these add less than they used to;
concrete descriptive language outperforms generic quality tags. Prefer specificity over boosters.

## Negative Prompt Patterns

Only Midjourney (`--no`), Stable Diffusion (negative field), and Leonardo have a true
negative-prompt mechanism. For DALL-E/GPT-Image-2/Flux, rephrase exclusions as positive
constraints inside the main prompt.

Common negative-prompt targets:
- Anatomy failures: `deformed hands, extra fingers, asymmetric eyes, malformed limbs`
- Unwanted artifacts: `watermark, text, logo, signature, blurry, low quality, jpeg artifacts`
- Composition failures: `cropped, out of frame, duplicate, cluttered background`
- Style leakage: name the unwanted style explicitly if the model keeps drifting toward it
  (e.g., `--no anime` if a photoreal prompt keeps returning illustrated results)

## Multi-Subject / Scene Composition Rules

1. **Establish a clear hierarchy** — name the primary subject first, secondary subjects after,
   with explicit spatial relationships ("in the foreground... behind her, slightly blurred...")
2. **Cap subject count realistically** — most generators degrade past 2-3 named subjects with
   distinct described attributes; complex group scenes need either acceptance of some
   randomness or multiple generation + compositing passes
3. **Use weighting/emphasis** to keep the hierarchy from collapsing (Midjourney `::`,
   SD `(token:1.3)`) — without it, generators often give equal visual weight to all
   mentioned elements regardless of prompt order
4. **Describe interactions, not just co-presence** — "two people shaking hands" generates
   more coherently than "two people, a handshake" as a bolted-on fragment
5. **One scene, one lighting setup** — conflicting lighting descriptions for different
   subjects in the same frame is a common cause of incoherent results

## Iterative Refinement Pattern

1. **Generate a baseline** with the core 5-layer prompt — don't over-specify on attempt 1
2. **Diagnose the gap** — is it composition, style, lighting, or a specific element wrong?
   Change ONE layer at a time; changing everything at once makes it impossible to learn
   what worked
3. **Reuse the seed** (where supported — Midjourney `--seed`, SD seed field) when refining
   composition/style without wanting the whole image to change
4. **Escalate specificity, not length** — replace vague terms with concrete ones rather
   than padding the prompt with more adjectives
5. **When stuck after 3 iterations**, suspect a structural conflict (e.g., asking for both
   "soft diffused light" and "dramatic hard shadows") rather than a wording problem —
   re-read the prompt for contradictions before adding more detail
6. **Document what worked** — once a prompt pattern produces a reliable result for a
   recurring need, that's a candidate to add to the `gpt-image-prompts` library rather
   than rediscovering it each time

## Workflow

1. Identify the target generator (if unspecified, ask or default to GPT-Image-2/natural language)
2. Identify the subject type — is this photography-style (use the Image Prompt Engineer
   agent's genre patterns for portrait/product/landscape/fashion), a UI mockup (route to
   `imagegen-frontend-web`/`imagegen-frontend-mobile` instead), or general/illustrative
   (use this skill's five-layer structure directly)
3. Build the prompt layer by layer: subject → action/composition → environment → lighting → style/technical
4. Apply the generator's parameter syntax from the reference table above
5. Add negative-prompt exclusions if the generator supports them; otherwise fold exclusions
   in as positive constraints
6. If multiple subjects, apply the composition rules above
7. Generate, diagnose gaps against the 5 layers, refine one layer at a time
8. Run critique-imageprompt on the final prompt before delivery — invoke the critique-imageprompt
   agent or paste the prompt into the critique checklist below. Address any FAIL or NEEDS WORK
   findings before finalizing.

## Cross-References

- **`gpt-image-prompts` skill** — 476+ curated, production-tested GPT-Image-2 prompt examples
  across 5 categories. Use it to find a ready-made starting point; use this skill to adapt,
  extend, or troubleshoot it, or to write one from scratch for a different generator.
- **`imagegen-frontend-web` / `imagegen-frontend-mobile` skills** — narrower, UI-screenshot-specific
  composition rules (one-image-per-section, hero composition bias, app-native UI patterns).
  Route there first for website/app design-reference image tasks; this skill is the
  general fallback for everything else.
- **Image Prompt Engineer agent** (`{agency-root}/agents/design/design-image-prompt-engineer.md`) —
  an autonomous agent specializing in photography-genre prompts (portrait, product, landscape,
  fashion) with deep genre-specific templates. Spawn that agent for hands-on photography prompt
  production; read this skill directly when you (or any agent) need the general cross-generator
  methodology, non-photography styles, or a generator the agent's templates don't cover
  (Higgsfield, Leonardo, Ideogram, Stable Diffusion parameter tuning).
- **`critique-imageprompt` agent** (`{agency-root}/agents/critiques/critique-imageprompt.md`) —
  scores any prompt produced with this methodology against character consistency, layer
  completeness, specificity, style coherence, generator fit, and negative-prompt coverage.
  Invoke before delivery (Workflow step 8) or use the Quick Critique Checklist below for an
  inline self-check without spawning an agent.

## Quick Critique Checklist

Before finalizing any image prompt, verify:

☐ Character attributes are concrete and complete (not "a woman" — name every visible trait)
☐ If multi-image series: exact same attribute phrases reused verbatim across all prompts
☐ Per-generator consistency mechanism in place (--cref, LoRA, seed, exact-match phrasing)
☐ All 5 layers present: subject / composition / environment / lighting / style
☐ Lighting is EXPLICIT — source, direction, quality, color temp (never left implicit)
☐ No style contradictions (lighting, medium, art style all coherent)
☐ Generator parameter syntax correct for target tool
☐ Negative prompts present (if supported) covering anatomy + artifacts + composition
