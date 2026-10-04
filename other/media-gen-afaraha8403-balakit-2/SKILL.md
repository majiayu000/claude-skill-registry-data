---
name: media-gen
description: >-
  AI media generation via Fal.ai: images, video, upscale, edits.
  Produces Instagram ad creative using a dual-model pipeline —
  runs Nano Banana Pro Edit AND Ideogram v4 Image-to-Image side-by-side
  for every concept, giving the user two takes per brief at negligible cost
  (~$0.28/concept). Always uses image-to-image when a reference image is
  provided, preserving product identity. Crafts photography-grade prompts
  using camera/lens/lighting terminology. Sends 1 image per message
  (Telegram delivery limitation).
  Use whenever the user says "generate an image", "create a photo",
  "make a video", "upscale this", "turn this into a video".
user-invocable: false
disable-model-invocation: false
version: "3.1.0"
author: "Balacode"
tags: [image-generation, video-generation, fal-ai, media, dual-model, social-media-ads, prompt-craft, photography, instagram-ads]
when_to_use: |
  USE WHEN:
  - User asks to generate, create, make, render, or produce an image/photo/picture.
  - User wants to animate an image into a video, or generate video from an image.
  - User wants to upscale, enhance, or sharpen an image or video.
  - User wants to edit an image (inpaint, outpaint, style transfer, re-style).
  - User mentions Fal.ai, or any specific image/video model by name.

  DO NOT USE WHEN:
  - User needs text-to-video from scratch with no seed image (use a video-first workflow).
  - User needs real-time video processing (Fal latency too high).
  - User wants audio/music generation (different domain).
---

# Media Generation (Fal.ai) — v3.1

> **Leading words:** pick the model, run the script, dual-model ads, one
> image per message, native filesystem path.

**Decision model (read this first):**
1. Pick the job: still / edit / upscale / video / Instagram ad pair.
2. Run `scripts/generate.py` (or the documented fal_client call). Do not
   paste a rotated key; use `FAL_KEY="$FAL_KEY"`.
3. Image-to-image when a reference exists. Dual-model for ad concepts
   (Nano Banana Pro Edit + Ideogram v4).
4. One image per chat message (Telegram).
5. Depth: [references/endpoint-models.md](references/endpoint-models.md),
   [references/model-input-formats.md](references/model-input-formats.md),
   [references/high-conversion-prompting.md](references/high-conversion-prompting.md),
   [references/fal-key-troubleshooting.md](references/fal-key-troubleshooting.md),
   [references/wix-product-image-extraction.md](references/wix-product-image-extraction.md).

**Black Forest Labs FLUX Prompting Guide Reference:**
The official FLUX prompting guide is at https://docs.bfl.ml/guides/prompting_summary.md
All photography terminology lives in [references/photography-lexicon.md](references/photography-lexicon.md), sourced from BFL's official Prompt Reference (https://docs.bfl.ml/guides/prompting_unified_reference.md).

**Key principle from BFL:** *"Prompt the model as if describing a real photograph: specify lens, lighting, framing, and texture details for maximum realism."*

**How FLUX reads prompts:** Write in prose, not keyword lists — describe scenes like a novelist. Lighting descriptions have the highest single impact on output quality.

---

## Setup

```bash
# Prerequisites
export FAL_KEY="your-key-here"   # On Windows: setx FAL_KEY "key" (restart terminal)
pip install fal-client

# CRITICAL: fal-client >= 1.0.0 required for CDN upload (image-to-image)
# Old v0.13.1 broke CDN auth. Upgrade: pip install --upgrade fal-client
```

**CRITICAL: FAL_KEY must use shell expansion, not the literal string.**
Hardcoding the key string (`FAL_KEY="07138a1e-..."`) returns 401 even when the shell-expanded version (`FAL_KEY="$FAL_KEY"`) works. The env var may contain escape characters or may have been rotated since you read it.
  ✅ `FAL_KEY="$FAL_KEY" python scripts/generate.py ...`
  ❌ `FAL_KEY="07138a1e-..." python scripts/generate.py ...`

(Run in foreground, not background, to avoid env-var drop issues)

### Direct Python API (fal_client v1.0.0)

