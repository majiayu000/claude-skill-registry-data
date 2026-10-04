---
name: build-game-ui-kits
description: "Game UI kits: raster UI from imported art, Imagegen, or explicit Grok stills; neutral-background controls, icons, HUD parts, interaction states, density variants, nine-slice assets, provenance, state/stretch proof."
---

# Build Game UI Kits

Portable raster UI kit: explicit tokens, densities, component states, hashes, proof.

## Workflow

1. Freeze the UI contract.
   - Required components, base sizes, densities, interaction states, nine-slice regions, palette tokens, minimum contrast, shared style fingerprint.
   - This skill: raster UI families. Animated character art → `$spritesheet-expert`; cross-family delivery → `$produce-2d-assets`.

2. Generate or import component art.
   - `$imagegen` default for new user-facing bitmap art. Load `$grok-imagine` only when Grok stills are selected explicitly. Provider creates semantic pixels; deterministic code may cut out, resize, assemble states, stretch nine-slices, and render proof — not draw replacement production UI.
   - Isolated controls and icons on flat gray, black, or white. Never request new green, blue, cyan, or magenta chroma. Preserve neutral fills and outlines; use BiRefNet/BEN2 or another reviewed model-backed cutout when connected-matte removal is ambiguous.
   - Grok: review `--dry-run` first; `--ack-run` only with explicit current-task consent. Animated UI/VFX sequences → `$spritesheet-expert`.
   - Every density and state below one kit root. Portable relative paths.
   - Provenance on every state/density variant: Imagegen, Grok still, imported, or fixture. Fixture may validate state geometry; not representative production media.
   - Include every required state (default, hover, pressed, disabled, selected, focus, or checked) the component can enter. Do not rename an identical file as a state.
   - State loses identity, text/icon geometry, edge quality, or semantics: regenerate via provider from the accepted base state. Do not procedurally repaint the failed state and label it generated.

3. Write `ui-kit.json` against `references/schemas/ui-kit-v1.schema.json`.
   - Require `schema_version`, `kind`, `kit_id`, `style_fingerprint`, `densities`, `tokens`, and `components`.
   - Reject missing states/densities, hash drift, unsafe paths, invalid nine-slice geometry, inconsistent sizes, and insufficient declared contrast.

4. Validate and render proof.

```powershell
python scripts/validate_ui_kit.py --kit <kit-root>/ui-kit.json --root <kit-root>
```

Writes `qa/ui-kit-report.json`, `qa/ui-state-board.png`, and `qa/ui-nine-slice.png` atomically. Installed skill directory: `python -m pip install -r requirements-runtime.txt` when needed.

5. Inspect boards at intended scale.
   - State distinction, legibility, alignment, pixel snapping, focus visibility, density parity, nine-slice corners/edges.
   - State board proves state/density comparison. Stretch board proves nine-slice behavior. Inspect alpha edges against checker/black/gray/white when transparent.
   - Report is a gate, not a visual substitute.

## Completion Contract

Done: validator exit 0; source/provenance hashes; `representative` true; every required state and density present; portable paths; both boards inspected. Fixture reports may pass technical checks, not production completion. Failed validation must not replace prior valid proof.

## Resources

- `scripts/validate_ui_kit.py`: validation and proof CLI.
- `scripts/ui_kit/`: schema and semantic validation.
- `references/schemas/ui-kit-v1.schema.json`: kit contract.
