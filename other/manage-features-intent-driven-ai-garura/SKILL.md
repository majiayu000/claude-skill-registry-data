---
name: manage-features
description: Author the canonical 3-tier domain → capability → feature catalog (features.yaml) from enriched-capabilities.yaml using the 5-point status vocabulary (planned | development | rollout | released | cleanup). Use this skill whenever product-keeper needs to materialise features.yaml during specify Stage 4b — after enrich-capabilities and before generate-intent-epics — or when any product-configuration workflow references authoring, updating, or regenerating the product feature catalog at .garura/product/scope/features.yaml. Emits a decision-manifest for inferred statuses so the orchestrator can drive the tiered surfacing flow.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# manage-features

> **Decision Surfacing Discipline (DSD):** This skill emits a `decision-manifest.yaml` alongside its primary artifact. Every inferred status assignment or taxonomy inference is recorded with tier and grounding source. The orchestrator drives the tiered surfacing flow after this skill completes.

Model-invocable skill that produces the canonical feature catalog. Called by `product-keeper` during `specify` Stage 4b — between `enrich-capabilities` (Stage 4) and `generate-intent-epics` (Stage 5).

## Purpose

`generate-intent-epics` needs a stable feature catalog to cross-check epic KB IDs against declared product features. Before this skill existed, the Stage-4 enriched record went directly to Stage 5 and the feature catalog was either reconstructed ad-hoc or hand-authored post-run. This skill closes that gap by materialising `features.yaml` at a well-known path with a well-known schema.

## Input

Receive from `product-keeper`:
- `enriched_capabilities_path` (path, required) — `.garura/product/scope/garura:enriched-capabilities.yaml` from Stage 4.
- `project_profile_path` (path, required) — the frozen project profile YAML. Drives two decisions: (a) greenfield vs brownfield default-status logic, (b) reading any feature-status overrides the user declared.
- `stm_output_base` (path, required) — base path for writes. `features.yaml` is written to `{stm_output_base}/scope/features.yaml`; the decision manifest goes to `{stm_output_base}/scope/decision-manifest-manage-features.yaml`.
- `ltm_rules_feature_catalog_path` (path, required) — path to `core/components/memory/standards/rules/feature-catalog.md` (LTM). The skill loads this file first and enforces every rule in it against its output. When `ltm_context` is present in the calling contract, resolve via `ltm_context.core_base`; never hardcode source-repo paths.

## Output

Return to caller:
- `features_path` — absolute path to the written `features.yaml`.
- `features_count` — integer count of feature entries written across all domains and capabilities.
- `decision_manifest_path` — absolute path to the decision manifest.
- `decisions_recorded` — integer count of decision entries. Must be ≥ 1 when any status was inferred (F3 fires otherwise).

## Process

### 0. Load the feature-catalog rules

Read `ltm_rules_feature_catalog_path` (typically `core/components/memory/standards/rules/feature-catalog.md`). This file is the source of truth for how the catalog is authored — 3-tier hierarchy, ID regex, naming, 5-point status enum, required fields, summary counters, decision-manifest obligations. The narrative in this SKILL.md is a faithful summary; if the rules file and this SKILL.md ever drift, the rules file wins. Load it first so every downstream step applies its rules.

### 1. Load inputs

Read `enriched-capabilities.yaml`. Extract:
- Domain slugs from each enriched capability's KB provenance header (`domain` field).
- Capability slugs, their features, and each feature's `feature_id`, `name`, and supplemental fields the enrich step surfaced (notes, evidence references, gap items).

Read `project-profile.yaml`. Extract:
- `project_type` — `greenfield` or `brownfield`. Absent → treat as greenfield.
- Optional `feature_status_overrides` — a `feature_id → status` map for brownfield projects.

### 2. Build the 3-tier hierarchy

Group features by `domain → capability → feature`. Never flatten. The output shape:

```yaml
summary:
  domains: <int>
  capabilities: <int>
  features_total: <int>
  features_planned: <int>
  features_development: <int>
  features_rollout: <int>
  features_released: <int>
  features_cleanup: <int>

domains:
  - slug: <domain-slug>
    status: <freeform — NOT 5-point>
    rollup_notes: >
      <prose summary from enriched record, or blank>
    capabilities:
      - slug: <capability-slug>
        status: <5-point vocab>
        rollup_notes: >
          <prose>
        features:
          - id: <PREFIX-Fnnn>
            name: <noun phrase, 3–10 words>
            status: <5-point vocab>
            notes: >
              <prose>
            # optional:
            evidence: [<path or url>, ...]
            gap_items: [<string>, ...]
            target_milestone: <version string>
```

### 3. Assign per-feature status

Apply per feature in order:

1. If `project_profile.feature_status_overrides[feature_id]` exists and is a valid 5-point value → use it. Pass-through, no decision entry.
2. Else if `project_type == "brownfield"` → `planned` (inferred — record decision at tier=`mid`, grounding_source=`brownfield-default`).
3. Else (greenfield) → `planned` (inferred — record decision at tier=`high`, grounding_source=`greenfield-default`).

