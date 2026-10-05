---
name: validate-layout
description: Verify that AI-generated interior designs preserve the original room layout by comparing depth maps and structural features. Use after rendering to check layout fidelity.
---

# Validate Layout Preservation

After generating a new design from a reference room photo, validate that the generated image preserves the original room's spatial layout — wall positions, furniture depth ordering, ceiling height, window placements.

Produces 5 visual diff outputs + quantitative scores. Auto-appends results to `notes.md`.

## Pre-flight Checks (MANDATORY)

Derive `IMAGE_NAME` from the source reference image filename (e.g., `PN_MASTER_2.png` → `PN_MASTER_2`).

```
!ls projects/${PROJECT_NAME}/references/preprocessed/${IMAGE_NAME}/depth_map.png 2>/dev/null && echo "HAS_ORIGINAL_DEPTH=true" || echo "HAS_ORIGINAL_DEPTH=false"
```

```
!ls projects/${PROJECT_NAME}/renders/*.png 2>/dev/null && echo "HAS_RENDERS=true" || echo "HAS_RENDERS=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

### Decision Logic

```
HAS_RENDERS=false?
└── STOP. No renders to validate. Run /render first.

HAS_REFERENCE=false?
└── STOP. No reference image. Cannot validate without original.

HAS_ORIGINAL_DEPTH=true?
└── Reuse existing depth map — skip re-extraction.

HAS_ORIGINAL_DEPTH=false?
└── Run /preprocess-room first (depth only) to get baseline depth map.
    Do NOT use local torch/MiDaS — always use fal.ai API via /preprocess-room.
```

## Input

Accept via `$ARGUMENTS` or ask:
1. **Project name**: which project
2. **Reference image**: original room photo (from `references/`)
3. **Render image(s)**: which render(s) to validate (from `renders/`)
4. **Threshold**: SSIM threshold (default: 0.70)

## Validation Script

Run this script for each render image to validate against the original:

```python
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import os

def validate_layout(original_path: str, rendered_path: str, output_dir: str, render_name: str = "render"):
    """
    Full layout validation: SSIM + pixel diff + edge comparison + overlay.
    Produces 5 visual outputs + quantitative scores.
    """
    # Load images
    orig = cv2.imread(original_path)
    render = cv2.imread(rendered_path)

    # Resize original to match render dimensions
    h, w = render.shape[:2]
    orig_resized = cv2.resize(orig, (w, h))

    gray_orig = cv2.cvtColor(orig_resized, cv2.COLOR_BGR2GRAY)
    gray_render = cv2.cvtColor(render, cv2.COLOR_BGR2GRAY)

    os.makedirs(output_dir, exist_ok=True)
    results = {}

    # --- 1. SSIM Score (structural similarity) ---
    score, ssim_map = ssim(gray_orig, gray_render, full=True)
    results['ssim_score'] = round(score, 4)
    results['ssim_rating'] = interpret_ssim(score)

    ssim_visual = np.uint8((1 - ssim_map) * 255)
    ssim_heatmap = cv2.applyColorMap(ssim_visual, cv2.COLORMAP_JET)
    heatmap_path = os.path.join(output_dir, f'diff_{render_name}_ssim_heatmap.png')
    cv2.imwrite(heatmap_path, ssim_heatmap)
    results['heatmap'] = heatmap_path

    # --- 2. Absolute pixel diff ---
    diff = cv2.absdiff(orig_resized, render)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff_amplified = cv2.normalize(diff_gray, None, 0, 255, cv2.NORM_MINMAX)
    diff_colored = cv2.applyColorMap(diff_amplified, cv2.COLORMAP_HOT)
    pixel_path = os.path.join(output_dir, f'diff_{render_name}_pixel.png')
    cv2.imwrite(pixel_path, diff_colored)
    results['pixel_diff'] = pixel_path

    # --- 3. Side-by-side ---
    side_by_side = np.hstack([orig_resized, render])
    sbs_path = os.path.join(output_dir, f'diff_{render_name}_side_by_side.png')
    cv2.imwrite(sbs_path, side_by_side)
    results['side_by_side'] = sbs_path

    # --- 4. Overlay blend (50/50) ---
    overlay = cv2.addWeighted(orig_resized, 0.5, render, 0.5, 0)
    overlay_path = os.path.join(output_dir, f'diff_{render_name}_overlay.png')
    cv2.imwrite(overlay_path, overlay)
    results['overlay'] = overlay_path

    # --- 5. Edge comparison (structural layout) ---
    edges_orig = cv2.Canny(cv2.GaussianBlur(gray_orig, (5, 5), 0), 50, 150)
    edges_render = cv2.Canny(cv2.GaussianBlur(gray_render, (5, 5), 0), 50, 150)

    edge_compare = np.zeros((h, w, 3), dtype=np.uint8)
    edge_compare[:, :, 1] = edges_orig     # green = original edges
    edge_compare[:, :, 2] = edges_render   # red = rendered edges
    # yellow where both overlap
    edges_path = os.path.join(output_dir, f'diff_{render_name}_edges.png')
    cv2.imwrite(edges_path, edge_compare)
    results['edges'] = edges_path

    # Edge IoU
    intersection = np.logical_and(edges_orig > 0, edges_render > 0).sum()
    union = np.logical_or(edges_orig > 0, edges_render > 0).sum()
    results['edge_iou'] = round(intersection / union, 4) if union > 0 else 0

    # Pixel change percentage
    results['pixels_changed_pct'] = round(np.mean(diff_gray > 30) * 100, 1)

    # Overall pass/fail
    results['overall'] = 'PASS' if score >= 0.70 else 'FAIL'
    results['recommendation'] = get_recommendation(score)

    return results


