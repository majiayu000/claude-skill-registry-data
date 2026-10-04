---
name: produce-2d-assets
description: "Multi-family 2D asset packs: coordinate and validate when one delivery spans two or more of sprites, static props, backgrounds, UI, and mockups; reconcile Imagegen/Grok/imported provenance, representative proof, style, variants, owners, release manifests."
---

# Produce 2D Assets

Coordinate asset families through owning skills, then validate one portable delivery pack. Single family: use its leaf skill.

## Route By Asset Family

- Animated characters, VFX rows, tilesets, textures, or atlases: `$spritesheet-expert`.
- Non-animated props, pickups, decals, and item icons: `$build-static-game-assets`.
- Layered, scrolling, or parallax scenes: `$build-game-backgrounds`.
- Raster controls, HUD components, states, densities, and nine-slice assets: `$build-game-ui-kits`.
- Contact sheets, store art, review boards, and reconstructed gameplay presentations: `$compose-asset-mockups`.

Delegate only when parallel ownership adds value, not because multiple skills exist. Small local work: execute directly. One owner per file; one coordinator for style and delivery.

## Workflow

1. Freeze the cross-family contract.
   - Pack id, owners, style bible, inventory, variant matrix, delivery targets, dependencies, acceptance proof.
   - One style fingerprint across families. State allowed differences; do not let families drift.
   - Semantic provider per generated family: `$imagegen` still default; `$grok-imagine` explicit; paid runs need reviewed dry-run plus current-task acknowledgement. Grok video-to-frames → `$spritesheet-expert`.

2. Produce each family through its owner.
   - Real source provenance, licenses, portable paths, current hashes, leaf skill deterministic report/proof.
   - `evidence.production_media` on every production leaf: `representative: true`, `provenance_verified: true`, explicit `source_types`. Imagegen/Grok/imported stay distinct. Fixtures, placeholders, deterministic drawings, legacy-unverified media cannot satisfy a production family.
   - Isolated sprites, props, UI: gray/black/white source backgrounds; reviewed model-backed removal when matte removal is ambiguous. Full-bleed backgrounds keep authored scene pixels.
   - Block a dependency until its upstream report passes. No placeholder deliverables to green the aggregate.
   - Provider fails identity, anatomy, semantics, repeat behavior, or edge quality: retry that route. Deterministic code may extract, align, compose, preview, validate — not replace failed semantic art.

3. Write `asset-pack.json` against the schemas under `references/schemas/`.
   - Require `schema_version`, `pack_id`, `owners`, `style_bible`, `inventory`, `variant_matrix`, and `delivery_manifest`.
   - Pin every deliverable and leaf validation report. Declare required variants and presentation status.

4. Validate the whole delivery.

```powershell
python scripts/validate_asset_pack.py --pack <pack-root>/asset-pack.json --pack-root <pack-root>
```

Writes `validation/asset-pack-validation-report.json`. Exit `0` pass, `1` contract failure, `2` real dependency still blocked, `3` operational failure. Installed skill directory: `python -m pip install -r requirements-runtime.txt` when needed.

5. Reconcile the real pack.
   - Inspect family proof together: scale, palette, camera, density, naming, variants, ownership, licensing, presentation truth.
   - Right proof per claim: animation playback/onion/contact, background composite plus scroll, UI state plus stretch boards, static contact/alpha, truth-labelled mockups. One contact sheet cannot certify all families.
   - Re-run aggregate validator after leaf changes; stale leaf reports must fail.

## Completion Contract

Done when every required leaf report is current and passing, every required variant and deliverable exists with matching hashes, presentation is passed or deliberately absent, paths are portable, and aggregate report exits zero.

## Resources

- `scripts/validate_asset_pack.py`: public aggregate validation CLI.
- `scripts/assetpack/`: schema, path, dependency, and delivery validation implementation.
- `references/schemas/`: style bible, inventory, variants, delivery manifest, and aggregate pack contracts.
