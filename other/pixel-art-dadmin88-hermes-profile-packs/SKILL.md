---
name: pixel-art
description: "Pixel art w/ era palettes (NES, Game Boy, PICO-8)."
version: 2.0.0
author: dodo-reach
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, pixel-art, arcade, snes, nes, gameboy, retro, image, video]
    category: creative
    credits:
      - "Hardware palettes and animation loops ported from Synero/pixel-art-studio (MIT) — https://github.com/Synero/pixel-art-studio"
---

# Pixel Art

Convert any image into retro pixel art, then optionally animate it into a short
MP4 or GIF with era-appropriate effects (rain, fireflies, snow, embers).

Two scripts ship with this skill:

- `scripts/pixel_art.py` — photo → pixel-art PNG (Floyd-Steinberg dithering)
- `scripts/pixel_art_video.py` — pixel-art PNG → animated MP4 (+ optional GIF)

Each is importable or runnable directly. Presets snap to hardware palettes
when you want era-accurate colors (NES, Game Boy, PICO-8, etc.), or use
adaptive N-color quantization for arcade/SNES-style looks.

## When to Use

- User wants retro pixel art from a source image
- User asks for NES / Game Boy / PICO-8 / C64 / arcade / SNES styling
- User wants a short looping animation (rain scene, night sky, snow, etc.)
- Posters, album covers, social posts, sprites, characters, avatars

## Workflow

Use the supplied era or palette. Ask about style or scene only when the brief leaves a material choice open. Work from an authorized local input and write to an explicit new output.

Use conversion for visual studies, retro treatments, and approved reference work. The converter uses RGB and discards transparency. The video script adds environmental overlays to a still; use the role's native-grid sprite and frame workflows for editable game assets, stable pivots, alpha, and cel animation.

Use `pixel_art()` first. If a scene effect was requested, pass the converted PNG to `pixel_art_video()`.

## Preset Catalog

| Preset | Era | Palette | Block | Best for |
|--------|-----|---------|-------|----------|
| `arcade` | 80s arcade | adaptive 16 | 8px | Bold posters, hero art |
| `snes` | 16-bit | adaptive 32 | 4px | Characters, detailed scenes |
| `nes` | 8-bit | NES (54) | 8px | True NES look |
| `gameboy` | DMG handheld | 4 green shades | 8px | Monochrome Game Boy |
| `gameboy_pocket` | Pocket handheld | 4 grey shades | 8px | Mono GB Pocket |
| `pico8` | PICO-8 | 16 fixed | 6px | Fantasy-console look |
| `c64` | Commodore 64 | 16 fixed | 8px | 8-bit home computer |
| `apple2` | Apple II hi-res | 6 fixed | 10px | Extreme retro, 6 colors |
| `teletext` | BBC Teletext | 8 pure | 10px | Chunky primary colors |
| `mspaint` | Windows MS Paint | 24 fixed | 8px | Nostalgic desktop |
| `mono_green` | CRT phosphor | 2 green | 6px | Terminal/CRT aesthetic |
| `mono_amber` | CRT amber | 2 amber | 6px | Amber monitor look |
| `neon` | Cyberpunk | 10 neons | 6px | Vaporwave/cyber |
| `pastel` | Soft pastel | 10 pastels | 6px | Kawaii / gentle |

Named palettes live in `scripts/palettes.py` (see `references/palettes.md` for
the complete list — 28 named palettes total). Any preset can be overridden:

```python
pixel_art("in.png", "out.png", preset="snes", palette="PICO_8", block=6)
```

## Scene Catalog (for video)

| Scene | Effects |
|-------|---------|
| `night` | Twinkling stars + fireflies + drifting leaves |
| `dusk` | Fireflies + sparkles |
| `tavern` | Dust motes + warm sparkles |
| `indoor` | Dust motes |
| `urban` | Rain + neon pulse |
| `nature` | Leaves + fireflies |
| `magic` | Sparkles + fireflies |
| `storm` | Rain + lightning |
| `underwater` | Bubbles + light sparkles |
| `fire` | Embers + sparkles |
| `snow` | Snowflakes + sparkles |
| `desert` | Heat shimmer + dust |

## Invocation Patterns

Run from the installed skill's `scripts` directory, using the path reported by Hermes for the active profile:

```bash
python pixel_art.py in.jpg out.png --preset gameboy
python pixel_art.py in.jpg out.png --preset snes --palette PICO_8 --block 6
python pixel_art_video.py out.png out.mp4 --scene night --duration 6 --gif
```

## Pipeline Rationale

**Pixel conversion:**
1. Boost contrast/color/sharpness (stronger for smaller palettes)
2. Posterize to simplify tonal regions before quantization
3. Downscale by `block` with `Image.NEAREST` (hard pixels, no interpolation)
4. Quantize with Floyd-Steinberg dithering — against either an adaptive
   N-color palette OR a named hardware palette
5. Upscale back with `Image.NEAREST`

Quantizing AFTER downscale keeps dithering aligned with the final pixel grid.
Quantizing before would waste error-diffusion on detail that disappears.

**Video overlay:**
- Copies the base frame each tick (static background)
- Overlays stateless-per-frame particle draws (one function per effect)
- Encodes via ffmpeg `libx264 -pix_fmt yuv420p -crf 18`
- Optional GIF via `palettegen` + `paletteuse`

## Dependencies

- Python 3.9+
- Pillow for conversion and video; ffmpeg on PATH for video only. If a dependency is absent, report it or use an available editor. Dependency installation is a separate operation.

## Pitfalls

- Pallet keys are case-sensitive (`"NES"`, `"PICO_8"`, `"GAMEBOY_ORIGINAL"`).
- Very small sources (<100px wide) collapse under 8-10px blocks. Upscale the
  source first if it's tiny.
- Fractional `block` or `palette` will break quantization — keep them positive ints.
- MP4 export pads an odd width or height by one pixel for encoding.
- Animation particle counts are tuned for ~640x480 canvases. On very large
  images you may want a second pass with a different seed for density.
- `mono_green` / `mono_amber` force `color=0.0` (desaturate). If you override
  and keep chroma, the 2-color palette can produce stripes on smooth regions.
  pepper the user with more picks.

## Verification

- PNG is created at the output path
- Clear square pixel blocks visible at the preset's block size
- Color count matches preset (eyeball the image or run `Image.open(p).getcolors()`)
- Video is a valid MP4 (`ffprobe` can open it) with non-zero size

## Attribution

Named hardware palettes and the procedural animation loops in `pixel_art_video.py`
are ported from [pixel-art-studio](https://github.com/Synero/pixel-art-studio)
(MIT). See `ATTRIBUTION.md` in this skill directory for details.
