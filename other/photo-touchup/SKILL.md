---
name: photo-touchup
description: Touch up a photo (or edit out something in it) — upscale resolution, fix flat/dim lighting, sharpen, or remove/change something in the frame (e.g. a face mask, a blemish, an object) using AI. Use when you want a photo "touched up," "cleaned up," made higher-res, or edited with AI. Pairs well with the `apple-photos` skill for pulling the source photo and re-inserting the result back into an album.
---

# Photo touch-up

Two different tools for two different jobs. Don't reach for the AI editor when a conventional
pass will do — it's slower, costs money, and can subtly change someone's face.

## 1. Conventional retouch (resolution, lighting, sharpness) — `scripts/retouch.py`

For: old/blurry photos, flat indoor lighting (gym fluorescents, etc.), general "make this
crisper." Free, local, fast (~1s), deterministic.

```bash
pip3 install --break-system-packages opencv-python-headless numpy   # once
python3 scripts/retouch.py in.jpg out.jpg                            # defaults are tuned & safe
python3 scripts/retouch.py in.jpg out.jpg --scale 2.0 --sharpen 0.2 --saturation 1.1
```

Pipeline: bilateral denoise → cubic upscale → light unsharp mask → subtle saturation lift →
global (not local) auto-levels. Defaults (`scale=1.6, sharpen=0.15, saturation=1.06`) are
calibrated to be visible but not "filtered."

**Hard-learned mistake — don't use `cv2.createCLAHE` (local/tiled contrast).** First pass on a
real photo used CLAHE + strong unsharp + Lanczos upscale and it looked fine at a small preview
thumbnail but was badly posterized/painted-looking at full resolution (blotchy skin, halo edges)
— because CLAHE's local contrast amplifies JPEG block artifacts, and it compounds with
sharpening. Global auto-levels (`cv2.normalize` on the L channel) gives contrast without this.
Cubic resize beats Lanczos here too — Lanczos over-crisps into halos at 1.5-2x.

**Always QA at full resolution, not the small preview.** Crop a face-sized region from both the
original and the output at 1:1 pixel scale and look at both — artifacts that are invisible in a
600px thumbnail (this is what shipped the posterization mistake) are obvious once zoomed in:

```python
import cv2
before = cv2.imread("original.jpg"); after = cv2.imread("retouched.jpg")
bh, bw = before.shape[:2]
scale = after.shape[1] / bw
x1, y1, x2, y2 = int(bw*0.30), int(bh*0.12), int(bw*0.70), int(bh*0.38)  # adjust to face location
cv2.imwrite("crop_before.jpg", before[y1:y2, x1:x2])
cv2.imwrite("crop_after.jpg", after[int(y1*scale):int(y2*scale), int(x1*scale):int(x2*scale)])
```
Read both crops back and actually look before calling it done.

## 2. AI generative edit (remove/change something in the frame) — Nano Banana Pro via `make-art`

For: removing a face mask, an object, a blemish that needs *reconstruction* (not just cleanup) —
anything where the model has to invent plausible pixels for something not visible in the source.
Uses the same engine as the `make-art` skill (`gemini-3-pro-image-preview`); read that skill for
the two gotchas (**network must be allowed**, and the `GEMINI_API_KEY`).

```bash
python3 <make-art skill dir>/scripts/gen_art.py \
  --image path/to/original.jpg \
  --image path/to/reference_face_1.jpg \
  --image path/to/reference_face_2.jpg \
  --prompt-file prompt.txt \
  --out edited.png --aspect 3:4 --size 2K
```

**Give it reference photos when reconstructing a person's face.** If the edit needs to invent
part of someone's actual face (e.g. what's under a mask), pass 1-2 additional `--image` args of
other clear, unobstructed photos of that same person alongside the photo being edited. Without
references the model guesses a generic face; with them it matches real nose/mouth/beard/skin
tone. Pick references that are well-lit, front-facing, and not obstructed by sunglasses/hats/masks.

Prompt pattern that worked well (mask removal, worked on the first attempt):
> "This is a real photograph of [person] wearing [thing to remove]. Edit this photo to remove
> [thing] and reveal what's underneath, photorealistically reconstructed to match their true
> face. [N] additional reference photos of this same person's actual unmasked face are
> provided — use them to accurately match real nose/mouth/beard/skin tone. Keep everything else
> in the original photo completely unchanged: same pose, same background, same lighting and
> angle, same framing. This should look like a photorealistic edit of the original, not a new
> illustration or a different person."

## Do NOT alter someone's actual physique/body for a profile photo (or similar use)

Editing body shape (as opposed to lighting/sharpness/blemish cleanup) means the photo stops
matching what the person looks like in person — and a dating or professional profile is exactly
where that gap gets discovered immediately, in a way that reads as dishonest rather than "good
photo." Conventional retouch and AI removal of an *object* (mask, blemish, background item) are
fine. Changing body composition in a photo used to represent oneself to others is not; push back
if asked.
