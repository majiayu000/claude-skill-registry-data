---
name: daftai-image-to-svg
description: >
  Converts transparent or solid-background single-color PNG files and SVG files containing one embedded
  or local PNG into verified path-only SVG output. Removes pure-color backgrounds automatically. Uses Potrace threshold
  and parameter scans with alpha error metrics to preserve detailed logos, stamps, engravings, and
  line art. Use when the user asks to convert images to SVG, vectorize PNG, convert bitmap to true SVG,
  remove embedded raster data from SVG, 图片转矢量, PNG 转 SVG, 真矢量, or 位图描摹.
metadata:
  openclaw:
    requires:
      anyBins:
        - bun
---

# Image to SVG

Convert transparent or solid-background single-color artwork into a genuine SVG containing paths rather than an embedded bitmap.

Automatic tracing approximates the raster boundary. Only the original vector source can provide mathematically exact curves.

## Scope

Supported:

- Transparent PNG.
- PNG on a pure-color background, including white, red, green, or other flat colors.
- SVG containing exactly one Base64 or local PNG.
- Single-color logos, stamps, engravings, silhouettes, and detailed line art.

Reject:

- Photos, gradients, textured backgrounds, and multicolor artwork.
- Remote image URLs.
- SVG mixing raster artwork with existing paths.
- Centerline or editable-stroke reconstruction.

For multicolor artwork, recommend VTracer instead of forcing this workflow.

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:

1. Determine this SKILL.md file's directory path as `SKILL_DIR`.
2. Set command working directory to `${SKILL_DIR}`.
3. Execute `bun ${SKILL_DIR}/scripts/vectorize.ts`.
4. Replace `${SKILL_DIR}` with the absolute path.

| Script | Purpose |
|---|---|
| `scripts/vectorize.ts` | Extract alpha, scan Potrace candidates, measure error, and deliver the best path-only SVG |
| `scripts/vectorize.test.ts` | Unit and real-toolchain regression tests |

## Dependencies

Detect the runtime once per session:

```bash
command -v bun
command -v ffmpeg
command -v ffprobe
command -v potrace
command -v rsvg-convert || command -v inkscape
```

Required:

- Bun.
- FFmpeg and FFprobe.
- Potrace.
- One SVG renderer: `rsvg-convert` from librsvg, or Inkscape.

If a dependency is missing, install it directly with the available package manager. Report only when installation fails or no package manager is available.

Common macOS installation:

```bash
brew install oven-sh/bun/bun
brew install ffmpeg potrace librsvg
```

If Homebrew is unavailable, install with the platform package manager. Do not ask before installing missing conversion dependencies.

## Workflow

1. Confirm the input is within scope.
2. Run the converter:

   ```bash
   bun ${SKILL_DIR}/scripts/vectorize.ts "/absolute/path/to/input.svg"
   ```

3. Read `<source-slug>.report.json`.
4. Confirm:
   - `structure.pathCount >= 1`;
   - `structure.imageCount === 0`;
   - `structure.dataImageCount === 0`;
   - `verified4x === true`.
   - `backgroundRemoval.applied === true` only when the input had a solid background.
5. Inspect the PNG preview, especially fine lines, holes, hatching, and sharp corners.
6. Report the SVG, preview, selected threshold, MAE, RMSE, and IoU.

Choose the objective explicitly:

- Use default `mae` for the closest alpha appearance.
- Use `iou` for overlap, contour match, 轮廓重合率, or IoU requests.
- Use `rmse` only when large alpha errors matter more than average error.

Never describe the result as lossless. Say “high-fidelity true vector” and include measured error.

## Usage

Specify an output parent directory:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts input.png --output-dir ./output
```

Override the detected color:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts input.svg --color "#0113a8"
```

Use solid-background PNG directly; do not preprocess manually:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts "logo-on-white.png"
```

Preserve all threshold candidates for manual comparison:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts input.svg --keep-candidates
```

Temporary candidates are deleted by default. Keep them only when tuning, comparing versions, or resolving visual review disputes.

Advanced threshold control:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts input.svg \
  --threshold-min 120 \
  --threshold-max 140 \
  --threshold-step 2
```

Validated defaults are `124..144`, step `2`, Potrace `alphamax=0.2`, and optimization tolerance `0.03`.

Optimize for binary outline overlap and scan Potrace smoothing:

```bash
bun ${SKILL_DIR}/scripts/vectorize.ts input.svg \
  --objective iou \
  --threshold-min 122 \
  --threshold-max 132 \
  --threshold-step 1 \
  --alphamax 0,0.2 \
  --opttolerance 0,0.03
```

For detailed hard-edge art, `alphamax=0` can raise IoU by avoiding curve smoothing. Do not hard-code color during experiments; inherit wrapper fill or use `--color`.

## Output

Single-file runs write directly into the chosen output directory:

```text
<output-dir>/
├── <source-slug>.svg
├── <source-slug>.preview.png
└── <source-slug>.report.json
```

Default runs do not create `candidates/`. With `--keep-candidates`, also write all measured candidates:

```text
<output-dir>/
├── <source-slug>.svg
├── <source-slug>.preview.png
├── <source-slug>.report.json
└── candidates/
    ├── candidate-t128-a0-o0.svg
    ├── candidate-t128-a0-o0.png
    └── ...
```

If `--output-dir` is omitted, create `<source-slug>-svg-output/` next to the input. Existing results are never overwritten; repeated runs append a timestamp to the output filename prefix. Do not copy the source file by default; the report records `sourcePath`.

For multiple input files, create one subdirectory per source under the chosen output parent to avoid collisions:

```text
<output-parent>/
├── first-image/
│   ├── first-image.svg
│   ├── first-image.preview.png
│   └── first-image.report.json
└── second-image/
    ├── second-image.svg
    ├── second-image.preview.png
    └── second-image.report.json
```

The report records `backgroundRemoval` when a pure-color background was converted to alpha. Intermediate PGM files remain temporary; candidate SVG/PNG files are preserved only with `--keep-candidates`.

## Validation

Run:

```bash
bun test ${SKILL_DIR}/scripts/vectorize.test.ts
```

For final delivery, also validate the generated SVG:

```bash
xmllint --noout "/path/to/result.svg"
rg -o '<path\b|<image\b|data:image/' "/path/to/result.svg" | sort | uniq -c
```

The final SVG must contain paths and no raster references.
