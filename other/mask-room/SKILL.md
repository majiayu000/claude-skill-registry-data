---
name: mask-room
description: Create precise masks for targeted room editing using fal.ai SAM segmentation. Use when the user wants to change specific elements (furniture, walls, floor) while keeping everything else intact.
---

# Mask Room Elements for Inpainting

Generate precise binary masks that isolate specific room elements for inpainting. Instead of regenerating the entire room, masks allow surgical edits — change only the sofa, repaint only the walls, replace only the flooring — while preserving everything else pixel-perfectly.

All masking uses **fal.ai SAM API** (`fal-ai/imageutils/sam`) — no local GPU, model downloads, or torch required.

## Pre-flight Checks (MANDATORY — run before masking)

**Before masking**, check what resources are available to choose the best method.

Derive `IMAGE_NAME` from the source image filename (e.g., `room.jpg` → `room`, `PN_MASTER_2.png` → `PN_MASTER_2`).

```
!ls projects/${PROJECT_NAME}/references/preprocessed/${IMAGE_NAME}/segmentation.png 2>/dev/null && echo "HAS_SEGMENTATION=true" || echo "HAS_SEGMENTATION=false"
```

```
!ls projects/${PROJECT_NAME}/references/masks/*.png 2>/dev/null && echo "HAS_EXISTING_MASKS=true" || echo "HAS_EXISTING_MASKS=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/renders/*.png 2>/dev/null && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"
```

### Decision Logic

```
HAS_REFERENCE=false AND HAS_RENDERS=false?
└── STOP. No source image to mask. Ask user to provide an image.

HAS_EXISTING_MASKS=true?
└── List existing masks. Ask user: reuse existing mask, create new one, or combine?

Target is a zone (wall, floor, ceiling) AND HAS_SEGMENTATION=true?
└── Use Method 2 (Color-based extraction from existing segmentation) — instant, no API call.

Target is a zone BUT HAS_SEGMENTATION=false?
└── Run /preprocess-room first (segmentation only) — then use Method 2.
    OR use Method 1 (SAM text-prompted) for immediate results.

Target is a specific object (sofa, lamp, plant)?
└── Use Method 1 (SAM text-prompted via fal.ai) — best for individual objects.
```

**Choose the lightest method that achieves the goal.** Zone masking from existing segmentation is instant; SAM API calls cost time and credits.

## Input

Gather from the user (ask if not provided via `$ARGUMENTS`):
1. **Room photo**: original or rendered image to mask
2. **Target element(s)**: what to isolate — "sofa", "walls", "floor", "ceiling", "windows", or custom description
3. **Mask output path** (default: `references/masks/`)

## Masking Methods

### Method 1: SAM via fal.ai (Text/Auto-Prompted)

Best for specific objects or when no segmentation map exists. Uses `fal-ai/imageutils/sam` endpoint.

```python
import fal_client, os, requests
import numpy as np
from PIL import Image

def mask_by_sam(image_path: str, output_path: str, fal_key: str):
    """Generate automatic segmentation mask via fal.ai SAM."""
    os.environ['FAL_KEY'] = fal_key

    # Upload image to fal.ai
    image_url = fal_client.upload_file(image_path)

    # Run SAM automatic segmentation
    result = fal_client.subscribe(
        "fal-ai/imageutils/sam",
        arguments={"image_url": image_url}
    )

    # Download full segmentation
    resp = requests.get(result['image']['url'])
    with open(output_path, 'wb') as f:
        f.write(resp.content)
    return output_path
```

After getting the SAM segmentation, extract the target element by color matching (see Method 2).

### Method 2: Color-Based Extraction from Segmentation Map

Best for masking zones when a segmentation map already exists (from `/preprocess-room` or Method 1). Each zone in the SAM output has a distinct color — extract the target zone by matching its color.

```python
import numpy as np
from PIL import Image

def mask_by_color(segmentation_path: str, target_color_rgb: tuple, output_path: str, tolerance: int = 30):
    """Extract a binary mask from segmentation map by matching a specific color.

    Args:
        segmentation_path: Path to SAM segmentation output
        target_color_rgb: RGB color of the zone to mask (e.g., (200, 100, 150) for ceiling)
        output_path: Where to save binary mask
        tolerance: Color matching tolerance (default 30 — increase for gradients)
    """
    seg = np.array(Image.open(segmentation_path).convert("RGB"))

    # Color distance matching
    diff = np.sqrt(np.sum((seg.astype(float) - np.array(target_color_rgb).astype(float)) ** 2, axis=2))
    mask = (diff < tolerance).astype(np.uint8) * 255

    Image.fromarray(mask).save(output_path)
    return mask

def mask_multiple_colors(segmentation_path: str, target_colors: list, output_path: str, tolerance: int = 30):
    """Combine multiple color zones into one mask (e.g., all wall sections)."""
    seg = np.array(Image.open(segmentation_path).convert("RGB"))
    combined_mask = np.zeros(seg.shape[:2], dtype=np.uint8)

    for color in target_colors:
        diff = np.sqrt(np.sum((seg.astype(float) - np.array(color).astype(float)) ** 2, axis=2))
        combined_mask = np.maximum(combined_mask, (diff < tolerance).astype(np.uint8) * 255)

    Image.fromarray(combined_mask).save(output_path)
    return combined_mask
```

