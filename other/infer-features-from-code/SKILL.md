---
name: infer-features-from-code
description: Infer the 3-tier domain → capability → feature catalog (scope/features.yaml) from scan-index.json during /codify by enumerating per-capability modules, routes, and entry-point wiring, then assigning a 5-point status (planned | development | rollout | released | cleanup) from release tags, churn, test presence, and deprecation markers. Used exclusively by product-keeper after infer-enriched-capabilities-from-code.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-features-from-code

Called by `product-keeper` during `/codify`, after
`infer-enriched-capabilities-from-code`. Produces `scope/features.yaml` at
`{stm_base}/{issue}/evidence/codify/proposals/scope/features.yaml`.

## Purpose

Once domains and enriched capabilities are proposed, the spec trunk needs
the canonical 3-tier feature catalog — the same artifact `manage-features`
writes in `/specify` Stage 4b. In `/codify` the feature list and per-feature
status must be reverse-engineered from code. This skill reads
`scan-index.json`, walks every selected capability from the sibling
proposals, enumerates feature candidates from modules / routes / entry-point
wiring, assigns each feature a 5-point status via the heuristic below, and
records every status decision in a `status_inferences` manifest for
downstream surfacing.

Tier-2 inference. `learning_category: product`. `sub_category: null`.

## Input

Receive from `product-keeper` via JSON contract. All paths absolute.

| Field | Required | Description |
|-------|----------|-------------|
| `scan_index_path` | yes | `scan-index.json` produced by `scan.py`. |
| `stm_base` | yes | STM root (`stm.base-path` in `.garura/core/config.yaml`). |
| `issue` | yes | Issue number (STM namespace). |
| `output_path` | yes | `{stm_base}/{issue}/evidence/codify/proposals/scope/features.yaml`. |
| `decision_manifest_path` | yes | `{…}/scope/decision-manifest-infer-features.yaml`. |
| `status_inferences_path` | yes | `{…}/scope/status-inferences-infer-features.yaml`. |
| `resolution_trace_path` | yes | `{…}/scope/resolution-trace-infer-features.yaml`. |
| `related_proposal_paths` | yes | Block with `scope_path`, `enriched_capabilities_path`, `domain_selection_path`. |
| `ltm_context` | yes | `{product_base, core_base, query_domains, locked_artifacts}`. |

## Process

### 1. Validate inputs

- `scan_index_path` parses as JSON with keys `manifests`, `trees`,
  `entry_points`, `docs`, `config_files`, `frontend_detection`, `patterns`,
  `git`. Missing → `scan_index_missing`.
- Every file in `related_proposal_paths` exists and is valid YAML. Missing
  any → `missing_related_proposal`. Parent dirs for the four output paths
  exist or are creatable.

### 2. Resolution Protocol walk

Per `core/components/memory/standards/rules/resolution.md`, record every
probe in `resolution_trace_path`. R1 skipped (codify bootstrap; reason
`"codify-bootstrap"`). R2 probes `{product_base}/scope/features.yaml` — if
present, read **informationally only**; prior IDs, name shapes, and status
values land in the trace. The skill still emits a fresh proposal; it does
NOT short-circuit to `alignment_confirmed`. Conflicts between an existing
catalog and the inferred proposal are surfaced as `status_inferences`
entries at `tier=mid`. R3 / R4 skipped (feature taxonomy is project-specific).

### 3. Read related proposals

Pull selected domain + capability slugs from `scope.yaml` +
`domain-selection.yaml`. Pull per-capability notes (module hints, anchored
framework idioms) from `enriched-capabilities.yaml`. These feed Step 4.

### 4. Enumerate feature candidates per capability

For each selected capability, walk the scan index through these signal lanes:

1. **Top-level modules under `src/`.** Direct children of the source root
   from `trees`. When convention nests deeper (`src/{capability}/*`), descend
   one more level under the capability subfolder.
2. **Per-capability subfolders.** When the capability slug matches a
   directory name, scope enumeration to that subtree. Each direct subfolder
   is a feature candidate.
3. **Route / handler counts.** From `entry_points` and
   `patterns.framework_idioms`, count routes (Express / FastAPI / Gin /
   Spring / Rails) per module. Multiple distinct route groups → multiple
   features; a single route group → one feature.
4. **Entry-point wiring.** From `entry_points`, identify modules registered
   in application bootstrap (main, app, server, cmd). Unregistered folders
   land as scaffold-only candidates (feeds `planned` status in Step 5).
5. **`patterns.naming_suffix_counts`.** Suffix counts (`*Repository`,
   `*Service`, `*Controller`, `*Handler`) confirm the feature exists but do
   NOT on their own raise the status above `planned`.

Name each feature from the module name in title case, plus — when available —
the nearest matching README header (`docs.readme_preview`). Names are noun
phrases of 3–10 words per `manage-features` R2. ID regex `^[A-Z]{2,4}-F\d{3}$`;
PREFIX is the capability's canonical abbreviation from
`enriched-capabilities.yaml`. Number features within a capability from
`F001` in enumeration order.

### 5. Assign per-feature status — heuristic (first match wins)

1. **`cleanup`** — module present AND a deprecation marker is hit. Markers:
   literal `@deprecated` annotation in any module file, `DEPRECATED` in
   module README, or `deprecated: true` frontmatter. Evidence: the exact
   file path + ≤200-char excerpt.