Rollup to capability- and domain-level:
- **Capability status.** Compute from its features using this precedence: if any feature is `released` → `released`; else if any is `rollout` → `rollout`; else if any is `development` → `development`; else if any is `cleanup` → `cleanup`; else `planned`.
- **Domain status.** Leave freeform. If the enriched record or project profile supplies a domain-level rollup string (e.g., `applied-and-evolving`), pass it through verbatim. Do not coerce to the 5-point enum — C4 forbids it.

### 4. Write `features.yaml`

Write to `{stm_output_base}/scope/features.yaml`. Include a header comment block with:
- Generation timestamp and play invocation context.
- Status vocabulary reference (the 5-point enum).
- A note that domain-level status is freeform and not validated.

Compute and populate the `summary` block counters from the per-feature status assignments.

### 5. Write the decision manifest

Write `{stm_output_base}/scope/decision-manifest-manage-features.yaml`. Each entry:

```yaml
decisions:
  - id: D-mf-<n>
    artifact_field: "domains[<i>].capabilities[<j>].features[<k>].status"
    feature_id: "<PREFIX-Fnnn>"
    decision: "<assigned status>"
    tier: "high" | "mid" | "low"
    grounding_source: "project_profile_override" | "greenfield-default" | "brownfield-default"
    recommendation: "<short rationale>"
    alternatives: [<other 5-point values considered>]
```

Record an entry only when a status was inferred — not when it was passed through from an override. F3 fires if any inference occurred and the manifest is empty.

### 6. Return the output contract

Emit `features_path`, `features_count`, `decision_manifest_path`, `decisions_recorded`.

## Authoring Rules

**R1 — Feature ID regex.** `^[A-Z]{2,4}-F\d{3}$`. PREFIX (2–4 uppercase letters) must match the domain-slug abbreviation from the KB provenance header (e.g., Agentic Methodology → `AM`, Engineering Observability → `EO`, AI Governance → `AG`, Work Intelligence → `WI`, Engineering Experience → `EE`). IDs not matching the regex are not written.

**R2 — Name format.** Feature name is a noun phrase of 3–10 words. Verb phrases, imperative phrases, and single nouns are invalid. Example: `Profile-Based Auto-Triage` (valid). `Triage users` (invalid).

**R3 — Required fields.** Every feature entry carries `id`, `name`, `status`, `notes`. Optional: `evidence`, `gap_items`, `target_milestone`. Missing or null on any required field is a structural violation.

**R4 — Domain mapping.** Nest each capability under its canonical domain per the KB provenance header. Do not arbitrarily relocate capabilities across domains.

**R5 — 3-tier shape.** `domains[].capabilities[].features[]` is mandatory. Features must not appear at the domain or top level; capabilities must not appear at the feature level. Flattening is a structural violation.

## Constraints

**C1 — No invented IDs.** Feature IDs are copied verbatim from the enriched record's `feature_id` field. Assigning an ID that does not appear in `enriched-capabilities.yaml` is a structural violation.

**C2 — Default-status rule.** Greenfield default is `planned`. Brownfield uses user-declared overrides where present; unresolved entries fall back to `planned`.

**C3 — Per-feature and per-capability status enum.** Values must belong to the 5-point enum: `planned | development | rollout | released | cleanup`. Any other value is rejected.

**C4 — Domain-level status is freeform.** Not validated against the 5-point enum. Strings like `applied-and-evolving` pass through unchanged. Coercing domain status into the 5-point vocab is a violation.

**C5 — Not user-invocable.** Model-invocable only, called by `product-keeper` during `/specify` Stage 4b. Direct user invocation is a protocol violation.

## Failure Conditions

**F1 — Missing artifact.** `features.yaml` is absent or empty after the skill completes. Unconditional failure.

**F2 — Bad status value.** Any feature or capability entry carries a status outside the 5-point enum. Domain-level status is exempt.

**F3 — Missing manifest when inference occurred.** The decision manifest is absent or empty when at least one status was inferred (i.e., not passed through from an override).

## Success Scenarios

**S1 — Greenfield.** Enriched record holds 23 capabilities / 85 features across 5 domains. Project profile has no pre-existing feature statuses. Every feature receives `planned`. Manifest records 85 entries at `tier=high`, `grounding_source=greenfield-default`. `features_count=85`, `decisions_recorded=85`.

**S2 — Brownfield.** Project profile declares overrides for 30 features (20 `released`, 10 `rollout`); the rest have no declared status. The 30 pass through verbatim (no manifest entries). The remaining features receive `planned` with manifest entries at `tier=mid`, `grounding_source=brownfield-default`. Both `features_path` and `decision_manifest_path` are present and non-empty.

## References

- Canonical example data: `.garura/product/scope/features.yaml` (the dogfooded Garura feature catalog — matches this schema).
- Intent source (source of truth): `core/components/skills/manage-features/reference/intent.yaml`. Change behaviour there, not in SKILL.md.
- Upstream producer: `enrich-capabilities` → `enriched-capabilities.yaml`.
- Downstream consumer: `generate-intent-epics` consumes `features.yaml` (required input) to cross-check epic KB IDs.
