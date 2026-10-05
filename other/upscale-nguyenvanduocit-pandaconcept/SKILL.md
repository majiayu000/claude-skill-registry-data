---
name: upscale
description: Upscale rendered images to 4K+ resolution using fal.ai Clarity Upscaler. Use when the user wants to upscale, enhance resolution, make images sharper, or increase image size.
---

# Upscale Images

Upscale rendered interior design images to 4K+ resolution using fal.ai's Clarity Upscaler — tunable resemblance/creativity for architectural photography.

## Prerequisites

- fal.ai API key configured in `CLAUDE.local.md`
- Python with `fal_client` and `Pillow` installed

## Input

Accept via `$ARGUMENTS` or ask:
- **Image path**: path to the image to upscale (relative to project renders, or absolute)
- **Scale factor**: 2x or 4x (default: auto — pick scale so output is ~4K)

If the user says "upscale" without specifying an image, use the **most recently created** file in `projects/${PROJECT_NAME}/renders/`.

## API Details

**Provider**: fal.ai
**Model**: `fal-ai/clarity-upscaler`
**Capability**: 1-4x upscale, adjustable resemblance (0-1) and creativity (0-1), prompt-guided

## Workflow

### Step 1: Resolve Image

```python
import os, glob

# If no image specified, find most recent render
renders_dir = f"projects/{project_name}/renders"
files = sorted(glob.glob(os.path.join(renders_dir, "*.png")), key=os.path.getmtime, reverse=True)
# Exclude already-upscaled files
files = [f for f in files if "_4k_" not in os.path.basename(f) and "_upscaled_" not in os.path.basename(f)]
input_path = files[0]
```

### Step 2: Auto-detect Scale

```python
from PIL import Image

img = Image.open(input_path)
w, h = img.width, img.height
target = 3840  # 4K width

if w >= target:
    scale = 2  # already large, 2x is enough
elif w * 4 <= target * 1.5:
    scale = 4
else:
    scale = 2
```

### Step 3: Upload & Upscale

```python
import fal_client
from datetime import datetime

# Read API key from CLAUDE.local.md
os.environ["FAL_KEY"] = "<fal_api_key_from_claude_local_md>"

image_url = fal_client.upload_file(input_path)

result = fal_client.subscribe("fal-ai/clarity-upscaler", arguments={
    "image_url": image_url,
    "scale": scale,
    "resemblance": 0.9,   # high = faithful to original
    "creativity": 0.2,     # low = minimal hallucination
    "prompt": "photorealistic interior design, architectural photography, sharp details, high resolution",
})

# Download result
import urllib.request
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
basename = os.path.splitext(os.path.basename(input_path))[0]
out_path = os.path.join(renders_dir, f"{basename}_4k_{timestamp}.png")

urllib.request.urlretrieve(result["image"]["url"], out_path)

w = result["image"].get("width", "?")
h = result["image"].get("height", "?")
size_mb = os.path.getsize(out_path) / (1024 * 1024)
print(f"Upscaled: {w}x{h} ({size_mb:.1f} MB)")
print(f"Saved: {out_path}")
```

### Step 4: Output

- Save upscaled image to same `renders/` directory with `_4k_` suffix
- Display the upscaled image to the user
- Report: original resolution → new resolution, file size

## Output Naming Convention

```
{original_name}_4k_{timestamp}.png
```

## Tuning Parameters

| Param | Default | Range | Effect |
|-------|---------|-------|--------|
| `scale` | auto | 1-4 | Upscale factor — auto-picks based on input size to target ~4K |
| `resemblance` | 0.9 | 0-1 | How faithful to original — 0.9 for interior design (preserve colors/layout) |
| `creativity` | 0.2 | 0-1 | How much AI "enhances" — keep low for architecture to avoid hallucination |
| `prompt` | (interior design) | text | Guides the upscaler — include relevant style keywords |

## Gotchas

- **Clarity Upscaler is the correct model** — `fal-ai/clarity-upscaler`. Controllable scale, resemblance, creativity.
- **Auto-scale logic** — If input is already large (≥3840px wide), use scale=2. For ~1200px inputs, use scale=4. Prevents absurdly large outputs.
- **Large output files** — 4K PNGs can be 15-25 MB. Warn the user if disk space is a concern.
- **Skip already-upscaled images** — Filter out files with `_4k_` or `_upscaled_` in the name.
- **API key** — Read from `CLAUDE.local.md`, field `fal.ai`.
- **Fallback** — If Clarity fails, fall back to `fal-ai/aura-sr` (fast GAN-based, fixed 4x, no params needed).

## Session Relevant Skills

- `/render` — generate images first, then upscale the best ones
- `/compare-models` — upscale the winning image after comparison
- `/refine` — if the upscaled image reveals quality issues not visible at low res, refine the prompt and re-render
