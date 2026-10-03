---
name: audit-asset-budget
description: "Use when scanning project asset directories to audit textures, meshes, and audio against target platform memory budgets and detect overages."
---

# audit-asset-budget

## 1. Overview

Scans project asset directories to audit textures, meshes, and audio against target platform memory budgets and detect overages. Produces `asset_budget.md` with memory footprint calculations, budget breach alerts, and actionable optimization recommendations.

## 2. When to Use

- **Scenarios**: Auditing asset memory usage against platform limits, identifying over-budget assets during art freezes, post-import asset validation.
- **Triggers**: `memory budget`, `asset audit`, `memory limit`, `texture budget`, `asset optimization`, `memory overage`, `platform limits`.

## 3. Core Pattern

1. **Asset Scanning & Metadata Extraction**: Scan directories to extract technical metadata:
   - **Textures**: Calculate footprint using *Width × Height × Channels × MipLevels × Compression Factor*.
   - **Meshes**: Calculate size via *Vertex Count (Pos + Norm + UV + Weight) + Index Count*.
   - **Audio**: Calculate uncompressed size via *Duration × SampleRate × Channels × BitDepth*.
2. **Budget Comparison**: Compare aggregated usage against target platform limits (e.g., Mobile, Switch, PS5/Xbox, PC).
3. **Breach Identification**: Flag assets causing category or total budget overages.
4. **Optimization Strategy**: Generate actionable recommendations (e.g., ASTC compression for textures, LOD reduction for meshes, bit-rate adjustment for audio).
5. **Reporting**: Export findings to `{TARGET_FOLDER}/docs/asset_budget.md`. Run during art freezes and after asset imports.

## 4. Interaction Protocol

### Error Handling & Intercepts

- **[Category Budget Breach]**: If a category is over budget: *"I've detected that the [Category] budget has been exceeded by [X%]. This poses a risk to [Platform] stability. Should we prioritize optimization for specific assets or adjust the total budget?"*
- **[Single Asset Outlier]**: If one asset consumes an extreme portion of its category: *"I notice [Asset Name] is consuming [X%] of the entire [Category] budget. This single asset might be an outlier—should we look into optimizing it specifically or re-evaluating its requirements?"*

## 5. Red Flags

- **Budget Adherence**: Keep all asset categories within allocated budgets.
- **Balanced Distribution**: No single asset consumes more than 20% of its category budget.
- **Compressed Audio Formats**: Use compressed formats instead of uncompressed WAV.
- **Complete Mipmap Chains**: Include mipmap chains for all textures.
- **Runtime Memory Measurement**: Measure decompressed/runtime memory footprint, not file size on disk.
