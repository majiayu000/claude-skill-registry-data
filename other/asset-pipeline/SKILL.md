---
name: asset-pipeline
description: Rules for files under assets/ in Iron Pipeline — Git LFS tracking, the assets-src/manifest.yaml provenance entry (fields, allowed values), licensing, Godot import formats, and the no-real-world-IP rule. Load before adding or changing anything under assets/ or assets-src/, or when reviewing such a change.
---
# Asset pipeline rules

`assets-src/manifest.yaml` is the provenance record for everything under `assets/`. It doubles as the Steam AI-generated-content disclosure record.

## Layout
| Path | Holds |
|---|---|
| `assets/` | shipped game content. `assets/LICENSE` (all rights reserved, not MIT) covers it. Every file except `.gitkeep` and `LICENSE` needs a manifest entry. |
| `assets-src/manifest.yaml` | one provenance entry per file under `assets/` |
| `assets-src/prompts/` | prompt files referenced by `prompt_file` |
| `assets-src/out/` | raw generation scratch; gitignored, never committed |

## Git LFS
Every new binary under `assets/` must be LFS-tracked. `.gitattributes` routes these through LFS: `*.png *.jpg *.webp *.ogg *.wav *.mp3 *.ttf *.otf`.
- Verify a file: `git check-attr filter <file>` must print `filter: lfs`.
- A binary type not in that list needs a `.gitattributes` line to be LFS-tracked.

## Manifest entry
`path` is relative to `assets/`. Fields and allowed values, from the manifest header:

| Field | Values |
|---|---|
| `path` | e.g. `units/mbt-ridgeback.png` |
| `kind` | `sprite`, `tile`, `icon`, `music`, `sfx`, `voice`, `font` |
| `source` | `generated`, `purchased`, `handmade`, `public-domain` |
| `tool` | for generated, e.g. `ComfyUI` |
| `model` | for generated, e.g. `z-image-turbo-fp8` |
| `prompt_file` | for generated, e.g. `prompts/units/mbt-ridgeback.txt` |
| `seed` | for generated, e.g. `123456` |
| `post` | post-processing, e.g. `"background removed, 128x128, palette locked"` |
| `license` | `all-rights-reserved`, `CC0`, or `<tool license>` |
| `commercial_ok` | `true` / `false` |
| `approved_by` | e.g. `jl` |
| `approved_on` | date |

Required on every entry: `path`, `kind`, `source`, `license`, `commercial_ok`, `approved_by`, `approved_on`. Also required when `source: generated`: `tool`, `model`, `prompt_file`, `seed`.

The license must permit commercial use, or the entry must say otherwise (`commercial_ok`).

`scripts/check-asset-manifest.sh` (run by `scripts/verify.sh`) only checks that some line contains `path: <file>`, as a substring match. Exact paths, field completeness and license are checked in review.

## Formats for Godot import
- Sprites: PNG with alpha.
- Audio: OGG.
- Dimensions and format must be sensible for Godot import.

## No real-world IP
- No real-world trademarks, logos, insignia or named real vehicles in prompts or filenames.
- Faction content follows `assets-src/prompts/factions.md`: original names only, with no real nations, alliances, armed forces or thinly-veiled copies, and no real-world symbols.