2. **`released`** — module present AND a release tag in `git.tags_recent`
   references the module path OR a semver ≥ 1.0 tag exists for the repo
   AND test signal is present for the module
   (`patterns.test_framework_signals` intersects the module path) AND the
   module does NOT appear in `git.churn_top` (churn is below the hot-file
   threshold → "stable").
3. **`rollout`** — module present AND test signal present AND either no
   release tag yet OR all tags are pre-1.0 (built, not fully released).
4. **`development`** — module present AND either partial test coverage
   (tests exist for some files in the module but not all) OR the module
   appears in `git.churn_top` (active churn). Active work-in-flight signal.
5. **`planned`** — module referenced in README, config, or an entry-point
   import path BUT the directory is absent OR contains only scaffolding
   (empty `index.ts`, lone `types.ts`, naming-suffix stubs with zero
   route/handler wiring).
6. **Fallback → `planned`** — no rule resolves. Recorded at `tier=low`
   with `grounding_source=insufficient-signal`.

Confidence per status:
- `high` — ≥ 2 signal lanes agree (e.g., release tag + test + low churn).
- `medium` — 1 strong signal OR 2 weak signals.
- `low` — fallback or single weak signal.

### 6. Build the 3-tier tree

Nest features under their capability; nest capabilities under their domain.
Slugs come verbatim from `domain-selection.yaml.selected_domains[].id` and
`enriched-capabilities.yaml.capabilities[].id` — never relocate, never
invent.

Capability-level status rollup (per `manage-features` precedence): any
`released` → `released`; else any `rollout` → `rollout`; else any
`development` → `development`; else any `cleanup` → `cleanup`; else
`planned`. Domain-level status is freeform (pass through from enriched
record or leave blank) — C4 of `manage-features` forbids coercing it to
the 5-point enum.

Compute summary counters: `domains`, `capabilities`, `features_total`,
`features_planned`, `features_development`, `features_rollout`,
`features_released`, `features_cleanup`.

### 7. Write status-inferences manifest + primary artifact

Write order (manifests first so mid-write crashes leave an audit trail):
resolution trace → status inferences → decision manifest → primary artifact.
Every per-feature status lands in `status_inferences_path` with
`feature_id`, `assigned_status`, `heuristic_rule` (1–6 above), `signals`
(concrete evidence paths), `confidence`, `alternatives_considered`, `tier`.

## Output

### Primary artifact — `scope/features.yaml`

```yaml
meta:
  source_type: "inferred_from_code"
  evidence:
    - "scan-index.json#/trees"
    - "scan-index.json#/entry_points"
    - "scan-index.json#/patterns/framework_idioms"
    - "scan-index.json#/patterns/naming_suffix_counts"
    - "scan-index.json#/patterns/test_framework_signals"
    - "scan-index.json#/git/tags_recent"
    - "scan-index.json#/git/churn_top"
    - "scan-index.json#/docs/readme_preview"
  confidence: "high" | "medium" | "low"   # aggregate over features
  learning_category: "product"
  sub_category: null
  tier: 2
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
  - id: "<domain-slug>"
    status: "<freeform or blank>"
    capabilities:
      - id: "<capability-slug>"
        status: "planned | development | rollout | released | cleanup"
        features:
          - id: "<PREFIX-Fnnn>"
            name: "<noun phrase, 3–10 words>"
            status: "planned | development | rollout | released | cleanup"
            description: "<1–2 sentences from module README/docstring>"
            evidence_paths:
              - "<repo-relative module path>"
              - "scan-index.json#<pointer>"
            confidence: "high | medium | low"
```

### Decision manifest — `decision-manifest-infer-features.yaml`

Standard Garura shape (`schema_version`, `skill`, `generated_at`,
`decisions[]`). One entry per inferred status, per name massaged away from
the raw module identifier, and per capability-level rollup. Each carries
`decision_id`, `decision_type`, `tier`, `grounding_source`,
`recommendation`, `alternatives`, `chosen_reason`.

### Return contract

```yaml
status: success
artifact_path: "<output_path>"
decision_manifest_path: "<decision_manifest_path>"
status_inferences_path: "<status_inferences_path>"
resolution_trace_path: "<resolution_trace_path>"
features_count: <int>
capabilities_count: <int>
domains_count: <int>
overall_confidence: "high" | "medium" | "low"
```

## Failure Modes

- `missing_related_proposal` — scope.yaml / enriched-capabilities.yaml /
  domain-selection.yaml absent or unparseable.
- `scan_index_missing` — `scan_index_path` absent or not valid JSON.
- `ltm_resolution_failed` — R2 errored (existing features.yaml not valid
  YAML, or product_base resolves outside the repo sandbox).
- `insufficient_signal` — scan present but zero modules under any selected
  capability AND zero entry-point wiring AND zero README references. No
  candidate list is inferable; product-keeper falls back to human input.

## Boundaries

- Read-only against `scan_index_path`, `related_proposal_paths`, and (for
  R2) `{product_base}/scope/features.yaml`. Emits a proposal only — writing
  to `.garura/product/scope/features.yaml` is a downstream `/garura:enrich` action.
- Does NOT re-run `scan.py`, invent capabilities or domains outside the
  sibling proposals, or produce intent epics.
