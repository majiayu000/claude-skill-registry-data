---
name: update-launcher-icon
description: Use when /logo.svg changes or when asked to update, replace, or apply the Android launcher app icon in femto-car-launcher. Triggers on "update the app icon", "apply the new logo", "make logo.svg the launcher icon". Covers deriving the adaptive-icon background / foreground / monochrome VectorDrawables from logo.svg, including the 66/108 safe-zone scaling math that raw SVG coordinates always violate.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Skill
paths:
  - logo.svg
  - app/src/main/res/drawable/ic_launcher_background.xml
  - app/src/main/res/drawable/ic_launcher_foreground.xml
  - app/src/nightly/res/drawable/ic_launcher_foreground.xml
  - app/src/main/res/mipmap-anydpi/**
---

# Updating the launcher icon from logo.svg

`/logo.svg` (512×512, project root) is the brand-mark SSOT. The
launcher icon is an [adaptive icon] **derived** from it; never edit
the derived drawables as the design source — change `logo.svg`
first, then re-run this procedure.

[adaptive icon]: https://developer.android.com/develop/ui/views/launch/icon_design_adaptive

## Layer mapping

| logo.svg element | Android resource | Rule |
| --- | --- | --- |
| Full-bleed background `<rect>` | `drawable/ic_launcher_background.xml` | Full-canvas fill of the rect's colour only. **Drop the corner radius** — the launcher applies its own mask shape. |
| Everything else (the mark) | `drawable/ic_launcher_foreground.xml` | Scaled into the safe zone (math below), centred on the canvas. |
| (same paths) | `<monochrome>` in `mipmap-anydpi/*.xml` | Shares the foreground drawable. Opacity differences survive as alpha in themed icons. |

`mipmap-anydpi/ic_launcher.xml` and `ic_launcher_round.xml` only
reference the two drawables — they normally need no edit.

## Safe-zone scaling (the step everyone skips)

The adaptive-icon safe zone is the centre circle of diameter 66 on
the 108 canvas. **Copying logo.svg coordinates 1:1 into the
foreground is always wrong** — the full-bleed logo art reaches the
canvas edge and the launcher mask clips it.

Keep the foreground viewport at 512 (matching logo.svg) and shrink
the mark into the safe circle:

1. Safe radius in 512 units: `512 × 33 / 108 ≈ 156`.
2. Find the mark's farthest extent from its own centre `c`,
   **including stroke**: `r_max = max(|p − c|) + strokeWidth / 2`
   over all path end/corner points `p`.
3. `scale = 150 / r_max` (use ~150, not 156, for breathing room).
4. Transform every coordinate `p' = 256 + (p − c) × scale` and
   multiply every `strokeWidth` by the same `scale`. This also
   re-centres the mark's optical centre on (256, 256).
5. **Re-verify after transforming** (arithmetic slips here are
   common): recompute
   `r'_max = max(|p' − (256, 256)|) + strokeWidth' / 2` over the
   transformed points with a calculator/script — do not do the
   square roots in your head. The procedure is only complete when
   `r'_max ≤ 156`.

## Procedure

1. **Read `/logo.svg`** and classify elements per the layer-mapping
   table.
2. **Write the background**: 108 viewport, single
   `M0,0h108v108h-108z` path filled with the logo's background
   colour. Nothing else.
3. **Write the foreground**: 512 viewport, one `<path>` per SVG
   element, coordinates transformed by the safe-zone math.
   Attribute translation: `stroke` → `android:strokeColor`,
   `stroke-width` → `android:strokeWidth`, `opacity` on a stroked
   path → `android:strokeAlpha` (on a filled path →
   `android:fillAlpha`), `stroke-linecap`/`-linejoin` →
   `android:strokeLineCap`/`LineJoin`, no fill →
   `android:fillColor="#00000000"`.
4. **Monochrome**: keep sharing the foreground drawable. Create a
   dedicated white-stroke drawable only if the mark encodes its
   hierarchy in *colour* rather than opacity (alpha is all the
   themed-icon pipeline keeps).
5. **No rasters**: `minSdk = 33`, so `mipmap-anydpi` always wins.
   Do not generate `mipmap-*dpi` webp/png fallbacks; delete any
   that exist.
6. **Verify** with the
   [`verify-android-build`](../verify-android-build/SKILL.md)
   skill.

## Nightly channel

`app/src/nightly/res/drawable/ic_launcher_foreground.xml` is the
stable foreground plus a two-path "N" badge (filled disc + glyph)
appended inside `<vector>`, so the two channels stay visually
distinguishable when both are installed side by side. Source-set
precedence lets it override the stable drawable — including the
shared monochrome icon — with no other wiring.

Regenerate it whenever `logo.svg` changes: re-run the procedure
above for the stable foreground, then re-append the two badge paths
unchanged. The badge geometry (disc centre 357.5,336.5, r 20.5) is
bound by the chevron ink, the tighter of its two clearance limits —
see the derivation in the comment above those paths in the drawable
— so treat it as fixed rather than rescaling or repositioning it by
eye.

## Skill-specific anti-patterns

- Copying logo.svg coordinates or stroke widths 1:1 into the
  foreground — the mask clips the mark (see safe-zone math).
- Reproducing the logo's rounded corners in the background layer.
- Generating density-bucket PNG/webp fallbacks "for older devices".
- Editing `ic_launcher_foreground.xml` directly to change the
  design — `logo.svg` is the SSOT.