You can bypass `generate.py` and call FAL directly with synchronous API — useful for quick scripts or when you need precise control over parameters:

```python
import fal_client

# Upload a reference image to FAL CDN (SYNCHRONOUS in v1.0.0, do NOT await)
image_url = fal_client.upload_file('/absolute/path/to/reference.png')

# Image-to-image with Nano Banana Pro Edit
result = fal_client.run('fal-ai/nano-banana-pro/edit', arguments={
    'image_urls': [image_url],        # REQUIRED: ARRAY, not a single string
    'prompt': 'Your photography-grade prompt...',
    'strength': 0.85                   # 0.70-0.90 range; higher = more original image preserved
})

# Result shape: {'images': [{'url': '...', ...}], 'description': 'model reasoning'}
output_url = result['images'][0]['url']
```

**Key gotchas with direct API:**
- `image_urls` is ALWAYS an array: `[url]` even for a single image. Using `'image_url': url` (string, not array) returns HTTP 422.
- `upload_file` is synchronous — do NOT `await` it. It returns the URL string directly.
- Must use the host filesystem path — on Windows: `C:/Users/<user>/file.png`, NOT `/tmp/file.png`
- Result dict has `images[].url` (not `image.url`). The `description` field holds the model's reasoning.

---

## Model selection

Default for product/ad work: run **both** Nano Banana Pro Edit (`image_urls` array) and Ideogram v4 I2I (`image_url` string) per concept. Cost is ~$0.28/concept. One image per chat message.

- Registry: [references/endpoint-models.md](references/endpoint-models.md)
- Input field shapes: [references/model-input-formats.md](references/model-input-formats.md)
- Photography language: [references/photography-lexicon.md](references/photography-lexicon.md)
- Conversion strategy (3 concepts, identity anchor, strength): [references/high-conversion-prompting.md](references/high-conversion-prompting.md)

Reference image present → image-to-image only. Never fall back to text-to-image.
No reference → Ideogram v4 T2I, optional Nano Banana T2I for variety.

## Dual-model delivery

For each concept, two images in **separate** messages (Telegram shows only the first image in a batch):

1. Nano Banana — Concept N
2. Ideogram v4 — Concept N

Ads use the 3-concept set in `high-conversion-prompting.md` (Ingredient Story, Spa/Lifestyle, Macro).

---

## Workflow (3-Phase, Agent Must Complete All)

### Phase 1: Intent Analysis & Strategy

1. **Analyse the brief** — What's the output format? (Instagram square, story, carousel, banner)
2. **If a product URL is provided:** Navigate to the page and extract:
   - Product name and description
   - Primary product image(s) at highest resolution
   - Brand colours and aesthetics
   
   **⚠️ Wix / JS-heavy site fallback:** If the browser tool errors out (blank page, WinError), the site is likely a Wix SPA. Do NOT retry the browser — switch to `curl + grep` to extract `wixstatic.com` image URLs from the raw HTML. See `references/wix-product-image-extraction.md` for the full recipe. Download images to `C:/Users/<user>/` not `/tmp/` (fal_client upload_file needs native Windows paths for `os.path.getsize`).
3. **If a reference image is provided (URL or file):** Classify the capability as `image-edit` (image-to-image) to preserve the subject's identity. The reference image becomes the foundation.
4. **Classify into capability branch:**
   - `image` — text-to-image generation (no reference image provided)
   - `image-edit` — image-to-image editing (reference image IS provided — ALWAYS prefer this)
   - `video` — animate an existing image into video
   - `upscale` — sharpen + enlarge an existing image or video
5. **This is an Instagram ad brief** — Default to the full Instagram Ad Creative Strategy (3-Concept Framework, dual-model generation, 1 image per message delivery). Run the strategy before proceeding.
6. **Intelligent model routing** — When an image-to-image reference is provided, ALWAYS use both Nano Banana Pro Edit + Ideogram v4 I2I in parallel. See the Model Selection section above for exact endpoint parameters.
7. **Cost-capability trade-off** — Cross-reference with `references/cost-reference.md`. State the total cost (~$0.85 for a full 3-concept set with both models). Note: costs are negligible, no need to pre-approve image runs.

### Phase 2: Prompt Engineering

