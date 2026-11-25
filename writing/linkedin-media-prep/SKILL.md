---
name: linkedin-media-prep
description: Convert, crop or fit-and-pad, resize, and compress images and videos for optimal LinkedIn upload quality and file size. Use when the user wants to prepare a photo, image, or video for LinkedIn (profile picture, cover photo, banner, post image, article featured image, post video, or video ad, or a carousel / document post made from slides), optimize file size for LinkedIn, crop, pad, letterbox, or resize to LinkedIn dimensions without cutting off signage, text, logos, or people at the edges, convert HEIC/RAW/PNG/MOV to LinkedIn-ready JPEG or MP4, or mentions LinkedIn media requirements, specs, or limits.
---

# LinkedIn Media Prep

Prepare any image or video for LinkedIn with correct dimensions, compression, and a deliberate choice between cropping and padding.

---

## Image Specs

| Use Case | Dimensions | Ratio | Notes |
|---|---|---|---|
| Post (portrait, max feed space) | 1080 × 1350 | 4:5 | **Default choice** for photos |
| Post (landscape) | 1200 × 627 | 1.91:1 | Good for banners, screenshots |
| Post (square) | 1080 × 1080 | 1:1 | Safe universal choice |
| Post (4:3) | 1440 × 1080 | 4:3 | Good for camera-native photos |
| Profile photo | 400 × 400 min | 1:1 | Recommend 800 × 800 |
| Cover photo | 1584 × 396 | 4:1 | Extreme ratio. Read Step 4 before cropping into it |
| Article featured | 1200 × 627 | 1.91:1 | |
| **Max file size** | **8 MB** | n/a | Target < 1 MB for fast upload |
| **Formats** | JPEG, PNG, GIF | n/a | **JPEG preferred** for photos |

## Video Specs

| Use Case | Dimensions | Ratio | Notes |
|---|---|---|---|
| Post (square) | 1080 × 1080 | 1:1 | Safe universal choice |
| Post (landscape) | 1920 × 1080 | 16:9 | Standard feed video |
| Post (vertical) | 1080 × 1920 | 9:16 | Mobile/Reels-style; pad if source is not 9:16 |
| **Max file size** | **5 GB** | n/a | Target < 200 MB for fast upload |
| **Max duration** | **30 minutes** | n/a | 3 seconds minimum |
| **Formats** | MP4 (H.264 + AAC) | n/a | **MP4 required** for best compatibility |
| **Frame rate** | 30 fps | n/a | Match source or standardise to 30 fps |
| **Pixel format** | yuv420p | n/a | Required for broad playback support |

---

## Carousel (Document Post)

A LinkedIn "carousel" is a document post: one PDF, one slide per page. Keep the user's own slides; never redesign or rewrite them unless asked.

- Output a single PDF, slides in the user's order (sort by the number in the filename, not alphabetically).
- One page size for every page: 1080x1350 (4:5) by default, or 1080x1080 (1:1) if most slides are square.
- Fit-and-pad each slide onto the page with the Image Workflow rules: never crop text or logos off the edges, never stretch, never upscale a small slide beyond its native size; pad with the slide's own background colour.
- LinkedIn limits: up to 100 MB and 300 pages. Compress images inside the PDF only as far as needed to stay well under the size limit.
- Report the page count, page size and file size, and list any slide that had to be padded heavily.

## Image Workflow

### 1. Inspect source

```bash
sips -g pixelWidth -g pixelHeight "<input>"
ls -lh "<input>"
```

### 2. Fix EXIF orientation (if needed)

iPhone and mobile photos often store portrait images with an EXIF orientation tag rather than rotated pixels. ImageMagick usually respects this automatically, but if the image appears sideways after conversion you can force it upright before cropping.

```bash
magick "<input>" -auto-orient "<input>-upright.png"
```

Use the upright version as your working copy for cropping.

### 3. Convert to editable format

If source is HEIC or other non-PNG:

```bash
sips -s format png "<input>" --out "<input>.png"
```

Use the PNG as the working copy for cropping.

### 4. Decide: crop or fit-and-pad

There are two ways to hit a target ratio, and the choice between them is the one decision in this workflow that can make the output worse than the source. Make it deliberately.

**Crop** throws away everything outside the crop box. It is the right call for a portrait or a scene with generous background around the subject. It is the wrong default for anything whose content runs to the edge: a sign above a doorway, a logo in a corner, a name badge, a whiteboard, a screenshot, a product that fills the frame, a group photo with people at both ends.