def interpret_ssim(score: float) -> str:
    if score >= 0.85: return "Excellent — layout nearly identical"
    if score >= 0.70: return "Good — layout preserved with minor variations"
    if score >= 0.55: return "Fair — noticeable layout differences"
    if score >= 0.40: return "Poor — significant layout deviation"
    return "Failed — layout not preserved"


def get_recommendation(score: float) -> str:
    if score >= 0.85:
        return "Layout excellent. Proceed with refinement or upscale."
    if score >= 0.70:
        return "Layout preserved. Minor variations acceptable for style change."
    if score >= 0.55:
        return "Layout shifted. Consider increasing control_strength or using structure control API."
    return "Layout lost. Re-render with depth map + structure control API. Check /preprocess-room output."
```

## Usage Example

```python
results = validate_layout(
    original_path="projects/prj2/references/PN_MASTER_2.png",
    rendered_path="projects/prj2/renders/japandi_v2.png",
    output_dir="projects/prj2/renders",
    render_name="japandi_v2"
)

print(f"SSIM: {results['ssim_score']} — {results['ssim_rating']}")
print(f"Edge IoU: {results['edge_iou']}")
print(f"Pixels changed: {results['pixels_changed_pct']}%")
print(f"Overall: {results['overall']}")
print(f"Recommendation: {results['recommendation']}")
```

## Output Files

Each validation produces 5 diff images in the render output directory:

```
renders/
├── japandi_v2.png                          # The render itself
├── diff_japandi_v2_ssim_heatmap.png        # Blue=same, Red=different (structural)
├── diff_japandi_v2_pixel.png               # Bright=more pixel change
├── diff_japandi_v2_side_by_side.png        # Original | Rendered side by side
├── diff_japandi_v2_overlay.png             # 50/50 blend to check alignment
└── diff_japandi_v2_edges.png               # Green=original edges, Red=rendered, Yellow=match
```

## Auto-Append to notes.md

After validation, append results to `projects/<name>/notes.md`:

```markdown
### Layout Validation — [render_name] (YYYY-MM-DD)

| Metric | Score | Rating |
|--------|-------|--------|
| Depth SSIM | 0.7295 | Good |
| Edge IoU | 0.1834 | Acceptable |
| Pixels Changed | 44.7% | Expected for style change |
| Overall | PASS | Layout preserved |

Diff outputs: `renders/diff_[render_name]_*.png`
Recommendation: Layout preserved. Minor variations acceptable for style change.
```

## SSIM Thresholds

| Score | Rating | Meaning |
|-------|--------|---------|
| >= 0.85 | Excellent | Room geometry nearly identical |
| 0.70–0.84 | Good | Layout preserved, minor furniture variations |
| 0.55–0.69 | Fair | Room shape similar but furniture rearranged |
| 0.40–0.54 | Poor | Room proportions may have changed |
| < 0.40 | Failed | Layout not preserved |

## When to Run

This skill runs automatically (no user prompt needed) when:
1. `/render` completes a **redesign** from a reference photo
2. Depth map exists in `references/preprocessed/${IMAGE_NAME}/`
3. The render was NOT a simple edit (edits don't need layout validation)

Skip validation when:
- Text-to-image render (no reference to compare against)
- Simple image edit (color/brightness adjustment via Gemini)
- User explicitly says "don't validate"

## Session Relevant Skills

- `/preprocess-room` — generates the original depth map (reuse if exists, never re-extract)
- `/render` — should auto-trigger this skill after redesign renders
- `/compare-models` — add SSIM score to provider comparison
- `/refine` — if layout is good but style needs work, refine the prompt

## Dependencies

```
pip install opencv-python-headless scikit-image pillow numpy
```

No torch, no local models. All image comparison is pure OpenCV + scikit-image.

## Gotchas

- **No local depth extraction** — if depth map is missing, run `/preprocess-room` (uses fal.ai API). Do NOT use torch/MiDaS locally.
- SSIM compares structure, not style — different colors with same layout scores high (correct behavior)
- Always resize to match dimensions before comparing — use render dimensions as target
- Edge IoU threshold is intentionally low (0.15) — style changes legitimately alter many edges
- For img2img renders (not structure-controlled), expect lower SSIM (0.55-0.70 is acceptable)
- Name diff files with render name prefix to support multiple renders per project