1. **Refine the user's description into a photography-grade prompt** using the Prompt Craft terms above.
2. **Structure: Camera → Lens → Aperture → Lighting → Subject → Surface → Props → Composition → Mood**
3. **For image-to-image (reference provided):**
   - The prompt describes what to CHANGE or ADD to the reference image
   - Be explicit about preservation: "while maintaining the same product shape, colors, and texture"
   - Use specific verbs: "place the soap on a marble surface" over "transform the scene"
4. **For text-to-image (no reference):**
   - Full scene description from scratch using photography language
5. **Show the user the refined prompt.** Ask: "Run this, or want to adjust?"

### Phase 3: Execution

**CRITICAL: FAL_KEY must be passed inline.** Background processes lose the env var. Always run in foreground:

```bash
# Image-to-image (with reference image):
FAL_KEY="$FAL_KEY" python scripts/generate.py image \
  --endpoint "fal-ai/nano-banana-pro/edit" \
  --prompt "refined prompt here" \
  --title "slug" \
  --aspect-ratio "1:1" \
  --input-image /path/to/reference.png

# Text-to-image (no reference):
FAL_KEY="$FAL_KEY" python scripts/generate.py image \
  --endpoint "fal-ai/flux-2/klein/9b" \
  --prompt "refined prompt here" \
  --title "slug" \
  --aspect-ratio "1:1"

# For brand-color precision, add HEX: "in color #E8D5C4 and #C27A8A"
```

---

## Commands

Set shorthand: `GEN="FAL_KEY=\"$FAL_KEY\" python scripts/generate.py"`

### Image (text-to-image)
```bash
$GEN image --endpoint "fal-ai/flux-2/klein/9b" --prompt "..." --title "slug" --aspect-ratio "1:1"
```

### Image Edit (image-to-image — preferred when reference image exists)
```bash
$GEN image --endpoint "fal-ai/nano-banana-pro/edit" --prompt "..." --title "edit" --input-image /path/to/reference.png
```

### Video
```bash
$GEN video --endpoint "bytedance/seedance-2.0/image-to-video" --image /path/to/image.png --prompt "motion" --title "slug" --folder /path/gen --duration 5
```

### Upscale
```bash
$GEN upscale --endpoint "fal-ai/topaz/upscale/image" --input /path/to/image.png --factor 2
$GEN upscale --endpoint "fal-ai/topaz/upscale/video" --input /path/to/video.mp4 --target-height 1080 --fps 30
```

---

## Output Structure

```
~/Documents/Media Gen/2026-07-09-japanese-garden/
├── prompt.md            # Full metadata: prompts, model, params, timestamps
├── image-01.png
└── video-01.mp4         # Only if video step ran
```

---

## Cost Quoting (Mandatory for Video)

- **Image gen**: ~$0.02-0.10/image — state cost, run autonomously after confirmation
- **Video gen**: MUST quote cost before running. Formula:
  `{model} = ${price_per_second}/s × {duration}s × {N} videos = ${total}`
  Use `references/cost-reference.md` for current pricing.
  Wait for explicit yes.
- **Video upscale**: Same rule. Topaz bills per tier:
  ≤720p: $0.01/s | ≤1080p: $0.02/s | >1080p: $0.08/s
  Price DOUBLES at 60fps. Use `--fps 30` to halve cost.

---

## Leading Words Reference

| Leading Word | Meaning | When to Use |
|---|---|---|
| **intent-matched execution** | Align tool/model choice exactly with user's stated goal | Before model selection |
| **intelligent model routing** | Evaluate task complexity and route to the right endpoint | During Phase 1 step 3 |
| **cost-capability trade-off** | Explicitly weigh quality/speed/cost before committing | During Phase 1 step 4 |
| **task-complexity triage** | Classify the difficulty of the generation request | Before reading reference files |
| **prompt craft** | Use photography language (lens, aperture, lighting, ISO) | During Phase 2 prompt engineering |

---

## Pitfalls