**Fit and pad** scales the whole image to fit inside the target box and fills the leftover space. Nothing is lost. The cost is that the image occupies less of the card.

Run this check before every crop. It is the step that stops you deleting the thing the user actually cared about.

**a. Name what is in the frame.** Look at the source and list what you would mention if you were describing the picture to someone: faces, text, signage, a logo, the horizon, hands, a product. Note roughly where each one sits. If the user gave a reason for the image ("the banner with our office sign in it"), that reason is the first item on the list and it is not negotiable.

**b. Draw the crop box on the source and look at it.** Work out the box you would use (Step 5), then render it:

```bash
# W H X Y are the crop box you are about to use
magick "source.png" -fill none -stroke red -strokewidth 16 \
  -draw "rectangle <X>,<Y> <X+W-1>,<Y+H-1>" \
  -resize 900x "crop-preview.png"
```

For the 3024 × 4032 example in Step 5, the box `3024x3780+0+126` draws as `rectangle 0,126 3023,3905`.

Open `crop-preview.png`. Everything outside the red rectangle is about to be deleted. Look at the picture rather than reasoning about the numbers, because the failure this prevents is exactly the one where the arithmetic was correct.

**c. Work out how much is going.** For a crop that trims height, the share removed is `(original_height − H) / original_height`, and the same on width. Keep that figure, the rule uses it.

**The rule:**

| What the preview shows | Do this |
|---|---|
| Everything you named sits inside the box with room to spare, and the crop removes less than about a quarter of the trimmed axis | **Crop** (Step 5) |
| Anything you named falls outside the box, or survives only by touching its edge | **Fit and pad** (Step 6) |
| The crop has to remove more than about half of one axis | **Fit and pad**, or change the target ratio (Step 7) |
| You cannot tell, or the call is purely aesthetic | Produce both and let the user choose |

Treat bare survival as failure. LinkedIn applies its own crops on top of yours: profile photos render in a circle, banners are trimmed differently on mobile. Anything flush against your crop edge is not safe.

**Banners especially.** The 4:1 cover photo is a thin horizontal slice. Cropping one out of an ordinary 4:3 or 3:4 photo deletes most of the picture, so nearly every banner made by cropping loses something. Default to fit-and-pad, or build the banner as a layout (Step 7), and crop only when the source is already close to 4:1.

### 5. Crop path (iterative with user)

Only once the Step 4 check has passed.

**First crop:** center, choose dimensions based on target ratio.

For a 4:5 portrait post from a portrait photo:
- Crop width = full width of image
- Crop height = width × 5 / 4
- Y-offset = (original_height − crop_height) / 2

Example for 3024 × 4032 source:
```bash
magick "source.png" -crop 3024x3780+0+126 "cropped.png"
```

**Iterative adjustments:**
- "More zoomed in" → reduce crop WxH (e.g. 2000×2500 instead of 3024×3780). Keep same ratio.
- "Too much space at top" → increase Y-offset (shift crop down).
- "Too much space at bottom" → decrease Y-offset (shift crop up).
- "Need wider/narrower" → adjust W and H maintaining ratio.

**Crop formula:**
```bash
magick "source.png" -crop <W>x<H>+<X>+<Y> "cropped.png"
# X = (original_width − W) / 2  (centered)
# Y = adjust based on subject position
```

If an iteration pushes something you named in Step 4a towards an edge, redraw the preview. The check is per crop box, not per session.

### 6. Fit-and-pad path

Scale the whole image to fit inside the target box, then fill the space left over. Nothing is lost. The work is in making the fill look deliberate, which is why white and black sit near the bottom of this list rather than the top.

**Choose the fill in this order:**

1. **A blurred enlargement of the image itself.** Works for almost any photograph. The colours match by construction, so it reads as a frame rather than a bar.
2. **A flat colour sampled from the image**, taken from the edges that will touch the pad. Use this when the background is already flat or close to it: a studio shot, a screenshot, a slide, a logo on a plain field. Blurring a flat background just produces a smear.
3. **A brand colour**, when the image is brand material and you know the hex. Check the subject still separates from it.
4. **White or black**, only when the image already has a white or black background that the pad continues seamlessly. Otherwise a white bar beside a photograph reads as a mistake, and it reads worse in dark mode, where it becomes the brightest thing on the screen.

**Sample the edge colour:**

```bash
# average colour of the top edge strip; use South, East or West for the other edges
magick "source.png" -gravity North -crop 100%x2%+0+0 +repage -resize 1x1\! -depth 8 txt:
```

