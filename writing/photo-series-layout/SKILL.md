---
name: photo-series-layout
description: 当使用者说"把这几张照片拼成一页"、"拼成一张长图"、"这组照片排成一页 PDF"时使用。Arrange 3–9 finished photographs into a cohesive one-page series, contact sheet, long image, or PDF. Use when a user wants to sequence and present a photo set with consistent frames, gutters, and canvas treatment. Preserve the photographer's chosen order unless they explicitly ask for sequencing suggestions; do not infer artistic intent from pixels alone. For a publication or exhibition-board layout with bands, a lead photo per band and a credit per band, or more than 9 photos, use photo-spread-composer.
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

# Photo Series Layout

Turn a small set of finished photographs into one coherent page without silently changing their meaning, order, or content.

## Scope

Use this skill when the user has **3–9 photographs** and wants one of these outputs:

- a one-page grid or strip;
- a single long image;
- a one-page PDF;
- a layout plan that another renderer can implement.

Do not use it to select the best photographs, retouch images, invent captions, or infer a photographer's intent. If the user needs EXIF framing first, treat each framed image as an input asset and do not add a second frame here.

Routing:

- The user's own 3–9 photos, wanted as one long image, grid, or one-page PDF in the order given: this skill.
- A publication or exhibition-board layout with bands, a lead photo in each band, captions, and a credit per band, or more than 9 photos: use `photo-spread-composer`.
- A single photo: a caption goes to `photo-caption-writer`, a shooting-data frame to `photo-exif-frame`, a minimal geometric poster to `photo-poster-stylist`.

## Inputs

Collect or derive only what is needed:

1. ordered image paths;
2. output path and format (`PNG`, `JPEG`, or one-page `PDF`);
3. layout intent: `auto`, `grid`, `horizontal`, or `vertical`;
4. canvas target, if any (pixels, aspect ratio, or print size plus DPI);
5. background, outer margin, gutter, and fit mode (`contain` or `cover`);
6. whether reordering suggestions are wanted.

If paths or output format are missing, ask. For unspecified visual settings, state the defaults before rendering. Never invent image order.

HEIC files (the iPhone default) need the pillow-heif package. Without it, convert a copy first; on macOS `sips -s format jpeg IMG_0001.HEIC --out IMG_0001.jpg` keeps the EXIF. The renderer stops on a HEIC input and prints this command; it never skips the file.

## Workflow

### 1. Establish the sequence

Treat the supplied order as authoritative.

If the user explicitly requests help sequencing, offer at most three **candidate** orders based only on observable or supplied attributes:

- chronological or event order;
- light-to-dark or warm-to-cool progression;
- repeated-form or visual-rhythm progression.

Label the basis of each candidate and ask the user to choose. Do not claim a narrative or emotional arc the photographer did not provide.

### 2. Choose a layout family

Read [references/layout-rules.md](references/layout-rules.md), then choose:

- `horizontal`: a left-to-right sequence, usually 3–5 images;
- `vertical`: a top-to-bottom sequence or long image;
- `grid`: equal cells for comparison or contact-sheet presentation;
- `auto`: the renderer picks the grid with no empty cell whose page shape is closest to the canvas, or to one cell's shape (4:3 by default) when no canvas is given. For 5 or 7 photos the only such grid is a single strip; the renderer then prints the `--columns` value for a compact grid with one empty cell at the end, which needs the user's approval.

The renderer reports grids as "C columns x R rows"; report them to the user in the same order. `references/layout-rules.md` lists what `auto` picks for 3–9 photos.

Prefer one consistent cell shape. Use an asymmetric layout only when the user identifies a lead image and approves the hierarchy; the bundled renderer intentionally does not invent asymmetric prominence.

### 3. Decide cropping policy

Use `contain` by default: preserve every photograph and allow background bars within cells.

Use `cover` only with explicit permission because it crops. Before rendering, say that edge content may be removed. Never stretch an image.

The renderer applies EXIF orientation and writes the page in one colour space. When every photo has the same RGB profile (for example all Display P3 from one iPhone), the page keeps that profile and embeds it. When profiles differ, or one is CMYK or grey, every photo is converted to sRGB and sRGB is embedded; untagged photos count as sRGB. PDF output is always converted to sRGB, because the PDF writer cannot embed a profile. Transparent areas take the background colour. Source files are never modified, and the output path may not be one of the inputs.

### 4. Render deterministically

The bundled renderer requires Python 3 and Pillow (`python3 -m pip install Pillow`); `scripts/image_io.py`, the image module shared with the other photo skills, must stay next to it. Run the commands from this skill's directory:

```bash
python3 scripts/layout_photos.py \
  --output series.png \
  --layout auto \
  --fit contain \
  image-01.jpg image-02.jpg image-03.jpg
```

For a vertical long image:

```bash
python3 scripts/layout_photos.py \
  --output series.pdf \
  --layout vertical \
  --cell-width 1800 \
  --cell-height 1200 \
  --margin 120 \
  --gutter 48 \
  image-01.jpg image-02.jpg image-03.jpg
```

Run `python3 scripts/layout_photos.py --help` for all options and `python3 scripts/layout_photos.py --selftest` to check the renderer. Pass input paths as separate arguments; do not build an unquoted shell string from user-supplied paths.

If Pillow is unavailable, provide the exact command and dependency requirement rather than pretending the file was rendered.

### 5. Inspect the result

Check all of the following:

- every requested input appears exactly once;
- order matches the approved sequence;
- no image is stretched;
- `contain` loses no image area;
- `cover` cropping is acceptable to the user;
- margins and gutters are consistent;
- text, logos, or extra decoration were not introduced;
- output dimensions and format match the request.

For print, additionally confirm physical size at the requested DPI and recommend a print-preview check. Do not claim color accuracy without a color-managed proofing workflow.

## Output report

Return:

- output path and pixel dimensions;
- ordered input list;
- layout as "C columns x R rows", empty cells, fit mode, margin, gutter, and background used;
- colour handling, taken from the renderer's `colour:` field (profile kept, or converted to sRGB);
- any crop warning or degraded behavior;
- one concise note on what still requires human visual approval.

## Failure handling

- Fewer than 3 or more than 9 inputs: stop and ask whether to change the set; do not silently drop images.
- Missing, unreadable, or unsupported image: identify it and stop before writing output. For HEIC, pass on the `sips` command the renderer prints.
- Duplicate path: stop and ask. If the user confirms the repetition is intentional, rerun with `--allow-duplicates`.
- Existing output: require `--overwrite`; never replace it silently. The renderer refuses an output path that is one of the inputs, even with `--overwrite`.
- Empty cells (`--columns`, or `--layout grid` with 3, 5, 7, or 8 photos): only with the user's approval; the renderer prints a note when a grid has them.
- Mixed aspect ratios: default to `contain`, not aggressive cropping.
- Multi-page request: explain that this skill and renderer produce one page; propose splitting only after the user approves the grouping.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.2.0 | 2026-09-26 | 实现 references 写的 auto 排布（先求无空格、再选最接近画布比例，8 张不再 3×3 空一格）；加 --allow-duplicates 放行已确认的重复照片，输出不得是输入照片；按共同 ICC 输出（同一 RGB 配置文件保留嵌入，混合时转 sRGB，PDF 一律 sRGB），透明区铺背景色；网格统一写"列×行"；HEIC 给 sips 提示；补 --selftest、Pillow 依赖与 python3 命令、与 photo-spread-composer 的判别句和中文触发语；目录内测试副本并入 tests/cases 后删除 | minor |
| 0.1.0 | 2026-09-09 | 初始版本 | minor |