1. **FAL_KEY must use shell expansion — hardcoding the literal key fails** — Always use `FAL_KEY="$FAL_KEY"` not `FAL_KEY="literal_key_string"`. The shell variable may contain extra characters or the key may be rotated. Shell expansion resolves correctly; hardcoded strings return 401.
2. **fal-client version matters** — CDN upload for image-to-image requires fal-client >= 1.0.0. v0.13.1 breaks `rest.fal.ai/storage/auth/token` with 405. Upgrade: `pip install --upgrade fal-client`
3. **Reference image provided → MUST use image-to-image** — Never use text-to-image when a product URL or reference image is available. The edit endpoints preserve product identity.
4. **Model endpoint not found** — Fal.ai may have renamed/deprecated it. Check fal.ai/models
5. **Response schema changed** — Update `output_path` mapping in references if Fal changes the API
6. **Upload limit** — Fal accepts files up to 10MB. Downscale large images before uploading as references
7. **Rate limits / queue** — Images <30s, videos 1-3 min. Warn user if >5 min
8. **No default model** — Do NOT pick a hardcoded default. Always reason through model selection
9. **Do not auto-animate** — Always ask "Want to turn this into a video?" after image generation
10. **Default duration is 5s** — Never propose 10s as a first option. Only escalate if user asks after seeing the 5s draft
11. **Instagram ads skip strategy** — NEVER skip the Instagram Ad Creative Strategy. Always plan the ad set before generating.
12. **Nonsensical product scenes** — Don't put a soap bar beside a coffee cup or create other pairings that don't make sense. The product must be shown in its actual use context (soap → shower/bath, not coffee drinking). Think like a marketing person: what story does this scene tell about the product?
13. **Nano Banana Pro Edit uses `image_urls` (array), NOT `image_url` (string)** — Passing `image_url: url` as a single string returns HTTP 422. Always use `image_urls: [url]` even for a single reference image.
14. **Wix / JS-heavy product pages break the browser tool** — Do NOT retry the browser. Switch immediately to `curl + grep wixstatic.com`. See `references/wix-product-image-extraction.md`.
15. **fal_client v1.0.0 `upload_file` is synchronous** — On Windows, pass an absolute path like `C:/Users/<user>/file.png`, not `/tmp/file.png`. The function calls `os.path.getsize()` which resolves against the native filesystem, not MSYS. Do NOT `await` it.
17. **`fal_client.run()` is the synchronous replacement for `subscribe()`** — `run_sync` does not exist in v1.0.0. Use `run()` directly without await.
18. **1 image per message** — Telegram and similar platforms may only render the first image in a multi-image message. Always send 1 image per message.
19. **Ideogram v4 I2I uses `image_url` (string), Nano Banana Pro Edit uses `image_urls` (array)** — Mixing these up returns 422. Always double-check the input field name.
20. **Cost data is in `x-fal-billable-units` response header, not the response body** — Use `resp.headers.get('x-fal-billable-units')` to get exact billable units. 1 unit = $0.15 USD.
21. **Both models together cost ~$0.28 per concept** — Run both freely. The total for a full 3-concept ad set (6 images) is ~$0.85.

---

## References

- `references/photography-lexicon.md` — Camera, lens, lighting; points at BFL + conversion templates
- `references/fal-key-troubleshooting.md` — FAL key formats, endpoint access, recovery steps, CDN fix
- `references/model-input-formats.md` — Which models accept which image input fields (image_url vs image_urls[]), plus `strength` parameter range for I2I
- `references/ad-psychology-guide.md` — Deep psychology: color emotion, subliminal cues, scanning patterns, persuasion, stop-scroll triggers
- `references/high-conversion-prompting.md` — Psychology, color theory, composition, identity anchor, strength tables, troubleshooting
- `references/wix-product-image-extraction.md` — Extracting product images from Wix JS-heavy sites using curl+grep
- `references/cost-reference.md` — Pricing tables for cost-capability trade-off
- `scripts/generate.py` — CLI script (image | video | upscale subcommands)
- `config.json` — Output directory config
- BFL Prompting Guide: https://docs.bfl.ml/guides/prompting_summary.md
- BFL Prompt Reference: https://docs.bfl.ml/guides/prompting_unified_reference.md
- BFL Photorealism Guide: https://docs.bfl.ml/guides/usecases_t2i_photorealistic.md
- Fal.ai model browser: https://fal.ai/models