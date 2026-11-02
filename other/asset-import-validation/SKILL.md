---
name: asset-import-validation
description: Validate imported game assets for format, scale, naming, dependencies, metadata, and target-platform constraints before they enter the content pipeline.
---

# Asset Import Validation

## Goal

Catch asset problems at import time rather than after they become runtime rendering or packaging defects.

## Inputs to inspect

Source assets, importer settings, naming conventions, metadata, dependency references, and supported runtime formats.

## Workflow

1. Define per-asset-class requirements for format, dimensions, units/scale, orientation, naming, color space, compression, and required metadata.
2. Run importer validation on a representative asset corpus, capturing warnings/errors and the exact source/importer versions.
3. Check dependency references, missing textures/materials, duplicate identifiers, path/case consistency, and platform-specific import options.
4. Test imported assets in a representative runtime scene and a clean package build; compare file size, draw/resource cost, and visual fidelity.
5. Add repeatable validation hooks to asset ingestion and document exceptions for intentionally non-standard assets.

## Validation checklist

- [ ] Every supported asset type has explicit requirements and actionable failure messages.
- [ ] Missing references and case-sensitive path failures are caught before runtime.
- [ ] Source metadata and required provenance are preserved through import.
- [ ] Platform-specific formats/settings are validated on the intended targets.
- [ ] Exceptions are narrowly scoped and reviewable rather than global suppressions.

## Required output

Deliver an asset-class rules table, import validation report, representative runtime/package evidence, and CI/content-ingestion gate.

## Boundaries and failure handling

Do not auto-convert or overwrite source assets without preserving originals; do not treat importer success as proof the asset works in-game.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