### How to identify zone colors

To find the color of a specific zone in the segmentation map:

```python
from PIL import Image
import numpy as np
from collections import Counter

def list_segmentation_colors(segmentation_path: str, top_n: int = 20):
    """List the most common colors in a segmentation map to identify zones."""
    seg = np.array(Image.open(segmentation_path).convert("RGB"))
    pixels = seg.reshape(-1, 3)
    color_counts = Counter(map(tuple, pixels))

    print("Top colors in segmentation (RGB → approximate zone):")
    for color, count in color_counts.most_common(top_n):
        pct = count / len(pixels) * 100
        print(f"  RGB{color} — {pct:.1f}% of image")
```

**Workflow**: Run `list_segmentation_colors()` → show user the color map → user identifies which color = which zone → extract mask by color.

Alternatively, use Gemini Vision to identify which color corresponds to which element by analyzing the segmentation map alongside the original image.

## Mask Post-Processing

```python
import cv2, numpy as np
from PIL import Image

def refine_mask(mask_path: str, output_path: str, dilate_px: int = 5, feather_px: int = 3):
    """Clean up mask: remove small holes, smooth edges, add feathering."""
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Fill small holes
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilate_px, dilate_px))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Smooth edges
    mask = cv2.GaussianBlur(mask, (feather_px*2+1, feather_px*2+1), 0)

    # Re-threshold
    _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

    cv2.imwrite(output_path, mask)
```

## Using Masks with Providers

### Stability AI Inpainting

```python
import requests

def inpaint_stability(image_path, mask_path, prompt, api_key):
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={"Authorization": f"Bearer {api_key}"},
        files={"image": open(image_path, "rb"), "mask": open(mask_path, "rb")},
        data={"prompt": prompt, "output_format": "png"}
    )
    return response.content
```

### OpenAI DALL-E Edit

```python
from openai import OpenAI

def inpaint_openai(image_path, mask_path, prompt):
    client = OpenAI()
    response = client.images.edit(
        image=open(image_path, "rb"),
        mask=open(mask_path, "rb"),
        prompt=prompt,
        size="1024x1024"
    )
    return response.data[0].url
```

## Output

```
references/masks/
├── wall_mask.png          # Binary mask: white = walls
├── floor_mask.png         # Binary mask: white = floor
├── sofa_mask.png          # Binary mask: white = sofa area
├── custom_mask.png        # User-prompted mask
└── mask_overlay.png       # Visualization: original + mask overlay
```

## Workflow

1. User identifies what to change: "change just the sofa" or "repaint the walls"
2. `/mask-room` generates precise binary mask for that element
3. `/render` uses mask + prompt for inpainting (Stability AI or OpenAI)
4. Only masked area changes — rest of image preserved pixel-perfectly

## Session Relevant Skills

- `/preprocess-room` — generates segmentation map (via fal.ai SAM) that `/mask-room` can reuse for zone-based masking
- `/render` — consumes masks for inpainting API calls
- `/edit-design` — generates the edit prompt; `/mask-room` generates the mask; `/render` executes
- `/validate-layout` — verify masked edits preserved layout

## Gotchas

- **No local models needed**: All masking uses fal.ai SAM API (`fal-ai/imageutils/sam`). No torch, no model checkpoints, no GPU.
- **Reuse existing segmentation**: If `/preprocess-room` already ran, the segmentation map is at `references/preprocessed/${IMAGE_NAME}/segmentation.png` — extract masks by color instead of calling SAM again.
- Point/box prompts are NOT supported by `fal-ai/imageutils/sam` — it runs automatic mode only. For specific objects, run SAM auto → then extract the target zone by its color in the output.
- For walls: may need to combine multiple color zones (left wall, back wall, right wall may be different colors in segmentation).
- Mask must be same resolution as source image.
- White = area to EDIT, Black = area to KEEP (standard inpainting convention).
- Feathering the mask edges by 3-5px produces smoother inpainting transitions.
- Some providers require RGBA PNG with transparency instead of separate mask — check provider docs.

## Dependencies

```
pip install fal-client opencv-python-headless pillow requests
```

- fal.ai API key required (from `FAL_KEY` env var or `CLAUDE.local.md`)
- No torch, transformers, or SAM2 local install needed
