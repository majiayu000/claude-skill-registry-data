---
name: 08-industry-alignment
description: Active, source-bounded alignment of a Gold dimensional design to Databricks Industry Vibe Data Models (and other canonical industry reference models — TM Forum SID, ARTS, ACORD, HL7, BIAN). Use when the customer operates in a recognizable vertical (retail, banking, healthcare, telecom, insurance, hospitality) and wants the Gold layer to cover industry-standard entities and use industry terminology, when checking industry coverage/gaps, or when the customer has a Vibe-generated Silver business model to align to. Overlays the parsed source schema with industry entities in Phase 0, steers domain assignment, conformed dimensions, grain/measure completeness, and naming in Phase 2, and emits an INDUSTRY_CROSSWALK the advisory Validation 6 re-scores. Does NOT invent tables absent from the source.
license: Apache-2.0
clients: [ide_cli, genie_code]
bundle_resource: none
deploy_verb: bundle_deploy
deploy_note: "Design-phase advisory pattern; output (INDUSTRY_CROSSWALK.csv, INDUSTRY_ALIGNMENT.md) feeds Gold design artifacts deployed downstream via `bundle deploy --target dev`. No standalone resource. On Genie Code, write all artifacts under the cloned repo root (state_file_root), never a bare relative path (see skills/genie-code-environment §8)."
coverage: full
metadata:
  author: prashanth subrahmanyam
  version: "1.0.0"
  domain: gold
  role: worker
  pipeline_stage: 1
  pipeline_stage_name: gold-design
  called_by:
    - gold-layer-design
  standalone: true
  last_verified: "2026-08-30"
  volatility: medium  # external reference (40+ published models) evolves faster than self-referential design workers
  upstream_sources:
    - repo: databricks-industry-solutions/lakehouse-industry-data-models
      path: model-agent/docs/design-guide.md
      url: https://github.com/databricks-industry-solutions/lakehouse-industry-data-models
      note: "Vibe Data Modeling design philosophy: industry standards as inspiration, not rigid templates. Vibe produces a Silver-layer business model; this worker aligns a Gold dimensional model to it by semantic coverage, not structural equivalence."
---

# Industry Data Model Alignment (Active + Advisory)

## Overview

This worker gives the Gold design an **active voice** for aligning to a **Databricks Industry Vibe Data Model** (or any canonical industry reference), instead of only grading alignment after the fact. It works in **two touchpoints**:

1. **Active (Phases 0 & 2):** overlay the parsed source schema with industry entities, then steer domain assignment, conformed-dimension identification, grain/measure completeness, and Gold naming toward industry standards.
2. **Advisory (Phase 8):** the crosswalk this worker writes is re-scored by `07-design-validation` Validation 6 into `INDUSTRY_ALIGNMENT.md`.

**REQUIRED BACKGROUND:** Read `references/industry-data-model-alignment.md` for the Silver-vs-Gold nuance, the manifest schema, the crosswalk states, and the scoring rubric. This SKILL.md is the behavioral companion to that reference.

## The Non-Negotiable Guardrail: Extract, Don't Generate

This worker is a **lens over the source schema — never a source of new tables.** It upholds `databricks-expert-agent`'s "Extract, Don't Generate" principle: the industry model informs *how* you model what the source contains; it must never inject entities the source lacks.

| The worker MAY | The worker MUST NOT |
|----------------|---------------------|
| Map each *parsed source table* to an industry entity | Invent a Gold table for an industry entity with no source data |
| Flag industry-**core** source tables at risk of exclusion | Add columns not derivable from the source schema |
| Recommend industry-standard **names** for Gold objects (still built from source columns) | Rename to industry terms that misrepresent the source column's meaning |
| Recommend domain grouping, conformed dims, measures to *consider* | Silently auto-apply any recommendation |
| **Surface a coverage gap** for human `Waived`/`Planned` disposition | Fabricate the missing entity to close the gap |

A surfaced gap is resolved as `Waived`/`Planned` via `SOURCE_TABLE_MAPPING.csv` with a rationale — never by inventing a table. All recommendations are recorded in `DESIGN_DECISIONS.md` and confirmed, mirroring the orchestrator's "never silently correct a classification" rule.

## When to Use / When to Skip

- **Use** when Phase 1 captured `industry_reference_source: vibe_generated | published` and `context/industry_reference.yaml` exists (reduce a Vibe Silver model or a published vertical model to that manifest — see the reference doc, Mode A/B).
- **Skip** entirely when `industry_reference_source: none`. Record "industry alignment: N/A" in the intake report and `DESIGN_DECISIONS.md`. Skipping is never a failure — this worker is optional and vertical-specific.

## Phase 0: Coverage Overlay

Run immediately after `classify_tables()` in orchestrator Phase 0, before any modeling, so coverage gaps are visible up front.

Use `scripts/industry_overlay.py`:

- `build_industry_overlay(classified, reference_path)` — annotates each *source* table with its industry entity (`Covered` by name/alias, `Absorbed` when attributes live in another table, or `Gap`), prints the overlay, and returns the crosswalk seed + provisional coverage %.
- Fold the printed overlay into the Schema Intake Report. Every `core`/`extended` `Gap` must get an explicit decision in Phase 1/2.

The manifest schema and matching rules live in `references/industry-data-model-alignment.md`.

## Phase 2: Active Guidance Rules

Apply the industry reference as an active checklist during dimensional modeling. Each rule **recommends** and **records in `DESIGN_DECISIONS.md` Section 8** — it never auto-applies.