It prints a line like `0,0: (43,88,118,255)  #2B5876FF`. Take the first six hex digits, `#2B5876`. Sample both edges that will touch the pad. If they come back noticeably different, the background is not flat, so use the blurred fill instead.

**Blurred fill (default for photos):**

```bash
magick "source.png" \
  \( -clone 0 -resize 1080x1350^ -gravity center -extent 1080x1350 -blur 0x24 -brightness-contrast -8x-10 \) \
  \( -clone 0 -resize 1080x1350 \) \
  -delete 0 -gravity center -composite -quality 85 "<name>-linkedin.jpg"
```

The first clone is the backdrop: filled to the target with `^`, blurred, and knocked back slightly so the sharp image sits in front of it. The second clone is the image itself, fitted inside the target with a plain `-resize`. Substitute your target size in both places.

**Flat fill:**

```bash
magick "source.png" -resize 1080x1350 -background "#2B5876" \
  -gravity center -extent 1080x1350 -quality 85 "<name>-linkedin.jpg"
```

`-resize 1080x1350` without `^` fits the whole image inside the box, and `-extent` adds the pad around it. Change `-gravity` when the image should sit off centre: on a banner, shift it so LinkedIn's profile photo does not land on top of the subject.

Both commands write the final file at target size, so skip Step 8 and go to Step 9.

**Banner placement.** LinkedIn draws your profile photo over the banner towards the lower left on desktop, and the banner is trimmed differently on mobile, so the reliably visible area is smaller than the full 1584 × 396. Published "safe area" figures disagree with each other, so do not build to a specific number. Keep anything that has to be read in the middle band, away from the left end and away from the outer edges, then check the result on a phone.

### 7. When neither a clean crop nor a clean pad exists

Some sources fight every target: an extreme ratio, a busy background that mirrors badly, a subject that fills the frame edge to edge. Work down this list.

1. **Change the target ratio.** A post does not have to be 4:5. Pick the listed ratio closest to the source and the problem usually disappears: a landscape photo into 1.91:1 or 1:1 costs a fraction of what 4:5 would. Free, and it settles most cases.
2. **Get a different source.** Another frame, the original before someone else cropped it, a re-shoot. Ask. People often have one and do not think to offer it.
3. **Build a layout instead of transforming a photo.** Place the subject on a canvas at the target size on purpose: subject to one side, breathing room on the other, background extended behind it. This is the right answer for 4:1 banners, which are a layout problem rather than a cropping problem.
4. **Extend the background.** If the area you need to add is plain, mirror the edge outwards and pad into the mirrored region:

   ```bash
   # widen a 3024-wide source to 4032 by mirroring 504 px onto each side
   magick "source.png" -virtual-pixel mirror \
     -set option:distort:viewport 4032x4032-504-0 -distort SRT 0 +repage "extended.png"
   ```

   Viewport is `<new W>x<new H>-<X>-<Y>`, where X and Y are how far outside the original the new canvas begins. Inspect the result: mirroring is invisible on sky, walls, carpet and bokeh, and obvious on anything with structure.

5. **Ship the compromise, and say what it cost.** If a crop has to lose something, name what it lost, in words, before the user posts it. The one thing not to do is hand back a cropped file as though nothing happened.

### 8. Resize & compress for LinkedIn

Skip this step if you padded, because Step 6 already wrote the final file.

```bash
magick "cropped.png" -resize 1080x1350 -quality 85 "<name>-linkedin.jpg"
```

For profile photos:
```bash
magick "cropped.png" -resize 800x800 -quality 85 "<name>-linkedin-profile.jpg"
```

For cover photos:
```bash
magick "cropped.png" -resize 1584x396 -quality 85 "<name>-linkedin-cover.jpg"
```

For 4:3 posts:
```bash
magick "source.png" -resize 1440x1080 -quality 85 "<name>-linkedin-4by3.jpg"
```

These assume the working file already sits at the target ratio. `-resize` preserves aspect ratio, so if the input is not at that ratio the output comes out short on one axis rather than at the size you asked for. If that happens, the input was never cropped or padded to the target, so go back to Step 4. Do not reach for `-resize 1584x396!`, which stretches faces and text.

### 9. Verify output

```bash
ls -lh "<output>.jpg"
sips -g pixelWidth -g pixelHeight "<output>.jpg"
```

Ensure:
- Dimensions match target
- File size < 8 MB (preferably < 1 MB)
- Quality is acceptable

