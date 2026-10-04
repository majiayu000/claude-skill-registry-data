---
name: Image Editing
description: Edit images with AI inpainting, outpainting, background removal, upscaling, and restoration tools.
metadata: {"clawdbot":{"emoji":"✂️","os":["linux","darwin","win32"]}}
---

# AI Image Editing

Help users edit and enhance images with AI tools.

**Rules:**
- Ask what edit they need: remove objects, extend canvas, upscale, fix faces, change background
- Check technique files: `inpainting.md`, `outpainting.md`, `background-removal.md`, `upscaling.md`, `restoration.md`, `style-transfer.md`
- Check `tools.md` for provider-specific setup
- Always preserve original file before editing

---

## Edit Type Selection

| Task | Technique | Best Tools |
|------|-----------|------------|
| Remove objects/people | Inpainting | DALL-E, SD Inpaint, IOPaint |
| Extend image borders | Outpainting | DALL-E, SD Outpaint, Photoshop AI |
| Remove background | Segmentation | remove.bg, ClipDrop, Photoroom |
| Increase resolution | Upscaling | Real-ESRGAN, Topaz, Magnific |
| Fix blurry faces | Restoration | GFPGAN, CodeFormer |
| Change style | Style Transfer | SD img2img, ControlNet |
| Relight scene | Relighting | ClipDrop, IC-Light |

---

## Workflow Principles

- **Non-destructive editing** — keep originals, save edits as new files
- **Work in layers** — combine multiple edits sequentially
- **Match resolution** — edit at original resolution, upscale last
- **Mask precision matters** — better masks = better results
- **Iterate on masks** — refine edges for seamless blends

---

## Masking Basics

Masks define edit regions:
- **White** = edit this area
- **Black** = preserve this area
- **Gray** = partial blend (feathering)

**Mask creation methods:**
- Manual brush in editor
- SAM (Segment Anything) for auto-selection
- Color/luminance keying
- Edge detection

---

## Common Workflows

### Object Removal
1. Create mask over unwanted object
2. Run inpainting with context prompt (optional)
3. Blend edges if needed
4. Touch up artifacts

### Background Replacement
1. Remove background (get transparent PNG)
2. Place on new background
3. Match lighting/color
4. Add shadows for realism

### Enhancement Pipeline
1. Restore faces (if present)
2. Remove artifacts/noise
3. Color correct
4. Upscale to final resolution

---

## Quality Tips

- **Feather masks** — hard edges look artificial
- **Context prompts help** — describe what should fill the area
- **Multiple passes** — large edits may need iterative refinement
- **Check edges** — zoom in to verify blend quality
- **Match grain/noise** — add film grain to match original

---

### Current Setup
<!-- Tool: status -->

### Projects
<!-- What they're editing -->

### Preferences
<!-- Preferred tools, quality settings -->

---
*Check technique files for detailed workflows.*
