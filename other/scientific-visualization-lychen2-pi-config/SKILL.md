---
allowed-tools: Read Write Edit Bash Glob Grep
compatibility: Requires Python 3.11+ and uv for pinned examples. Bundled CLIs are network-free and load Matplotlib, Pillow, or pypdf only when needed. Plotly static export with Kaleido v1 requires a compatible Chrome/Chromium installation.
description: Create publication-ready scientific figures. Use when plotting analyzed results or preparing journal graphics.
license: MIT
metadata:
    github-path: skills/scientific-visualization
    github-pinned: v2.65.0
    github-ref: refs/tags/v2.65.0
    github-repo: https://github.com/K-Dense-AI/scientific-agent-skills
    github-tree-sha: 232740861698bb81a29e3bb312d36f9ae629f6f5
    skill-author: K-Dense Inc.
    version: "1.1"
name: scientific-visualization
---
# Scientific Visualization

Build figures that preserve scientific meaning before optimizing appearance. Separate universal principles from dated publisher rules, preserve raw data and transformations, use color redundantly, and inspect delivered files rather than trusting plotting defaults.

## Figure integrity and delivery

Preserve source data and processing history. Choose encodings, axes, labels, and uncertainty displays that represent the data accurately. Check publication rules when a specific submission requires them; general plots do not need a journal audit.

Deliver figures and captions that explain the science. Keep production checks and publication-status notes in working records or native comments; if comments are unavailable, use the conversation outside the artifact. Do not put compliance claims or routine disclaimers in titles, captions, or figure panels. These output rules also apply when using the reference checklists. Native comments mean comments attached to the source document or figure file; captions and footnotes remain reader-visible and are not substitutes for comments.

**Audience-view check:** inspect the exported figure and caption without the production conversation. Labels and caption should state what was measured, encoded, and necessary to interpret it. Put a genuine model condition beside the affected result (for example, “Values are normalized to baseline; absolute levels are not comparable”), not in a defensive disclaimer panel. Omit “not a reproduction” or source-relationship commentary. Keep provenance and export checks in the manifest or working record; include comparisons, limitations, or disclosures when they are scientifically needed or explicitly required.

Use the relevant accessibility features for the medium, and distinguish interactive outputs from static exports.

Read `references/publication_guidelines.md` for deceptive-encoding and integrity checks. Read `references/journal_requirements.md` only after the target and phase are known.

## Workflow

### 1. Define the evidence and destination

Record:

- audience and medium: manuscript, web, slide, poster, supplement;
- exact publisher/journal, article type, submission phase, and intended final width;
- variable semantics, units, sample/replicate structure, missing/censored values;
- estimator and uncertainty definition;
- transformations: filtering, aggregation, normalization, smoothing, bins, image processing;
- source-data paths/identifiers and output provenance.

Use reasonable general figure settings when no publication target is specified. Resolve exact publisher requirements when preparing that submission, without adding a pending-verification label to the figure.

### 2. Choose an honest encoding

Prefer position on a common scale. Before coding, check:

- **Bars/areas:** normally include zero because length/area is measured from a baseline.
- **Points/lines:** nonzero limits can be valid; show context and disclose breaks.
- **Uncertainty:** name SD, SE, CI, percentile, posterior, or another interval; state `n` and the unit of replication.
- **Raw observations:** show them when feasible; do not let jitter obscure categories/values.
- **Missing data:** distinguish missing, zero, censored, and excluded; use gaps or explicit model/interpolation styling.
- **Area/volume:** scale area/volume, not radius/diameter; avoid decorative 3D.
- **Log axes:** label the base/transform and declare how zero/negative values are handled.
- **Binning/smoothing:** record edges, bandwidth/window, method, and sensitivity.
- **Normalization:** state formula/reference and keep limits consistent across compared panels.
- **Dual axes:** prefer aligned panels; if unavoidable, justify units and do not engineer apparent correlation.
- **Images:** preserve originals, disclose whole-image adjustments, show scale bars, and avoid clipped/erased background.

### 3. Design accessibility in, not after

