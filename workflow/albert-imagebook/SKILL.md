---
name: albert-imagebook
description: >-
  Transform photos into illustrations, stickers, paper cutouts and pixel art with reusable
  style directions, open space and exact-size exports. Use for photo-to-art, 照片转插画,
  照片贴纸, named Imagebook styles, or original-and-art comparisons.
license: MIT
metadata:
  version: "0.3.0"
  author: AlbertAZ1992
---

# Albert’s Imagebook

One installable Skill, one shared image workflow, and 24 photo-to-art styles.
Resolve package paths relative to this file, including when installed outside the repository.

## Select the source and style

Inspect the user's attached photo or explicit local file. For a directory, inventory image files,
exclude hidden files and generated output, and avoid following symlinks outside that directory.
Process each original independently; do not apply successive styles to previously generated art.

Discover styles from `styles/*/prompt.md`. Titles, descriptions, keywords and aliases identify
both Chinese and English names. The directory name is the stable style ID. A new prompt file
is immediately usable; no catalog or extra Skill installation is required.

Use a named style directly. If asked to recommend, offer a few source-specific choices; if asked
to choose and generate, choose and proceed. Some newer styles currently have one beach study rather
than several source examples, but they are selected and run through the same prompt-file workflow.
For an unfamiliar style with a supplied visual reference, derive its material and composition from
that reference. Clarify only when neither the name nor the reference establishes a usable direction.
Sample artworks are for browsing, not image references unless requested.

Read the selected prompt completely. For established styles, pass everything after `## Prompt` to the image model
unchanged. Follow it with one delivery block and any explicit user requirements. The style prompt
owns interpretation, palette, material, mark-making and optional typography. Do not add a
second art direction, motif quota, color plan, caption package or copied sample composition.

## Resolve delivery

Default: one **design-only portrait, 1080×1440, no new text**. Keep visual content below a
65% ceiling within the artwork canvas; generally aim around 45–55% or less. Judge the overall
scene footprint, including spaces inside the subject group, not just pigment-colored pixels.
Keep its overall width and height comfortably within the paper. A sparse style
should stay much sparser, never expand to meet a target. These are composition instructions,
not guaranteed pixel measurements or an inset rectangle. In comparisons this applies only
to the artwork half; the original photo continues to fill its own half.
Default to an optically centered, stable composition with balanced space on opposing sides;
handmade marks may be uneven without making the whole scene tilted or displaced.
The style determines subject selection, scale and how marks meet the surrounding paper.
State omitted defaults briefly and proceed when source and style are clear. Explicit choices win.
Ask only about material ambiguity, such as missing exact wording or conflicting instructions.

| Preset ID | Chinese name | Aspect | Final PNG size |
| --- | --- | --- | --- |
| portrait | 竖版 | 3:4 | 1080×1440 |
| feed | 信息流 | 4:5 | 1080×1350 |
| square | 方形 | 1:1 | 1080×1080 |
| story | 全屏竖版 | 9:16 | 1080×1920 |
| landscape | 横版 | 16:9 | 1920×1080 |

These are product export presets, not claims about platform upload limits. Custom sizes and
source aspect are allowed. Resolve aspect-only requests to integer pixels before generation.
For automatic sizing, choose a preset appropriate to the photo and intended use.

- `design-only` / 只要作品: one full artwork, original used as reference only. Photo Play retains
  photographic subjects as part of its mixed-media artwork.
- `top-bottom` / 上下对照: original above, artwork below, exactly 50:50.
- `left-right` / 左右对照: original left, artwork right, exactly 50:50.
- `wallpaper-pack` / 壁纸套装: separate phone, tablet, desktop and watch artworks at resolved
  device sizes. For a coherent set, use its first artwork alongside the source for later images;
  otherwise generate each independently. Each output uses design-only export.

Text can be absent, supplied verbatim, or generated according to the style in a specified language.
No new text means no added lettering, captions, signatures, watermarks or pseudo-text.
On generated painted or modeled objects, omit source lettering under no-new-text delivery.
Existing markings on an original-photo panel or retained photographic subject stay unless removal is
requested. For generated copy, names, dates and documentary facts must be supplied or established
by the source. Exact supplied wording overrides optional text in a style prompt.

Count source/style/layout/size combinations before a batch. Each chosen wallpaper device is one
output; do not also multiply it by ordinary social presets. Use one fresh image call per artwork.

## Generate the complete artwork

Run the export plan before generation. It resolves the final canvas and each comparison panel.
Generate the complete artwork, including its paper/background and breathing space, at the panel
aspect using the closest supported dimensions. A portrait top-bottom comparison uses a 3:2
artwork; a landscape left-right comparison uses an 8:9 artwork.

Append this delivery block to the complete style prompt:

```text
DELIVERY FOR THIS IMAGE
Source: attached original photo, reference for its subject and relationships.
Canvas: <panel aspect and tool-supported pixels>.
Layout: one complete standalone artwork, no original-photo panel or comparison.
Composition: the overall scene footprint must occupy no more than about 65% of this canvas.
Aim around 45–55% or less, allowing substantially more open paper for a sparse style.
Include the gaps inside the subject group when judging its overall extent; sparse pigment
alone does not make a nearly edge-to-edge scene small. Keep the group optically centered,
with balanced opposing margins and a stable, level composition unless requested otherwise.
The ceiling is not a fill target. Let open paper flow between forms as well as around them;
do not recreate the whole photographic background just to occupy the available area.
Make the scene readable through the style's chosen subjects and relationships.
Compose an organic balance rather than a measured rectangle or uniform border. Generate the surrounding
paper/background as part of the same artwork. Preserve the style's natural edge treatment:
broken marks, exposed paper, dragged pigment, or soft fading where appropriate to its medium.
Let peripheral marks become sparse and give way to the background before reaching the canvas
edges; keep the focal subject intact. Avoid straight rectangular scene cutoffs and a picture
pasted onto a mat. The export script will preserve this complete composition without adding margins.
Text: <no new text; exact supplied wording; or style-led wording in specified language>.
Keep the selected style's material, color logic and subject interpretation.
```

