---
name: spritesheet-expert
description: "Make game sprites from generated art: animation sheets, icon and item atlases, pose sets, tiles, backgrounds and UI. Plans the generation prompt and layout guide, then cuts out, registers, packs and reviews the result with one CLI."
---

# Spritesheet Expert

One CLI, four commands. The image model draws; `sprite.py` does everything else.

```text
plan   → run.json, one sheet prompt + layout guide (all states or sets of a run in one image)
(you)  → generate that sheet with the anchor + guide attached
build  → cutout, frames on one baseline and one body size, atlas, previews, review.html
repair → in-between kit for each bad frame; regenerate it and rebuild with --patch
check  → report problems; --strict blocks delivery
```

Run commands from this folder: `python sprite.py <command> --help`.
Requires Python 3.11+, Pillow, numpy and scipy.

## Lanes

| Lane | Use for | Recipe |
| --- | --- | --- |
| `animation` | Walk, run, idle, attack, jump, hurt, cast, VFX rows | [recipes/animation.md](recipes/animation.md) |
| `slots` | Named cells without time: character poses and gestures, icons and items, UI states, nine-slice panels | [recipes/slots.md](recipes/slots.md) |
| `atlas` | Loose items without a grid: separated by shape, named, packed tightly | [recipes/atlas.md](recipes/atlas.md) |

Tiles and backgrounds come next. Until then, use the v1 skill for them.

## Rules

- **Style follows the request.** Never add a style the user did not ask for.
  Put their words in `--style`; leave it empty when they gave none.
- **The agent calls the image provider.** `plan` writes the prompt and the
  references to attach. The CLI never calls a provider and never holds secrets.
- **Anchor first for characters.** Get one approved image of the character,
  pass it as `--anchor`, and attach it to every generation. Identity drift is
  the most common failure.
- **One image first, then repair.** Generate all states of a character in one
  sheet (`prompts/_all.txt` + `guides/_all.png`): frames drawn together share
  color, light and motion. Build, review, then fix only the bad frames with
  `repair` (neighbors + pose) and `build --patch`. Separate images per frame
  or per state drift in color and light.
- **Native alpha first.** Ask for a transparent background. When the provider
  cannot, a flat `#808080` gray works: `build --cutout auto` removes it,
  including enclosed holes, and un-mixes edge colors.
- **Look before you ship.** Open `review.html`. Play every state, use onion
  skin and the four backgrounds, and read every check that is not `pass`.
  Checks are hints, not proof. Regenerate a sheet instead of patching pixels.
- **Record the source.** `build --source state=image --provider "<name>"`
  copies the image into the run and stores its SHA-256. A source that changes
  after ingest fails `build` and `check`.

## Outputs

| File | What it is |
| --- | --- |
| `atlas.png`, `atlas.json` | One row per state or set, fixed cells, pivot; frame durations (animation) or slot names and nine-slice margins (slots) |
| `frames/<state>/NN.png` | Each runtime frame |
| `previews/<state>.webp` | Animated preview with alpha (animation only) |
| `review.html` | Self-contained review page: play, step, onion skin, mattes, checks, source |
| `run.json` | Plan, sources with hashes, build report and checks |

## Cutout options

`--cutout auto` (default) uses native alpha, else removes a flat matte.
`--cutout birefnet` runs BiRefNet on CPU for busy backgrounds; it needs
`pip install "rembg[cpu]"`.