- Use color plus marker, line style, hatching, direct label, or panel separation.
- Choose qualitative, sequential, diverging, or cyclic color according to data semantics.
- Audit foreground/background contrast at the rendered size.
- Make missing and out-of-range values explicit.
- Provide alt text, a longer description for complex figures, and underlying data for web delivery.
- Treat WCAG 2.2 as web guidance: 4.5:1 normal text, 3:1 large text, and 3:1 for graphical objects required for understanding; color cannot be the only cue. Applicability and exceptions matter.

See `references/color_palettes.md`. A grayscale screen is useful but is not a complete color-vision or accessibility test.

### 4. Implement with scoped styles

Use Matplotlib's object-oriented API and temporary style contexts:

```python
import matplotlib.pyplot as plt

from style_presets import style_context

with style_context("default", palette_name="okabe_ito_on_white"):
    fig, ax = plt.subplots(
        figsize=(89 / 25.4, 60 / 25.4),
        layout="constrained",
    )
    ax.plot(x, y, marker="o", label="Observed")
    ax.set(xlabel="Time (hours)", ylabel="Response (unit)")
    ax.legend()
```

`layout="constrained"` supports colorbars, nested GridSpec, subfigures, and `subplot_mosaic`. Do not call `tight_layout()` afterward; it disables constrained layout.

For exact physical dimensions, do not use `bbox_inches="tight"` unless the changed page size is intentional.

#### Color normalization

```python
import matplotlib as mpl

norm = mpl.colors.TwoSlopeNorm(vmin=-2, vcenter=0, vmax=5)
cmap = mpl.colormaps["RdBu_r"].with_extremes(bad="#777777")
image = ax.imshow(values, norm=norm, cmap=cmap, interpolation="nearest")
fig.colorbar(image, ax=ax, label="Change (unit)")
```

Use `LogNorm`, `CenteredNorm`, `SymLogNorm`, `BoundaryNorm`, or `TwoSlopeNorm` only when its mapping matches the scientific meaning.

#### Seaborn

Seaborn 0.13.2 uses the current `errorbar` API:

```python
sns.lineplot(
    data=frame,
    x="time",
    y="response",
    hue="treatment",
    style="treatment",
    markers=True,
    errorbar=("ci", 95),
    n_boot=5000,
    seed=20260723,
    ax=ax,
)
```

Axes-level functions fit custom Matplotlib layouts; figure-level functions create their own figures/facets. Do not customize Seaborn's internal artist lists as if they were stable API.

#### Plotly

- Use `write_html()` for interaction and `write_image()`/`plotly.io.write_images()` for static output.
- Kaleido 1.3.0 requires Chrome/Chromium; it no longer bundles Chrome.
- Current static formats: PNG, JPEG, WebP, SVG, PDF. EPS is Kaleido v0-only.
- Do not pass deprecated `engine=` or use Orca/`plotly.io.kaleido.scope`.
- `width`, `height`, and `scale` control pixels; `scale=3` is not inherently “300 DPI.”
- WebGL traces embed raster content in PDF/SVG.
- Fully offline exports need local external assets when a figure references MathJax/topojson/tiles.

### 5. Export explicitly and record provenance

```python
from figure_export import export_figure

report = export_figure(
    fig,
    "outputs/figure1",
    formats=["pdf", "png"],
    dpi=600,
    bbox_inches=None,  # preserve figure page dimensions
    provenance={
        "raw_data": "data/source.csv",
        "transformations": ["predeclared QC filter", "group mean"],
        "uncertainty": "95% bootstrap CI; seed 20260723",
        "missing_data": "retained as gaps",
    },
    write_manifest=True,
)
```

The exporter refuses implicit overwrite, writes atomically, keeps vector DPI for embedded rasters, uses TIFF LZW, and can use PDF/PS Type 42 fonts. It does not validate scientific content or publisher acceptance.

For editable fonts:

- PDF/PS Type 42 embeds TrueType fonts.
- `svg.fonttype="none"` keeps text editable/searchable but does not embed fonts; appearance depends on installed fonts.
- `svg.fonttype="path"` preserves glyph appearance as paths but loses editable/searchable text.

Use an opaque explicit background unless transparency is required; blending against another background changes apparent contrast.

### 6. Inspect, compare, and review