Keep open ground within and around the artwork, using edges appropriate to its medium.
Paint and ink may disperse or break; stickers need a clean die-cut rim, cardstock needs cut edges
and shallow shadows, pixels need crisp steps, and line art needs deliberate open contours.
Do not add painterly fading to these graphic forms. A requested letter mask or arch is an
intentional design boundary, not an accidental rectangular crop. For enamel or photographic subjects, keep the object or
person intact and apply this transition to the surrounding marks and environmental fragments.
The style files describe what to draw and how, including negative space and material-specific
edges. Preserve these instructions. The shared workflow sets delivery size, overall breathing
room and photo-and-art placement; it must not override the style's brushwork with full-bleed fill.
Do not impose generic blur or feathering on every style: paint, wax, stamps and enamel have
different edge behavior. An explicit full-bleed or close-crop request overrides default spacing.

Use the available image-generation/editing tool, preferring the host's built-in tool and following
its actual schema. The model draws the complete composition; the script controls export size
and comparison assembly. Never repaint the original half with AI. Different aspects are independently
composed; do not stretch or crop the artwork to fit. If no image tool is available, explain what
is needed rather than returning a prompt as an image.

## Export and deliver

Use [scripts/compose.mjs](scripts/compose.mjs) for exact dimensions and 50:50 splits.
It resizes the complete generated artwork to its panel, preserving the existing paper, negative
space and natural painted edges. It adds no mat, border, background replacement or feather mask.
It requires Node 22+ and ImageMagick 7 (`magick`). Run it from the installed Skill path:

```bash
node <skill-dir>/scripts/compose.mjs --plan --layout top-bottom --preset portrait
node <skill-dir>/scripts/compose.mjs --source photo.jpg --art generated.png \
  --layout top-bottom --preset portrait --out comparison.png
node <skill-dir>/scripts/compose.mjs --art portrait-artwork.png \
  --preset portrait --out artwork.png
```

Use `--size WIDTHxHEIGHT` instead of `--preset` for custom dimensions; the split axis must be even.
Custom spacing or full bleed belongs in the generation request, not an export-area percentage.
--background accepts a six-digit hex color for unused space in the original-photo panel only;
the default is warm white (#f6f3ed). It does not change the generated artwork's background.
The script refuses larger artwork aspect mismatches, tolerates at most two pixels of rounding,
and never overwrites existing outputs. [CLI help](scripts/compose-help.txt) has all options.

Photo placement defaults to `--photo-fit cover`: fill the original-photo half edge to edge,
without padding or separator strips. Preserve its aspect and crop only the excess. Inspect the
crop before delivery, especially people near the edges. `--photo-gravity` defaults to center;
choose west/east/north/south or a corner when needed to retain the important subjects.
For example, `--photo-gravity west` keeps a subject near the left edge in a wide source photo.
Mention any meaningful crop. Never stretch or AI-repaint the original to fill its half.
Use `--photo-fit contain` only when the user explicitly wants the entire original with padding.
If the user requires both no crop and no padding, plan panels at the source aspect and generate
the artwork at that aspect. A fixed incompatible canvas, exact 50:50 split, no crop and no padding
cannot all be satisfied together; explain that conflict rather than silently adding white bars.
No divider or labels are added by default. In comparisons, the generated breathing space belongs
to the artwork half; the original-photo half uses its existing contain/cover placement.
Keep the raw generated image and export a standalone artwork too. Always give the complete
generated artwork, including its natural background, to --art. Do not crop it down to the painted
subject, remove its background, or supply a previously assembled comparison.
For a standalone version of a comparison artwork, export the raw file at the panel size in
design-only mode.

Inspect the actual artwork for style, source recognition, comfortable spacing and requested text.
Judge the artwork half by itself and in the finished comparison: does one relationship read
first, is there meaningful open paper between forms, and has the background become an almost
solid painted sheet? Check the overall footprint as well as the pigment: even thin marks can
span almost the whole page. Check optical centering and stable orientation. If the group feels
too large, displaced or above the 65% ceiling, correct its scale and position with the image
tool. Do not repair it with a smaller rectangular inset.
Pixel-based paper estimates are optional rough diagnostics; pale paint and paper texture can
confuse them. A passing estimate alone does not establish a comfortable composition.
For comparisons, inspect the top/outer edges and the seam for compositor-added padding. Under
the default cover placement, the photograph must reach all four edges of its half; do not mistake
letterbox bars for the generated artwork's intentional paper. Verify focal subjects survive the crop.
Check that the painted region meets the background naturally rather than ending at a rectangular
inset. If it was generated full bleed by mistake, regenerate with the corrected composition;
shrinking it onto a blank canvas or blurring its rectangular boundary does not repair the artwork.
For ordinary delivery, correct a visible missed requirement with one focused retry; report a
remaining limitation plainly. For an explicitly requested creative first-pass comparison, generate
one sample per direction and record visible limitations without automatically polishing every sample.
Confirm the actual final dimensions. If an exact aspect/export is unavailable, explain the
limitation instead of claiming a preset or exact split was delivered.

Save to the requested destination or a fresh `output/albert-imagebook/<job>/` in the user's working
directory. Copy tool-managed results there and preserve originals and earlier outputs. Name files
by source, style and layout; return the actual images and usable paths. Account for missing batch
outputs in the conversation, without adding failure logs to the public galleries.
