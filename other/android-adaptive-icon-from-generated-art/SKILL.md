---
name: android-adaptive-icon-from-generated-art
description: "Use when replacing an Android app's launcher icon with model-generated art, or when an adaptive icon looks cropped, blank, boxed or crossed by a stray arc on a real launcher, or themed or old launchers show a default icon instead."
---

# Adaptive launcher icon from generated art

One keyed PNG becomes ~20 files. The traps are all silent: the icon still
builds, installs and launches while being wrong. Generate the emblem itself with
`monarch-art-generation`, which owns the resumable batch runner under the image
quota and the rule against wiring a half-drawn set.

In Ironvellum, `python tools/icon_install.py <png>` (`--dry-run` to preview)
writes all 20 files under the rules below and refuses unkeyed or empty sources.

## What the manifest actually references

Check before generating anything:

```
res/mipmap-anydpi-v26/ic_launcher.xml   -> background / foreground / monochrome
res/mipmap-<bucket>/ic_launcher_foreground.png
res/mipmap-<bucket>/ic_launcher_monochrome.png
res/mipmap-<bucket>/ic_launcher{,_round}.png   # legacy, pre-26 launchers
```

Five density buckets (mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi). Miss the legacy pair and
old launchers show the default robot; miss monochrome and themed icons fall
back.

## The three rules that are easy to get wrong

1. **Safe zone.** An adaptive foreground is 108dp but a launcher may mask it to
   any shape; only the centre **72dp (66%)** is guaranteed visible. Art drawn
   edge to edge loses its outer third to a circle mask. Scale the emblem into
   66% of the canvas and leave the rest transparent.
2. **Monochrome is a silhouette, not a picture.** Android tints that layer, so
   colour in it is meaningless. Write flat white on the source's alpha.
3. **Legacy bitmaps have no mask**, so they may use more of the square (~84%).

Sizes: adaptive edge = 108dp x bucket scale (mdpi 108 ... xxxhdpi 432);
legacy = 48dp x bucket scale (mdpi 48 ... xxxhdpi 192).

## Refuse bad input rather than shipping a slab

Two checks, both cheap, both catch a real failure:

- **Unkeyed source**: if >90% of pixels are alpha > 24 the ground was never
  removed — the icon will be a rectangle. Refuse.
- **Empty source**: max alpha 0. Refuse.

A density-keyed source can also carry a faint paper film that passes both checks
and shows as a box on the launcher — measure and cut it per
`monarch-art-generation` (Trap 1).

## Generated art carries its own frame

The model's sketched margin border becomes a stray arc across the icon inside an
adaptive mask. Crop it before installing, per `monarch-art-generation` (Trap 2).

## Prompt for a thumbnail, not a poster

The icon is judged at 48dp. Ask for: single centred emblem, massive bold
silhouette, thick pale strokes on transparency, no frame, no text, no
background, readable at 48dp. Fine detail and lettering are wasted.

Match the emblem's value to the background drawable — a dark `ic_launcher_
background` needs pale ink, not a dark shape.

## Verify on a launcher, never on the PNG

The PNG always looks fine; the mask is what crops it.

```
adb install -r -t app-debug.apk
adb shell input keyevent KEYCODE_HOME
adb shell input swipe 540 1800 540 600 300      # open the app drawer
adb shell uiautomator dump /sdcard/ui.xml
# find text="<AppName>" bounds, screencap, crop just above that label
```

Look for: emblem inside the mask, nothing clipped at the corners, adequate
contrast against the background layer.
