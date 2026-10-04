---
name: compose-asset-mockups
description: "Asset mockups: non-destructive presentations of validated game assets; store art, review boards, gameplay reconstructions, pitch layouts; preserve source hashes, licenses, provenance, representative-media status, truth labels."
---

# Compose Asset Mockups

Derived presentations from validated assets. Do not mutate sources or present reconstruction as captured gameplay.

## Workflow

1. Accept only pinned inputs.
   - Each asset and font must reference artifact, upstream manifest, validation report, SHA-256, license, provenance.
   - Unvalidated sources return to the owning skill. Do not repair or regenerate them here.
   - Reject upstream reports with missing, stale, or non-representative production-media evidence. Fixture, placeholder, or reconstructed substitute cannot replace a rejected source.

2. Define the presentation contract.
   - Write `presentation.json` against `references/schemas/presentation.schema.json`.
   - Fix brief, approved copy, brand kit, inventory, gameplay scenes, compositions, licenses, provenance, output manifest.
   - Label every scene runtime-captured, reconstructed, or illustrative. Attach capture evidence only to runtime-captured truth.

3. Seal and resolve imported content.

```powershell
python scripts/prepare_presentation.py --presentation <root>/presentation.json --root <root>
```

Validates contract, writes canonical prepared/resolved JSON, verifies every pin, copies imported content into `presentation/content-addressed/`. `--validate-only` skips import copy. Installed skill directory: `python -m pip install -r requirements-runtime.txt` when needed.

4. Build only derived outputs.
   - Compose from the resolved store with the project's existing image, HTML/canvas, or design tooling.
   - Respect canvas, safe zone, layer order, asset list, licensed fonts, approved copy, and resampling rules.
   - Deterministic composition may arrange approved pixels — not invent missing character, prop, background, or UI art. Missing production media → `$imagegen`, explicit `$grok-imagine` still route, or owning asset skill.
   - Outputs under `presentation/outputs/`. Never overwrite source assets, manifests, reports, fonts, or licenses.

5. Capture and reconcile proof.
   - Inspect each output at delivery size: crop, readability, source fidelity, license/provenance coverage, truth label, hash.
   - Contact board proves layout only. Runtime-captured claims need hash-backed capture evidence; reconstructed and illustrative outputs keep truth labels visible in the contract.
   - Update presentation manifest and any runtime capture evidence. Revalidate before handoff to `$produce-2d-assets`.

## Completion Contract

Done: preparation exit 0; all imports hash-verified; every output belongs to a declared composition; licenses and provenance complete; truth labels honest; mockups inspected.

## Resources

- `scripts/prepare_presentation.py`: validation, sealing, and import CLI.
- `scripts/presentation_pipeline/`: contract and content-addressed preparation.
- `references/schemas/`: presentation, brief, composition, evidence, inventory, license, provenance, and manifest contracts.
