---
name: build-static-game-assets
description: "Static game assets: non-animated raster from imported art, Imagegen, or explicit Grok stills; props, pickups, decals, item icons, neutral-background cutouts, pivots, sizing, provenance, hashes, contact-sheet proof."
---

# Build Static Game Assets

Portable static-asset pack: explicit roles, dimensions, pivots, crop policy, licensing, provenance, proof.

## Workflow

1. Define the asset inventory.
   - Each id, role, target size, pivot, transparency rule, crop policy, scale class, license, shared style fingerprint.
   - This skill: non-animated assets. Frame sequences and atlases → `$spritesheet-expert`; backgrounds → `$build-game-backgrounds`; raster controls → `$build-game-ui-kits`.

2. Generate or import real source art.
   - `$imagegen` default for new user-facing bitmap art. Load `$grok-imagine` only for explicit Grok stills. Provider creates semantic pixels; local scripts may crop, remove backgrounds, resize, compose proof, validate — not draw replacement production art.
   - Isolated sources on flat gray, black, or white. Never request green, blue, cyan, or magenta chroma. Preserve subject neutrals: prefer BiRefNet/BEN2 or similar model-backed cutout when connected-matte removal is ambiguous.
   - Grok: review `--dry-run` first; `--ack-run` only with explicit current-task consent. Never call paid inference from tests.
   - Sources below one pack root with portable relative paths and SHA-256 pins.
   - Declare `source.provenance` per asset. Generated sources identify Imagegen or Grok; imported art and fixtures stay explicit. Fixture can test the pipeline; never representative production media.
   - Keep transparent margins; do not hide crop or pivot defects by resizing proof.
   - Identity, anatomy, edge quality, or requested semantics fail: regenerate via selected provider. Do not procedurally repaint the failed asset and present it as generated.

3. Write `static-pack.json` against `references/schemas/static-asset-pack-v1.schema.json`.
   - Require `schema_version`, `kind`, `pack_id`, `style_fingerprint`, `licenses`, and `assets`.
   - Reject unknown licenses, duplicate ids, stale hashes, unsafe paths, invalid pivots, cyclic references, dimension mismatch, or unsupported crop/transparency policies.

4. Validate and render the contact proof.

```powershell
python scripts/validate_static_pack.py --pack <pack-root>/static-pack.json --root <pack-root>
```

Writes `qa/static-pack-report.json` and `qa/static-pack-contact.png` atomically. Installed skill directory: `python -m pip install -r requirements-runtime.txt` when needed.

5. Inspect the contact sheet.
   - Silhouette, consistent scale, pivot intent, alpha edges on checker/black/gray/white, cropping, role coverage, palette/style continuity, readability at target size.
   - Contact sheet proves pack comparison, not animation, runtime interaction, or provenance. Read the owner report and hash-bound provenance.

## Completion Contract

Done: validator exit 0; current source/license/provenance pins; `representative` true; portable paths; contact-sheet hash matches report; sheet inspected. Failed validation must preserve previous proof. Fixture reports may pass technical checks, not production completion.

## Resources

- `scripts/validate_static_pack.py`: validation and contact-proof CLI.
- `scripts/static_assets/`: schema and semantic validation.
- `references/schemas/static-asset-pack-v1.schema.json`: pack contract.
