---
name: shoot-outing-review-card
description: 当使用者说"做一张这次外拍的回顾卡"、"把这次扫街做成回顾卡"、"看看我这次拍摄的参数习惯"时使用。Turn one photography outing into a shareable review card with a cover image, EXIF habit summaries, and a capture timeline. Use when the user wants to review a shoot, visualize focal-length/aperture/shutter habits, or make an outing recap from a folder of photos.
category: photography
version: 0.2.0
status: draft
priority: P2
compatible_agents:
  - claude-code
  - openclaw
  - cursor
  - codebuddy
  - generic-llm-agent
---

# Shoot Outing Review Card

Create an evidence-based visual recap of one photography outing. The card helps a photographer notice capture habits; it does not judge whether those habits are good or infer artistic intent.

## Inputs

Ask for only what is missing:

- image files from one outing (JPEG or TIFF; PNG and WebP also work; RAW files need JPEG previews; HEIC/HEIF needs the `pillow-heif` package or a JPEG copy first: `sips -s format jpeg IMG.HEIC --out IMG.jpg`, which keeps the EXIF on macOS),
- output path,
- optional title, subtitle (Chinese is fine), cover image, accent color, and font file.

If the files may be shared outside the user's device, confirm whether filenames or dates are sensitive. Never display GPS coordinates, camera serial numbers, owner names, or free-text EXIF comments.

## Workflow

1. **Confirm the set.** Treat the supplied files as one outing unless the capture times span more than 24 hours. If they do, report the span and ask whether to split it; do not silently combine separate outings.
2. **Read facts.** Run `scripts/make_review_card.py` to read capture time, focal length, 35 mm equivalent focal length when present, f-number, exposure time, ISO, and camera model. The capture time is DateTimeOriginal only: a file that carries only IFD0 DateTime (an edit or export time) counts as missing a capture time, stays off the timeline, and is named in a warning.
3. **Audit coverage.** Report how many files were readable and the coverage of each EXIF field. A statistic based on fewer than 3 observations or less than 30% coverage is labelled `insufficient data`, not interpreted.
4. **Choose the cover.** Prefer the user-selected file. Otherwise the script deterministically chooses the earliest landscape-oriented image (EXIF orientation applied, so a phone portrait stored sideways counts as portrait), falling back to the earliest readable image. Do not claim that the automatic choice is the “best” photo.
5. **Summarize habits.** Describe only visible distributions, for example “18–35 mm accounts for 62% of images.” Do not turn correlation into a story about intention or skill.
6. **Render and inspect.** Generate the PNG, then check that the title, sample counts, missing-data notes, labels, and timeline are legible. Preserve the JSON sidecar as the auditable source for every number shown.

## Deterministic tool

Requires Python 3.9+ and Pillow; fontTools is optional and lets the script check that a font has every glyph. `scripts/image_io.py` is a shared copy of the photo skills' image module; identical copies live in `photo-caption-writer`, `photo-exif-frame`, `photo-series-layout`, and `photo-spread-composer`, and `scripts/validate.sh` requires them to stay byte-identical, so never edit one copy alone. `python3 scripts/make_review_card.py --selftest` runs the regression checks.

```bash
python3 scripts/make_review_card.py \
  IMG_001.jpg IMG_002.jpg IMG_003.jpg \
  --output outing-review.png \
  --title "Sunday walk" \
  --subtitle "Riverside · 7 September 2026" \
  --accent "#E98A4B"
```

Useful options:

```text
--cover PATH          select the cover explicitly
--width PX            output width (default 1600; minimum 900)
--json PATH           JSON sidecar path (default: output name + .json)
--font PATH           font file for all text (default: an installed font that has
                      every glyph, e.g. Hiragino Sans GB or STHeiti for a Chinese title)
--no-camera-model     omit camera model from the card
```

The script exits 2 and writes nothing when no readable image is supplied, the selected cover is not among the readable inputs, the color is invalid, `--output` or `--json` is one of the input photos, `--output` does not end in `.png`, `.jpg`, `.tif`, or `.webp`, the title needs glyphs that no available font has (Chinese with no Chinese font installed, or a `--font` without them), the title or subtitle is too long to fit the card even at the smallest size, or the output cannot be written. It warns on stderr—but still produces a card—when EXIF is sparse, when a file has only an export time, or when files are skipped. A skipped file (HEIC/HEIF without `pillow-heif`, or a file Pillow cannot read) is printed with the reason, and for HEIC with the `sips` command; convert the HEIC files and re-run before delivering unless the user accepts a card without them, and report the skipped files either way.

## Output contract

Return:

1. the PNG review card (the format follows the `--output` extension; JPEG is written at quality 95). The card embeds the cover's RGB ICC profile, so a Display P3 cover keeps its colours;
2. a UTF-8 JSON sidecar containing input counts, time span, EXIF coverage, histogram bins/counts, cover-selection method, the cover and output colour profiles (`color`), the fonts used, and warnings;
3. a short factual note containing:
   - files included / files skipped,
   - capture-time span,
   - strongest distribution only when its field passes the coverage threshold,
   - any sparse or absent fields.

Do not fabricate missing EXIF. Use `unknown`, omit the affected chart, or label it `insufficient data`.

## Interpretation rules

- Use 35 mm-equivalent focal length when available for all included observations; otherwise use actual focal length and label it clearly. Do not mix the two scales in one histogram.
- Aperture buckets are based on recorded f-numbers, not inferred depth of field.
- Shutter buckets describe exposure duration, not subject motion.
- A timeline shows capture density, not importance or effort.
- Duplicate timestamps remain separate captures; this is a habit card, not a unique-scene count.
- Edited exports can carry rewritten or stripped metadata. State this limitation whenever coverage is incomplete.

## Boundaries

- This skill summarizes an outing. For framing one photo with its EXIF, use `photo-exif-frame`; for arranging several selected works, use `photo-series-layout`.
- It does not rank photographs, identify the photographer's style, diagnose technique, or infer emotion.
- It does not upload files or query external services.
- It does not alter source images; an `--output` or `--json` path that is one of the input photos is refused.

## Minimum verification

Before delivery, verify:

- output PNG opens and has the requested dimensions;
- the output path is none of the input photos, and every input photo is unchanged;
- JSON parses and its `included + skipped` equals the input count; skipped files are reported with their reason;
- every chart states both `n` and coverage;
- the title and subtitle show real characters, not boxes (a Chinese title needs a font with Chinese glyphs; the script picks one or stops);
- no private EXIF fields appear;
- an EXIF-free image produces a card with explicit missing-data labels rather than invented values.

Cases: `tests/cases/shoot-outing-review-card.md` (fixtures in `tests/fixtures/shoot-outing-review-card/`).

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.2.0 | 2026-09-26 | 新增 --font，默认按文字挑有字形的已装字体，中文标题不再是方块；--output/--json 指向输入照片时拒绝，不再把原 JPEG 覆盖成 PNG；自动封面按 EXIF 转正后的尺寸挑横图；拍摄时间只取 DateTimeOriginal，只有导出时间的图不进时间线；机身名不再重复厂商；HEIC 跳过时在 stderr 给出 sips 命令；封面 ICC 原样嵌入（P3 不再发灰）；加 --selftest；删掉与库级 UNLICENSED 矛盾的 license 行；description 前加中文触发语；示例命令改用 python3 | minor |
| 0.1.0 | 2026-09-09 | 初始版本 | minor |
