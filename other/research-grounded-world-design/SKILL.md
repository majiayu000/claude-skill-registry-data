---
name: research-grounded-world-design
description: Internal world-design stage behind the storyboard entry point. Builds reusable visual assets — scenes, characters, costumes, props, architecture, atmosphere, continuity — from a script, confirmed production config, fact-check package, or fictional world rules, with one traceable reference image per subject and view. Do not trigger this directly on a user request; the `storyboard` skill routes here. Read it when following that route, when a caller names this skill explicitly, or when the user asks specifically for 世界观设定、视觉圣经、角色三视图、世界资产库 as standalone deliverables.
---

# Research-Grounded World Design

## Core Contract

One reusable visual-world package before shot production. Every selected subject gets a stable ID, evidence class, written specification, prompt, reference binding, generated asset, and continuity key. One complete subject view per image, registered immediately with absolute paths.

Production depth controls coverage. Card completeness, source or world-rule binding, continuity keys, image inspection, and manifest traceability stay constant at every depth.

## Capabilities

Load `imagegen` before the first generation call, and `web-access` before researching real subjects. Without `imagegen`, produce cards and prompts and stop before §6. Without `web-access`, work from local material and mark gaps `待核实`.

## 0. Load The Confirmed Config

When called from the storyboard workflow, read `planning/production_config.json` and carry across: `evidence_mode`, `production_depth`, `world_design_scope`, `image_generation_scope`, `bible_sections`, `quality_floor`, script path, aspect ratio, visual style, reference roots.

| Depth | Entity coverage | View coverage |
|---|---|---|
| `compact` | core recurring entities | one identity-defining view, plus continuity-critical views |
| `standard` | all recurring entities | identity, scale, handling, and location-continuity views |
| `detailed` | all visible entities | plus action phases, material detail, and state changes |

Gate C-W: the world run records the same evidence mode, depth, scope, and quality floor as the storyboard config.

## 1. Resolve Evidence Mode

Read [evidence-modes.md](references/evidence-modes.md). Select `strict_evidence`, `hybrid_evidence`, or `fiction_consistency`, then classify each entity as `historical`, `contemporary_real`, `scientific`, `invented`, or `stylized`. A real entity inside an invented story activates `hybrid_evidence` for that entity set.

## 2. Start An Isolated World Run

```bash
python3 scripts/init_world_run.py \
  --project <project-dir> --slug <short-name> \
  --evidence-mode <mode> --production-depth <depth> \
  --world-design-scope <core_recurring|all_recurring|all_visible> \
  --bible-section world,characters,props \
  --production-config <storyboard-run>/planning/production_config.json
```

Declare only the bible sections this project contains; `style` and `continuity` are always created. Read [world-design-contract.md](references/world-design-contract.md) before writing cards or manifests.

## 3. Register Evidence Or World Rules

Real entities: read local sources, prior fact-check records, approved photographs, maps, and documents. Register direct sources in `research/source_register.csv`, save usable images to `research/reference_images/`, and bind each entity to source IDs, observable facts, rights notes, and local paths.

Invented worlds: define physics, technology, social structure, geography, material culture, scale, palette, and motifs in `research/world_consistency_brief.md` and `research/evidence_profile.json`.

Keep style references separate from factual evidence in every mode.

## 4. Build Design Cards

One card per reusable entity in `design/design_cards.json`, typed as `world`, `location`, `character`, `costume`, `prop`, `architecture`, `atmosphere`, `vehicle`, `creature`, `material`, `graphic`, or `typography`. Each carries a stable ID, evidence class, source bindings, visible specification, continuity keys, prompt, required views, generated asset IDs, approval status, depth, and selection reason.

## 5. Build The Visual Bible

Write positive visual specifications into the declared `bible/<section>.md` files. Define recurring relationships explicitly: character scale within locations, ownership and handling, family resemblance, screen direction, light direction, weather progression, state changes, palette hierarchy.

Gate W: every entity selected by `world_design_scope` has one approved card and at least one approved reference or generated image.

## 6. Generate Reference Assets

Generate each declared view as one complete image — one subject, one view per file:

```text
generated/<asset-type>/<design-id>__<view-slot>__v001.png
```

Append each result to `manifests/assets.json` with design ID, view slot, version, prompt, evidence IDs, generator, absolute path, created time, and approval status. Replacements increment the version; earlier versions move to `garbage_pile/asset_versions/`.

## 7. Validate And Deliver

```bash
python3 scripts/validate_world_manifest.py --run <world-run-dir>
```

Inspect each approved image against its card: real entities against bound evidence (silhouette, proportions, construction, material, scale, usage), invented entities against declared rules and continuity keys.

Export to `deliverables/`: `<title>_visual_bible.xlsx`, `<title>_design_cards.json`, `<title>_asset_index.csv`, `<title>_prompt_book.md`, `<title>_world_design_qa.md`.

## Storyboard Handoff

Hand back the absolute world-run path, `design/design_cards.json`, approved `bible/` files, the approved asset manifest, required design IDs, evidence mode and entity classes, and continuity keys. Storyboard shots reference these through `world_asset_ids`. Reuse the same design IDs across episodes; a changed specification creates a new asset version.

## Completion Report

Depth, scope, evidence mode, source count, selected entity count, card count by type, generated and approved counts, replacements, fidelity or consistency issues, quality-floor status, delivery paths.
