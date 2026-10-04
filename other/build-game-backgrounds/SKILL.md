---
name: build-game-backgrounds
description: "Game backgrounds: layered raster packs from imported art, Imagegen, or explicit Grok stills; full-bleed parallax, scrolling panoramas, environment layers, horizon-safe composition, provenance, manifests, visual proof."
---

# Build Game Backgrounds

Portable layered-background pack: sources, camera contract, hashes, composite, and scrolling proof agree.

## Workflow

1. Define the scene contract before generating art.
   - Canvas size, aspect ratio, horizon, focal safe zone, layer order, depth, parallax factors, repeat behavior, style fingerprint.
   - This skill: background planes. Animated sprites/atlases → `$spritesheet-expert`; isolated props → `$build-static-game-assets`.

2. Generate or import the layers.
   - `$imagegen` default for new user-facing bitmap art. Load `$grok-imagine` only when Grok stills are selected explicitly. Provider creates semantic pixels; deterministic code may assemble, scroll, measure seams, and render proof — not paint replacement production scenery.
   - Full-bleed scene layers keep authored scene pixels; no forced neutral matte. Isolated transparent overlay: generate on flat gray, black, or white; model-backed removal when connected-matte removal threatens subject colors. Never request new green, blue, cyan, or magenta chroma.
   - Grok: review `--dry-run` first; `--ack-run` only with explicit current-task consent. Video animation → `$spritesheet-expert`; this skill accepts still layers.
   - Every source below one pack root. Portable relative paths; SHA-256 per layer.
   - Provenance per layer: Imagegen, Grok still, imported, or fixture. Fixtures may exercise composition and seam gates but are not representative art.
   - Keep sky, far, mid, near, foreground, overlay, and effects roles explicit. Do not bake gameplay-critical objects into a background without naming the tradeoff.
   - Composition, continuity, depth, or requested semantics fail: regenerate the affected provider layer. Edge harmonization may touch only a narrow provider-derived repeat band and must retain the original hash — not become procedural replacement art.

3. Write `background-pack.json` against `references/schemas/background-pack-v1.schema.json`.
   - Require `schema_version`, `kind`, `pack_id`, `style_fingerprint`, `canvas`, `camera`, and `layers`.
   - Reject duplicate order/depth ambiguity, hash drift, missing sources, unsafe paths, invalid safe zones, or incompatible dimensions.

4. Validate and generate deterministic proof.

```powershell
python scripts/validate_background_pack.py --pack <pack-root>/background-pack.json --root <pack-root>
```

Writes `qa/background-pack-report.json`, `qa/background-composite.png`, and `qa/background-scroll.gif` atomically. Installed skill directory: `python -m pip install -r requirements-runtime.txt` when preflight reports a missing module.

5. Inspect the actual composite and scrolling preview.
   - Seams, focal readability, horizon stability, parallax order, crop behavior, contrast behind gameplay, repeated-edge continuity.
   - Composite proves layer order and framing. Scrolling GIF proves declared offset/repeat behavior. Inspect both; one cannot substitute for the other.
   - Fix source or contract; rerun. Do not approve from JSON alone.

## Completion Contract

Done: validator exit 0; current input/provenance hashes; `representative` true; portable paths; report cites current proof hashes; both proof images inspected. Fixture reports may pass technical checks, not production completion. Keep prior proof if contract validation fails.

## Resources

- `scripts/validate_background_pack.py`: validation and proof CLI.
- `scripts/background_pack/`: schema and semantic validation.
- `references/schemas/background-pack-v1.schema.json`: pack contract.
