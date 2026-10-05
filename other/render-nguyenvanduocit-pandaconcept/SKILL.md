---
name: render
description: Send image generation prompts to AI providers and collect outputs. Use when the user wants to actually generate interior design images via API calls.
---

# Render Interior Design Images

Execute image generation by sending prompts to AI provider APIs and managing the output.

## CRITICAL — Read Before Writing Any Code

1. **Gemini model**: ALWAYS use `gemini-3.1-flash-image-preview`. NO other model name. Do NOT guess or use `gemini-2.0-*`, `gemini-2.5-*`, or any other variant — they will fail with misleading errors (Google returns "API key expired" or 404 when a model doesn't exist).
2. **API keys**: Read from `CLAUDE.local.md` first (check for `**Gemini**:` line), then fall back to environment variables. NEVER ask user for a key that's already in `CLAUDE.local.md`.
3. **SDK**: Use `google-genai` (`from google import genai`), NOT `google.generativeai`.
4. **Copy code examples below exactly** — do not write API calls from memory.

## Prerequisites

- API keys in `CLAUDE.local.md` or environment variables (see CLAUDE.md)
- Python environment with provider SDKs installed

## Auto-Routing (MANDATORY — do NOT skip)

**Before rendering**, run these checks to detect the rendering mode automatically:

```
!ls projects/${PROJECT_NAME}/references/masks/*.png 2>/dev/null && echo "HAS_MASKS=true" || echo "HAS_MASKS=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/depth_map.png 2>/dev/null && echo "HAS_DEPTH=true" || echo "HAS_DEPTH=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/prompts/ 2>/dev/null && echo "HAS_PROMPTS=true" || echo "HAS_PROMPTS=false"
```

### Mode Selection (automatic — do NOT ask user)

Determine mode by checking **both** the available assets AND the user's intent:

```
HAS_MASKS=true?
└── INPAINTING MODE (mask + image + prompt → inpaint API)
    Providers: Stability AI /edit/inpaint, OpenAI DALL-E edit

HAS_DEPTH=true AND user wants REDESIGN (new style, different look)?
└── STRUCTURE CONTROL MODE (depth/control map + prompt → structure API)
    Providers: Stability AI /control/structure, Gemini (image editing with depth reference)

HAS_REFERENCE=true AND user wants EDIT (enhance, add details, adjust tone, fix elements)?
└── IMAGE EDITING MODE (reference image + edit instruction → Gemini editing)
    Provider: Gemini (send image + text prompt, no mask/depth needed)
    Use this when: "add details", "make more realistic", "brighter", "change color", "enhance"
    Gemini handles edits natively — no preprocessing required.

HAS_REFERENCE=true AND user wants REDESIGN AND HAS_DEPTH=false?
└── STOP. Run /preprocess-room FIRST. Do NOT redesign without control maps.

None of the above?
└── TEXT-TO-IMAGE MODE (prompt only)
    Providers: Any (OpenAI, Gemini, Stability, Grok)
```

**Key distinction**: EDIT ≠ REDESIGN.
- **Edit** = enhance/tweak the existing image (add details, adjust brightness, fix elements) → Gemini image editing, no preprocessing needed
- **Redesign** = apply a completely different style while keeping layout → needs depth map + structure control

**If control maps exist AND the task is a redesign, USE THEM.** Never fall back to text-to-image when structure data is available.

If `HAS_SEMANTIC=true`, read `semantic_analysis.json` to cross-check that the prompt matches the room's actual characteristics (style, materials, lighting). Warn if prompt contradicts analysis data.

**Provider routing by mode:**
- **Inpainting**: Stability AI (`/edit/inpaint`) or OpenAI (DALL-E edit) — ONLY these support masks
- **Structure control**: Stability AI (`/control/structure`) or Gemini (image editing with depth reference) — best layout fidelity
- **Image editing**: Gemini (`gemini-3.1-flash-image-preview`) — send reference image + text instruction directly
- **Text-to-image**: Any provider (OpenAI, Gemini, Stability, Grok)

## Workflow

### Step 1: Input
Accept via `$ARGUMENTS` or ask:
- **Prompt**: a ready-to-use prompt (or reference a previous `/generate-prompt` output)
- **Provider(s)**: which AI provider(s) to use — or "all" for comparison
- **Parameters**: image size, quality, number of variations

### Step 2: Provider-Specific API Calls

For each provider, construct the appropriate API call:

**OpenAI (DALL-E 3)**:
```python
from openai import OpenAI
client = OpenAI()
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",  # wide for rooms
    quality="hd",
    n=1
)
```

**Google Gemini (Image Generation / Editing)**:
```python
from google import genai
from google.genai import types
from PIL import Image
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Text-to-image (no reference)
response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt],
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
)

# Image editing / redesign — send ALL available visual context
# Gemini is multimodal: the more context images you send, the better it understands the room
ref_image = Image.open(image_path)

contents = [ref_image, "This is the original room photo.\n"]

# Attach preprocessed maps if available (check preprocessed/${IMAGE_NAME}/ folder)
preprocessed_dir = f"projects/{project_name}/references/preprocessed/{image_name}"

depth_path = os.path.join(preprocessed_dir, "depth_map.png")
if os.path.exists(depth_path):
    contents.append(Image.open(depth_path))
    contents.append("This is the depth map showing spatial structure and distances.\n")

seg_path = os.path.join(preprocessed_dir, "segmentation.png")
if os.path.exists(seg_path):
    contents.append(Image.open(seg_path))
    contents.append("This is the segmentation map showing distinct zones (walls, floor, ceiling, furniture).\n")

# Attach mask if available (for targeted edits)
mask_dir = f"projects/{project_name}/references/masks"
if os.path.exists(mask_dir):
    import glob
    mask_files = glob.glob(os.path.join(mask_dir, "*.png"))
    for mask_file in mask_files:
        contents.append(Image.open(mask_file))
        mask_name = os.path.basename(mask_file).replace("_mask.png", "").replace(".png", "")
        contents.append(f"This is a mask highlighting the '{mask_name}' area (white = area to change).\n")

# Add the actual prompt last
contents.append(edit_prompt)

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=contents,
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"]),
)

# Extract output image
for part in response.candidates[0].content.parts:
    if part.inline_data:
        with open(output_path, "wb") as f:
            f.write(part.inline_data.data)
```
> **SDK**: Use `google-genai` (`pip install google-genai`), NOT the deprecated `google.generativeai`.
> Gemini is multimodal — send ALL available context (original + depth + segmentation + masks) for best results. The more visual context, the better AI understands room structure and generates accurate designs.

**Stability AI**:
```python
import requests
response = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={"Authorization": f"Bearer {api_key}"},
    files={"none": ""},
    data={"prompt": prompt, "negative_prompt": negative, "output_format": "png"}
)
```

**Grok (xAI)**:
```python
from openai import OpenAI  # xAI uses OpenAI-compatible API
client = OpenAI(api_key=os.environ["GROK_API_KEY"], base_url="https://api.x.ai/v1")
response = client.images.generate(model="grok-2-image", prompt=prompt)
```

### Step 2B: Layout-Controlled Rendering (when reference photo exists)

When the project has preprocessed control maps (from `/preprocess-room`), use layout-controlled APIs instead of plain text-to-image. These APIs accept a reference image (depth map or edge map) alongside the prompt, allowing the model to preserve the original room's spatial structure while applying the new design style.

**Stability AI Structure Control** (recommended — no GPU needed):
```python
import requests

def render_with_structure(prompt, reference_image_path, api_key, control_strength=0.7):
    """Render with room layout preservation via Stability AI structure control."""
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/control/structure",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "image/*"},
        files={"image": open(reference_image_path, "rb")},
        data={
            "prompt": prompt,
            "control_strength": control_strength,
            "output_format": "png"
        }
    )
    if response.status_code == 200:
        return response.content  # Raw PNG bytes
    raise Exception(f"Stability API error: {response.status_code} {response.text}")
```

**Stability AI Inpainting** (for masked edits from `/mask-room`):
```python
def render_inpaint(prompt, image_path, mask_path, api_key):
    """Inpaint specific masked region while preserving the rest."""
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/edit/inpaint",
        headers={"Authorization": f"Bearer {api_key}", "Accept": "image/*"},
        files={
            "image": open(image_path, "rb"),
            "mask": open(mask_path, "rb")
        },
        data={"prompt": prompt, "output_format": "png"}
    )
    return response.content
```

### Step 3: Output Management
- Save generated images to `output/[style]/[provider]/[timestamp].png`
- Display image paths and metadata
- Log prompt + parameters + provider for reproducibility

### Step 4: Auto-Validate Layout (for REDESIGN renders only)

**After rendering a REDESIGN** (not edit/text-to-image), automatically run `/validate-layout` if a reference image + depth map exist. Do NOT ask user — just do it.

```python
# Auto-validate after redesign render
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def auto_validate(original_path, rendered_path, output_dir, render_name):
    orig = cv2.imread(original_path)
    render = cv2.imread(rendered_path)
    h, w = render.shape[:2]
    orig_resized = cv2.resize(orig, (w, h))

    gray_orig = cv2.cvtColor(orig_resized, cv2.COLOR_BGR2GRAY)
    gray_render = cv2.cvtColor(render, cv2.COLOR_BGR2GRAY)

    # SSIM
    score, ssim_map = ssim(gray_orig, gray_render, full=True)

    # SSIM heatmap
    ssim_visual = np.uint8((1 - ssim_map) * 255)
    cv2.imwrite(f'{output_dir}/diff_{render_name}_ssim.png',
                cv2.applyColorMap(ssim_visual, cv2.COLORMAP_JET))

    # Edge comparison
    edges_orig = cv2.Canny(cv2.GaussianBlur(gray_orig, (5,5), 0), 50, 150)
    edges_render = cv2.Canny(cv2.GaussianBlur(gray_render, (5,5), 0), 50, 150)
    edge_cmp = np.zeros((h, w, 3), dtype=np.uint8)
    edge_cmp[:,:,1] = edges_orig
    edge_cmp[:,:,2] = edges_render
    cv2.imwrite(f'{output_dir}/diff_{render_name}_edges.png', edge_cmp)

    # Overlay
    overlay = cv2.addWeighted(orig_resized, 0.5, render, 0.5, 0)
    cv2.imwrite(f'{output_dir}/diff_{render_name}_overlay.png', overlay)

    status = 'PASS' if score >= 0.70 else 'FAIL'
    print(f'Layout validation: {status} (SSIM={score:.4f})')
    if score < 0.70:
        print('⚠ Layout deviation — consider increasing control_strength or using structure control API')
    return score, status
```

Skip validation when:
- Mode is IMAGE EDITING (simple enhance/tweak via Gemini)
- Mode is TEXT-TO-IMAGE (no reference to compare)
- User explicitly says "don't validate"

### Step 5: Results Summary
Present results:
- Which providers succeeded/failed
- Image file paths
- Layout validation score (if auto-validated)
- Cost estimate per generation (if available)
- Suggest `/compare-models` if multiple providers were used
- Suggest `/refine` if the user wants to iterate

## Error Handling
- Missing API key: tell user which env var to set
- Rate limiting: suggest waiting or trying another provider
- Content filtering: adjust prompt and retry
- API errors: show error details and suggest fixes

## Session Relevant Skills

- `/compare-models` — if multiple providers were used, suggest /compare-models to evaluate outputs side-by-side. This is the natural next step after multi-provider rendering.
- `/refine` — if the user is unhappy with the output, /refine takes the prompt + feedback and generates an improved version. Don't manually tweak prompts — /refine tracks iteration history.
- `/generate-prompt` — if no prompt is provided, redirect to /generate-prompt first. Don't accept vague descriptions as render input — proper prompt engineering makes the difference.
- `/edit-design` — if the user wants to modify a rendered result, /edit-design analyzes the output image and generates targeted edit prompts.
- `/style-guide` — reference when troubleshooting style accuracy issues. If renders don't match the expected style, check if the right keywords were used.
- `/preprocess-room` — run this FIRST when working with a reference room photo. It generates depth maps and edge maps that enable layout-controlled rendering.
- `/mask-room` — generates masks for targeted inpainting. Use with the inpainting API calls above.
- `/validate-layout` — run AFTER rendering to verify the generated image preserved the original room layout.

## Gotchas

- **Always save before displaying**: Save images to `output/[style]/[provider]/` before showing results. If the API returns URLs (OpenAI, Grok), download them — URLs expire.
- **Don't render without a proper prompt**: Vague inputs like "make a nice living room" produce poor results. Redirect to /generate-prompt. BUT for image editing mode (enhance, brighten, add details), a natural language instruction IS a valid prompt.
- **API keys**: Read from `CLAUDE.local.md` FIRST (parse the markdown for key values), then fall back to env vars. Each provider needs its own key.
- **Gemini model — ONLY `gemini-3.1-flash-image-preview`**: This is the ONLY model that supports image generation/editing. Other model names (`gemini-2.0-*`, `gemini-2.5-*`) will fail. Google returns MISLEADING errors — "API key expired" or 404 — when the model doesn't exist. If you see "API key expired", check the model name FIRST before blaming the key.
- **Edit vs Redesign**: When user wants to enhance/tweak an existing image (add details, adjust brightness, more realistic), use Gemini image editing directly — do NOT require `/preprocess-room`. Only require preprocessing for full style redesign.
- **Cost awareness**: DALL-E HD costs ~$0.08/image, Stability ~$0.03, Grok varies. Warn the user before "render all providers".
- **Layout-controlled rendering requires preprocessing first**: For REDESIGN tasks only. Don't skip `/preprocess-room` when changing styles. Without control maps, you can't guarantee layout preservation.
- **control_strength tuning**: Start at 0.7 for Stability structure. Higher = more layout fidelity but less style freedom. Lower = more creative but may distort room shape.
- **Inpainting needs both image AND mask**: The mask from `/mask-room` defines what changes. White pixels = edit zone, black = preserve.
