---
name: photo-exif-frame
description: 当使用者说"给照片加参数边框"、"加个相机参数水印"、"给这张照片加个信息带"、"照片下面印上光圈快门"时使用。Add a configurable information band to an existing photograph using embedded EXIF facts such as aperture, shutter speed, exposure compensation, ISO, capture time, and camera. Use when a user asks to frame, label, or export a photo with shooting metadata. Do not use for interpreting photographic intent, inventing missing metadata, or editing the photograph itself.
category: photography
version: 0.1.1
status: draft
priority: P2
compatible_agents:
  - claude-code
  - openclaw
  - cursor
  - codebuddy
  - generic-llm-agent
---

# Photo EXIF Frame

Create a reproducible framed-photo asset while keeping facts and aesthetic choices separate. The script reads metadata and renders pixels; the agent confirms layout choices and never guesses absent EXIF values.

## Inputs

Collect or confirm:

- source image path and output path;
- band color and text color;
- fields to show, in order;
- optional font path;
- optional band-height and horizontal-padding ratios.

Defaults are documented in `references/layout-defaults.md`. If the user has not expressed a preference, state the defaults before rendering. Treat paths and style values as user-controlled inputs, not facts about the photograph.

## Workflow

1. **Protect the source.** Write to a different output path. Never overwrite the source unless the user explicitly requests it and the environment's safety policy permits that action.
2. **Inspect metadata.** Run the renderer with `--inspect` first when practical. Treat only the reported embedded values as camera-recorded facts.
3. **Resolve missing facts.** Leave missing fields blank. This version does not accept manual metadata overrides; do not edit the report to make a field appear camera-recorded. The capture time comes from DateTimeOriginal only: a file that carries only IFD0 DateTime (its last edit or export time) gets a blank CAPTURED field and a warning saying why.
4. **Choose the presentation.** Confirm field order, colors, font, and ratios. Do not claim that these choices reveal the image's intent.
5. **Render deterministically.** Use `scripts/render_exif_frame.py`. The script applies EXIF orientation, adds a band below the uncropped photograph, sizes the type so every label and value fits its cell, and writes a new image. It keeps the source's RGB ICC profile (a Display P3 photo stays Display P3; the band and text colours are converted into that profile), converts CMYK or grey profiles to sRGB, composites transparent areas onto the band colour, and writes JPEG at quality 95 with 4:4:4 chroma.
6. **Verify.** Inspect the output dimensions and the script's metadata report. Confirm that every displayed non-empty value appears in embedded EXIF.
7. **Report provenance.** Return source/output paths, rendered fields, blank fields, and style values.

## Commands

Inspect without rendering:

```bash
python3 scripts/render_exif_frame.py input.jpg --inspect
```

Render with defaults:

```bash
python3 scripts/render_exif_frame.py input.jpg --output framed.png
```

Customize fields and layout:

```bash
python3 scripts/render_exif_frame.py input.jpg \
  --output framed.png \
  --fields aperture,shutter,iso,captured,camera \
  --band-color '#F3F0E8' \
  --text-color '#171717' \
  --band-ratio 0.16 \
  --padding-ratio 0.04 \
  --font /System/Library/Fonts/Supplemental/Arial.ttf
```

The font path is the macOS one; any TrueType/OpenType file works, for example `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` on Linux. Without `--font` the renderer picks an installed system font that has the glyphs the text needs.

The renderer requires Python 3 and Pillow; fontTools is optional and lets it check that a font has every glyph. `scripts/image_io.py` is a shared copy of the photo skills' image module; identical copies live in `photo-caption-writer`, `shoot-outing-review-card`, `photo-series-layout`, and `photo-spread-composer`, and `scripts/validate.sh` requires them to stay byte-identical, so never edit one copy alone. Use `--help` for the complete interface and `--selftest` for the regression checks.

HEIC/HEIF files (the iPhone default) need the `pillow-heif` package, or a JPEG copy first: `sips -s format jpeg IMG.HEIC --out IMG.jpg` (macOS; keeps the EXIF).

## Output contract

Return or record:

- source and output paths;
- source metadata report from the script;
- displayed field order;
- fields left blank;
- style configuration;
- output pixel dimensions;
- font, the label and value sizes used (`font_size_px`), and the readable minimum (`min_readable_value_px`);
- source and output colour space (`color_space`, `output_color_space`, `color_policy`);
- a warning that source EXIF is read for display but not copied into the composite output;
- other warnings, including absent EXIF, a capture time left blank because only IFD0 DateTime exists, transparency, or a fallback font.

## Boundaries

- Do not infer aperture, shutter speed, ISO, date, device, location, or authorship from visible content.
- Do not invent a value merely to balance the layout.
- Do not alter crop, exposure, color, retouching, or composition. This library has no retouching or colour-grading skill yet; those edits happen before framing.
- Do not describe mood, meaning, or creative intent unless the photographer supplied that context.
- GPS and other sensitive EXIF fields are neither displayed nor copied by default.
- This skill creates one framed photograph. To arrange 3–9 of your own photos into one image or PDF, use `photo-series-layout`; for a magazine- or board-style spread with a credit on every photo, use `photo-spread-composer`.

## Failure handling

- **No EXIF:** render requested labels with blank values and report that no embedded values were found.
- **Partial EXIF:** render known values and leave the rest blank.
- **Unsupported/corrupt image:** stop without replacing any existing output and report the decoder error.
- **HEIC/HEIF:** without `pillow-heif` the renderer exits 2 and prints the `sips -s format jpeg` command; convert to a JPEG next to the original (never over it) and render that.
- **Font unavailable:** require a valid font path when typography matters. Without `--font` the renderer uses an installed system font (Helvetica or Arial on macOS, DejaVu Sans on Linux, a Chinese font when a value needs one) at the fitted size; if none is installed it uses Pillow's built-in font and warns, and on Pillow older than 10.1 it stops and asks for `--font`. A `--font` that lacks glyphs for the text is refused instead of drawing boxes.
- **Text does not fit:** the type already shrinks to fit each cell, down to the readable minimum (12 px or 0.6% of the output's long edge, whichever is larger). Below that the renderer stops: select fewer fields or pass a narrower font, for example Arial Narrow. `--band-ratio` sets the band height, not the cell width, so raising it does not help. Do not silently omit facts.

## Validation cases

See `tests/cases/photo-exif-frame.md` (fixtures in `tests/fixtures/photo-exif-frame/`) and run `python3 scripts/render_exif_frame.py --selftest`. At minimum, test full EXIF, partial/no EXIF, rotated EXIF orientation, unsafe same-path output, and narrow-image overflow before promoting the skill beyond draft.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 不给 --font 时不再落到 10px 默认字体：改用系统字体，字号按格宽倒推、缩到放得下，低于可读下限才报错；更正"加大 --band-ratio"的错误建议并让自定义示例能跑通；拍摄时间只取 DateTimeOriginal；曝光补偿印成 -2/3 EV；保留源 ICC（P3 不再发灰），透明区填信息带色，JPEG 用 q95 4:4:4；加 --selftest；删掉与库级 UNLICENSED 矛盾的 license 行；目录内测试副本并入 tests/cases 后删除；description 前加中文触发语，泛称路由改成实名；示例命令改用 python3 | patch |
| 0.1.0 | 2026-09-09 | 初始版本 | minor |
