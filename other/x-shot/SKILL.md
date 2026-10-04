---
name: x-shot
description: Frame a screenshot into a polished X post image — flat backdrop colour sampled from the screenshot itself, seamless card, pixel-perfect embed, rendered to PNG via headless Chrome. Takes an optional image path or description; defaults to the most recent Desktop screenshot.
argument-hint: "[image path or description — blank = latest Desktop screenshot]"
disable-model-invocation: true
---

Turn a screenshot into an image ready to post on X. The design is derived from the screenshot's own content — never a stock template.

## 1. Pick the source image

- If args contain a path, use it. If args describe an image ("the terminal one"), match against recent files.
- Otherwise: most recent `Screenshot *.png` in `~/Desktop` (`ls -t`).
- Read the image and note `sips -g pixelWidth -g pixelHeight`.

## 2. Derive the design from the content

Read the screenshot and decide:

- **Backdrop colour**: pick the screenshot's most distinctive accent colour (a progress bar, button, syntax highlight) and use it as a flat, full-bleed backdrop — slightly deepened/desaturated so the screenshot stays the star. If the screenshot has no accent, use a warm neutral (cream for dark screenshots, deep charcoal for light ones).
- **Card colour**: exactly match the screenshot's own background colour so the card padding blends seamlessly — no visible seam. If you can't match it confidently, skip padding: round the image itself and shadow it directly.
- Hard rules: flat colours only — no gradients, no purple/teal "AI" palettes, no decorations, no added text unless asked. One soft shadow for depth.

## 3. Compose

Canvas 1200×675 CSS px (16:9) for landscape sources; 1080×1350 (4:5) if the source is taller than wide. Centre a rounded card (radius 20px, padding ~44–52px) containing the screenshot as a base64 `<img>`.

**Pixel-perfect rule**: render at `--force-device-scale-factor=2` and set the img CSS width to `pixelWidth / 2` so source pixels map 1:1 — never upscale. If that exceeds the canvas, scale down only.

## 4. Render

```sh
cd <scratchpad>
base64 -i "$SRC" -o shot.b64   # inject into the HTML via a placeholder swap
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --screenshot=out.png \
  --window-size=1200,675 --force-device-scale-factor=2 \
  --hide-scrollbars "file://$PWD/post.html"
```

## 5. Verify and deliver

- Read the rendered PNG. Check: no seam between card and screenshot, nothing cropped, backdrop not garish. Iterate until clean.
- Copy to `~/Desktop/<subject>-x.png` and tell the user the path and dimensions.
- Offer variants (light backdrop, tighter crop, caption) only after delivering.