Then open the file and check it against your Step 4a list:
- Every item you named is still in the picture, and still legible at feed size
- If you padded, the fill reads as deliberate rather than as a bar, in both light and dark mode
- If you cropped and something did not survive, tell the user before they post

---

### Which video format should I choose?

| Source orientation | Your goal | Recommended target |
|---|---|---|
| Portrait (phone video) | Maximum mobile feed space | **Vertical 1080×1920** (pad with black if source is 3:4 or 4:5) |
| Portrait (phone video) | Safe universal compatibility | **Square 1080×1080** (centre-crop) |
| Landscape (screen-recording, camera) | Standard feed video | **Landscape 1920×1080** |
| Landscape | Safe universal compatibility | **Square 1080×1080** (centre-crop) |
| Not sure | n/a | **Square 1080×1080** |

> **Rule of thumb:** Square works everywhere. Vertical gets the most mobile screen real estate but can letterbox on desktop. Landscape is best for demos, interviews, and cinematic content.

A centre-crop deletes the edges of every frame, exactly as it does for a still. Before choosing a crop chain over a pad chain, scrub the source and check what lives near the edges: captions burned into the footage, a speaker who drifts out of centre, a logo bug in a corner, a screen share whose toolbar sits at the top. If any of it matters, scale and pad instead. Step 4 of the Image Workflow is the same judgement in more detail.

---

## Video Workflow

### 1. Inspect source

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,avg_frame_rate,duration,bit_rate \
  -show_entries format=duration,size,bit_rate \
  -of csv=p=0 "<input>"
```

Also check for rotation metadata:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream_side_data=display_matrix \
  -of default=nk=1:nw=1 "<input>"
```

### 2. Handle rotation (iPhone / mobile sources)

Mobile videos often store frames in landscape with a rotation tag. Apply `transpose` in the filter chain before cropping/scaling.

| Display Matrix | Transpose value | Meaning |
|---|---|---|
| `-90°` (270°) | `1` | 90° clockwise |
| `+90°` | `2` | 90° counter-clockwise |
| `180°` | `3` | 180° |
| No rotation | omit | n/a |

### 3. Choose target and build filter chain

**Square (1080×1080)**, centre-crop after rotation:
```
transpose=1,crop=1080:1080:(in_w-1080)/2:(in_h-1080)/2,format=yuv420p
```

**Landscape (1920×1080)**, scale to fit then pad, or centre-crop:
```
transpose=1,scale=1920:-2,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p
```

**Vertical (1080×1920)**, scale to width then pad top/bottom:
```
transpose=1,scale=1080:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p
```

If the source aspect ratio already matches the target, you can omit `pad` and just `scale=1080:1080` or `scale=1920:1080`.

### 4. Common one-liner (portrait iPhone to square)

The most frequent request: a portrait iPhone video converted to a LinkedIn-ready square MP4.

```bash
ffmpeg -y -i "IMG_xxxx.MOV" \
  -vf "transpose=1,crop=1080:1080:(in_w-1080)/2:(in_h-1080)/2,format=yuv420p" \
  -c:v libx264 -profile:v main -level 4.2 -preset medium -crf 23 -r 30 \
  -c:a aac -b:a 128k -movflags +faststart \
  "output_linkedin_square.mp4"
```

Swap `transpose=1` for the correct rotation value from Step 2, or omit `transpose=1,` if the source has no rotation metadata.

### 5. Transcode

```bash
ffmpeg -y -i "<input>" \
  -vf "<filter_chain>" \
  -c:v libx264 -profile:v main -level 4.2 -preset medium -crf 23 -r 30 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "<output>.mp4"
```

Parameter notes:
- `-profile:v main -level 4.2` gives broad device compatibility
- `-crf 23` gives good quality / size balance (lower = higher quality)
- `-r 30` standardises the frame rate
- `-movflags +faststart` puts the moov atom at the beginning for web streaming

### 6. Verify output

```bash
ls -lh "<output>.mp4"
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,avg_frame_rate,duration,bit_rate \
  -show_entries format=duration,size,bit_rate \
  -of csv=p=0 "<output>.mp4"
```

Ensure:
- Dimensions match target
- File size reasonable for upload (< 200 MB ideally)
- No rotation metadata remains (players should not rotate it again)

---

## Tools

- **Images:** Prefer `magick` (ImageMagick 7) or `convert` (ImageMagick 6). Fallback to `sips` on macOS for basic format conversion. Install via `brew install imagemagick`.
- **Videos:** `ffmpeg` + `ffprobe`. Install via `brew install ffmpeg`.