| # | Guidance | Uses reference for | Recorded as |
|---|----------|--------------------|-------------|
| 1 | **Canonical domain assignment** | Map source tables to the industry's domain names so Gold domains match industry language | Domain column in the table inventory |
| 2 | **Conformed-dimension identification** | Industry models expose shared dims (customer/product/date); promote matched entities referenced by 2+ facts | Bus-matrix note + `04-conformed-dimensions` decision |
| 3 | **Grain & measure completeness** | Compare the entity's `core_attributes`/expected measures against your fact design; flag standard measures the source *can* support | Grain/measure table + rationale |
| 4 | **Terminology steering** | When a source table maps to an entity but is named off-standard, recommend the industry name (only if it faithfully represents the source) | Naming decision + old→new mapping |
| 5 | **Gap surfacing (not filling)** | For each core/extended `Gap`, force a `Waived` (out of scope) or `Planned` (later phase) decision | `SOURCE_TABLE_MAPPING.csv` EXCLUDED/PLANNED row + rationale |
| 6 | **Sensitivity alignment** | Where the entity is `PII`, ensure the covering Gold table carries the `PII` tag | `table_properties.PII` on the YAML (Phase 4) |

At the end of Phase 2, after gaps are dispositioned, write the crosswalk with `write_crosswalk()`.

## The Crosswalk Artifact (hand-off contract)

`gold_layer_design/INDUSTRY_CROSSWALK.csv` — the single artifact Validation 6 consumes. Matching is owned **here**; scoring/gating is owned by `07-design-validation`.

| Column | Meaning |
|--------|---------|
| `entity` | Industry reference entity name |
| `domain` | Industry domain |
| `importance` | `core` \| `extended` \| `optional` |
| `sensitivity` | `PII` \| `none` |
| `state` | `Covered` \| `Absorbed` \| `Waived` \| `Planned` \| `Gap` |
| `gold_tables` | Pipe-delimited Gold table(s), or empty |
| `rationale` | Required for `Waived`/`Planned`/`Gap` |

## Hand-off to Validation 6

`07-design-validation` Validation 6 **loads** `INDUSTRY_CROSSWALK.csv` (it does not re-match): it verifies each `Covered`/`Absorbed` row's `gold_tables` still exist in the current YAML, re-checks `PII` sensitivity against `table_properties.PII`, scores coverage/terminology/PII per the rubric, emits `INDUSTRY_ALIGNMENT.md`, and stays **advisory** (excluded from `all_valid`). The `_norm`/`IMPORTANCE_WEIGHT` constants live in `scripts/industry_overlay.py`.

## Common Mistakes

| Mistake | Why it's wrong |
|---------|----------------|
| Inventing `dim_supplier` to hit 100% | Violates Extract-Don't-Generate; creates a table with no source data |
| Auto-renaming source tables to industry terms silently | Recommendations must be recorded and confirmed, not applied invisibly |
| Making coverage a hard gate | Reference is external, volatile, and a different layer; false failures result |
| Re-implementing matching in Validation 6 | Two matchers drift; the crosswalk is the single source of truth |
| Forcing normalized industry structure into Gold | Defeats the dimensional model's purpose |

## Inputs

- **From Phase 0:** classified source table inventory (`classify_tables()` output)
- **From Phase 1:** `industry_vertical`, `industry_reference_source`, `industry_reference_path`
- **From customer:** `context/industry_reference.yaml` (normalized manifest; template in `assets/templates/`)

## Outputs

- Printed industry coverage overlay (Phase 0)
- Industry Alignment section appended to `DESIGN_DECISIONS.md` (Phase 2)
- `gold_layer_design/INDUSTRY_CROSSWALK.csv` (Phase 2, consumed by Validation 6)
- Terminology/domain/conformed-dim recommendations feeding Phases 2–4

## Design Notes to Carry Forward

- [ ] Provisional coverage % from the Phase 0 overlay
- [ ] Every core/extended gap has a `Waived`/`Planned` disposition with rationale
- [ ] Conformed-dim promotions and terminology renames recorded in `DESIGN_DECISIONS.md` Section 8
- [ ] `INDUSTRY_CROSSWALK.csv` written and ready for Validation 6

## Next Step

Continue Phase 2 dimensional modeling with the industry-informed decisions, then proceed through Phases 3–7. At Phase 8, `07-design-validation` Validation 6 consumes the crosswalk and emits `INDUSTRY_ALIGNMENT.md`.

## Reference Files

- **[Industry Data Model Alignment](references/industry-data-model-alignment.md)** — manifest schema, Silver-vs-Gold nuance, crosswalk states, scoring rubric, report template
- **Overlay script:** `scripts/industry_overlay.py` — matching, overlay, crosswalk writer
- **Manifest template:** `assets/templates/industry_reference.template.yaml`

## Related Skills

- `design-workers/07-design-validation` — Validation 6 (consumes the crosswalk)
- `design-workers/04-conformed-dimensions` — conformed-dimension patterns (guidance rule 2)
- `common/naming-tagging-standards` — snake_case, tags (`layer`/`domain`/`PII`), dual-purpose descriptions

## References

- [Vibe Data Modeling (Databricks blog)](https://www.databricks.com/blog/reimagining-data-modeling-lakehouse-introducing-vibe-data-modeling)
- [lakehouse-industry-data-models](https://github.com/databricks-industry-solutions/lakehouse-industry-data-models)
- [AgentSkills.io Specification](https://agentskills.io/specification)