1. Inspect file metadata.
2. Audit palette contrast/grayscale separation.
3. Compare against a dated publisher snapshot.
4. View at final size in the manuscript/web context.
5. Manually review fonts, embedded rasters, clipping, legends, scale bars, image integrity, caption, alt text, and source data.
6. Re-check the live target-journal page immediately before upload.

## Pinned snapshot

The examples and smoke tests use direct package pins current on 2026-07-23:

```bash
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.1" \
  --with "seaborn==0.13.2" \
  --with "plotly==6.9.0" \
  --with "kaleido==1.3.0" \
  --with "pillow==12.3.0" \
  --with "pypdf==6.14.2" \
  python your_figure.py
```

This is a dated direct-dependency snapshot, not a transitive lock. Use the project's uv lock for exact replay; this skill intentionally ships no dependency lock.

## Bundled CLIs

All helpers are deterministic, network-free, bounded, reject symlink inputs/destinations where relevant, and refuse overwrite unless `--force` is explicit.

### Inspect raster/vector metadata

```bash
uv run --isolated --no-project --python 3.13 \
  --with "pillow==12.3.0" \
  python scripts/image_metadata.py figure.tiff \
  --format tiff --mode RGB --min-dpi 300 --target-width-mm 85 \
  --alpha-policy forbid
```

Supports raster images (Pillow), SVG, PDF (pypdf), and EPS/PS. Reports dimensions, DPI/effective DPI, mode, alpha, ICC presence, compression, page size, and conservative first-page PDF font resources. It does not inspect every embedded raster in a vector container.

### Audit palette contrast and grayscale

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/palette_audit.py \
  --palette okabe_ito_on_white \
  --background FFFFFF \
  --role graphical
```

Reports exact WCAG sRGB contrast plus pairwise CIE L* grayscale screening. The grayscale threshold is a heuristic, not a standard.

### Plan/screen publisher export

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/export_plan.py \
  --publisher nature \
  --figure-type combination \
  --width single \
  --phase final
```

Add `--input figure.pdf` to screen machine-readable properties. Profiles are official-source snapshots accessed 2026-07-23, not automatic compliance rules.

### Preview styles

```bash
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.1" \
  python scripts/style_preview.py \
  --output outputs/style-preview \
  --style default \
  --palette okabe_ito_on_white \
  --formats png,svg
```

### Inspect/write styles and smoke-test export

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/style_presets.py --list
uv run --isolated --no-project --python 3.13 \
  python scripts/style_presets.py --show nature
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.1" \
  python scripts/figure_export.py --demo outputs/export-smoke --manifest
```

## Assets

- `assets/publication.mplstyle`: general print starting point.
- `assets/nature.mplstyle`: dated flagship Nature visual starting point, not a compliance preset.
- `assets/presentation.mplstyle`: larger projected-display style.
- `assets/color_palettes.py`: importable Okabe-Ito and Paul Tol values with metadata.
- `assets/publisher_profiles.json`: dated, machine-readable planning snapshots.

Matplotlib style files omit `#` in hex colors because `#` begins comments in `.mplstyle` parsing.

## References

- `references/publication_guidelines.md`: integrity, deceptive encodings, accessibility, static/interactive output.
- `references/color_palettes.md`: palette semantics, exact values, WCAG contrast, grayscale caveats, color management.
- `references/journal_requirements.md`: phase-specific official publisher snapshots.
- `references/matplotlib_examples.md`: current, runnable Matplotlib/Seaborn/Plotly patterns.
- `references/sources.md`: official URLs, dates, versions, and research basis.

## Final review checklist

- [ ] Raw data/images and transformation code are preserved.
- [ ] Missing values, exclusions, bins, normalization, and uncertainty are explicit.
- [ ] Baselines, scales, limits, and area/volume encodings are honest.
- [ ] Color is redundant and rendered contrast was reviewed.
- [ ] Figure has an accessible description/data alternative where applicable.
- [ ] Physical dimensions, DPI, format, fonts, transparency, and file size were inspected after export.
- [ ] Publisher rules were verified for the exact journal and phase.
- [ ] No automated report is presented as a scientific, accessibility, or compliance certification.
