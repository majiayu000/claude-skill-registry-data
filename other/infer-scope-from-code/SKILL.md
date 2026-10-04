---
name: infer-scope-from-code
description: Infer the v1 scope.yaml (selected / deferred / rejected capabilities plus depth caps, within-domain coverage gaps, and constraint trace) by scoring KB capabilities against scan-index.json signals during /codify. Bounds the selection to the domains already chosen in the domain-selection proposal and the profile posture from the project-profile proposal. Used exclusively by product-keeper in the /codify play.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-scope-from-code

Called by `product-keeper` during /codify after `infer-domain-selection-from-code` and `infer-project-profile-from-code` complete. Produces `scope/scope.yaml` at `{stm_base}/{issue}/evidence/codify/proposals/scope/scope.yaml`.

## Purpose

During /codify (brownfield bootstrap), the scope artifact that /specify normally produces via `configure-capabilities` (KB walk + user decisions on optional capabilities) must instead be reverse-engineered from the existing codebase. This skill consumes `scan-index.json` plus the two prior proposals (domain-selection, project-profile) and emits a scope proposal grounded entirely in scan-index signals. It never invents evidence, never selects a capability outside the already-chosen domains, and always surfaces low-evidence items rather than silently rejecting them.

The capability universe is bounded by the intersection of:

- `selected_domains` from the domain-selection proposal (narrows the KB walk)
- KB capability listings under `{kb_domain_dir}/{domain}.md` (enumerated as `## Features` blocks with IDs and Inclusion rules)

For every KB capability inside a selected domain, this skill scores scan-index evidence and classifies the capability as `selected` (high/medium evidence), `deferred` (low evidence, scaffolds only), or `rejected` (zero evidence). Capabilities whose KB Inclusion rule fires on profile posture but have no scan evidence go into `within_domain_coverage_gaps` — the code is silent on them, not absent.

## Input

Receive from product-keeper via JSON contract.

- `scan_index_path` (path, required) — `scan-index.json` produced by scan-codebase.
- `related_proposal_paths` (list, required) — must contain the absolute paths to the already-emitted `domain-selection.yaml` and `project-profile.yaml` proposals. Validation halts if either is missing.
- `kb_domain_dir` (path, required) — `core/components/memory/knowledge/domain/`. Drives the capability walk.
- `stm_base` (path, required) — STM root resolved from `.garura/core/config.yaml` `stm.base-path`.
- `issue` (str, required) — issue number driving /codify.
- `output_path` (path, required) — `{stm_base}/{issue}/evidence/codify/proposals/scope/scope.yaml`.
- `decision_manifest_path` (path, required) — `decision-manifest-infer-scope-from-code.yaml` alongside the artifact.
- `ltm_context` (block, required) — `{product_base, core_base, query_domains, locked_artifacts}`. Presence triggers the Resolution Protocol (R3-focused here).
- `resolution_trace_path` (path, required) — where `resolution-trace.yaml` is written.

## Process

1. **Validate inputs.** Confirm `scan_index_path` exists and parses as JSON. Confirm both related proposal paths exist and parse. Confirm `kb_domain_dir` exists and contains at least one `*.md` file. Create output parent directories if missing. Structured failures: `scan_index_missing`, `missing_related_proposal`, `kb_domain_dir_missing`.

2. **Read related proposals.** Load `selected_domains[]` from the domain-selection proposal and the `profile` block from the project-profile proposal. The scope walk is strictly bounded by `selected_domains` — capabilities outside those domains are never considered, even if scan signals suggest them (those belong to the domain-selection proposal, not here).

3. **Execute LTM Resolution Protocol (R3-focused)** per `core/components/memory/standards/rules/resolution.md`. R3 = consult KB capability listings per selected domain. For each domain in `selected_domains`, open `{kb_domain_dir}/{domain}.md` and enumerate every capability (feature ID, Inclusion rule, Signals block). R1/R2/R4 remain available but R3 is the primary ground-truth path here because the KB domain files already carry canonical capability listings. Write the trace to `resolution_trace_path`.

4. **Score each KB capability against scan-index signals.** For every capability enumerated in Step 3, inspect the following scan-index paths and record every path consulted (these become `meta.evidence`):

   | Signal (scan-index path) | Evidence rule |
   |--------------------------|---------------|
   | `patterns.framework_idioms[]` | Idiom match to the capability's KB "Signals" block (e.g. `auth-middleware` idiom → auth capability) → **high**. Indirect match (e.g. `orm` idiom → data-layer capability) → **medium**. |
   | `patterns.naming_suffix_counts` | `Repository`/`Service`/`Controller`/`Handler` suffix counts inside a top-level module matching the capability's conceptual name → **medium** when count >= 3, **low** when 1-2. |
   | `trees[].children` under `src/` or `app/` | Top-level module name matches capability slug or a synonym from the KB "Search patterns" line → **medium** (structural presence). No match → contributes nothing. |
   | `git.churn_top[]` | A module already matched by `trees` appears in churn_top → upgrade match to **high** (active capability, not dormant). Absent from churn → match stays where it was (do not downgrade). |
   | `manifests[].dependencies` | Specialized library declared (e.g. `stripe` → payments, `opensearch`/`elasticsearch` → search, `passport`/`next-auth` → auth, `socket.io` → realtime) → **high** for the unlocked capability. |
   | `entry_points[]` and `config_files.ci` | Dedicated entry point or CI job for a capability's surface (e.g. `worker`, `migrate`, `seed`) → **medium** operational-presence signal. |
   | `frontend_detection` | Presence of a frontend for UI-bearing capabilities (e.g. catalog, cart) — without it, those capabilities drop from **high** to **medium**. |
   | `docs.readme_preview` / `docs.adrs` | Capability keyword hits in README or ADRs → **medium** documentation-presence signal (never alone sufficient for **high**). |

   **Score resolution rule:** the highest matched evidence level for a capability wins. Multiple **medium** matches from independent signal families (e.g. manifest dep + naming suffix + churn) may compound to **high** if and only if at least two families fire.

5. **Classify every capability.**

   - `selected_capabilities` — evidence level **high** or **medium**. Carry the KB feature list forward; mark features as `inclusion_basis: inferred_from_code` with the matched signals as rationale.
   - `deferred_capabilities` — evidence level **low** (a single weak signal, or a scaffold marker such as an empty `auth/` directory with no middleware). Record `defer_reason: scaffold-only-no-active-usage`, `v1_1_trigger: when-capability-ships-active-code`.
   - `rejected_capabilities` — zero scan-index evidence and capability's KB Inclusion rule does not fire on profile posture. No speculation; if a capability has no signal and no mandatory profile condition, it is rejected with `reason: no-scan-signal-and-no-mandatory-profile-condition`.
   - `within_domain_coverage_gaps` — capabilities whose KB Inclusion rule DOES fire on the project-profile posture (e.g. "mandatory when `industry == developer-tools`") but where zero scan evidence exists. The code is silent on them; this is a gap, not a rejection. One entry per domain, listing the silent capabilities with `coverage: missing` and `recommended_action: user-review-at-codify-checkpoint`.

6. **Build `constraint_trace`.** Walk `{kb_domain_dir}/_cross-tree-constraints.yaml` if present. For each constraint, record `applied` or `not_applicable` with a `why` grounded in either a scan-index path or a profile field. Never silently skip a constraint.

7. **Build `depth_caps`.** Default `global: null` and `per_feature: {}`. If `patterns.framework_idioms` or `manifests` show evidence of Enterprise-depth patterns (multi-tenancy gateway, RBAC engine, feature-flag service), do NOT set a cap. If the profile's `delivery.ci_maturity == 'none'` and no test framework appears, set `global: "Standard"` with evidence citation.

8. **Assemble the artifact.** Write `meta` block first, then scope body. Meta lists every scan-index evidence path consulted across all scoring decisions (deduplicated). Meta `confidence` is the min of per-capability confidences; **low** whenever `scan_status: budget_exhausted` regardless of per-capability scores.

9. **Write decision manifest.** One entry per capability (selected, deferred, rejected) plus one per depth-cap decision plus one per within-domain gap. Each entry: `{capability_slug, tier, grounding_source, recommendation, alternatives_considered, confidence}`. `grounding_source` is either `scan-index:<json-path>` or `kb:{domain}.md#{feature-id}` or `profile:<field>`. Low-confidence entries MUST list alternatives_considered.

## Output

Primary artifact at `output_path`:

```yaml
meta:
  source_type: "inferred_from_code"
  evidence:
    - "scan-index.json#/patterns/framework_idioms"
    - "scan-index.json#/patterns/naming_suffix_counts"
    - "scan-index.json#/trees"
    - "scan-index.json#/git/churn_top"
    - "scan-index.json#/manifests/0/dependencies"
    - "scan-index.json#/frontend_detection"
    - "scan-index.json#/docs/readme_preview"
  confidence: "high" | "medium" | "low"
  learning_category: "product"
  sub_category: null
  tier: 2
  scan_status_warning: null        # or message when scan truncated
  related_proposal_paths:
    - "{path to domain-selection.yaml}"
    - "{path to project-profile.yaml}"
selected_capabilities:
  - capability_slug: "{slug}"
    domain: "{domain}"
    source: "inferred_from_code"
    evidence_level: "high" | "medium"
    matched_signals:
      - "scan-index:{json-path}"
    features:
      - id: "{KB feature id}"
        name: "{KB feature name}"
        inclusion_basis: "inferred_from_code"
        rationale: "{signal → inclusion sentence}"
        feature_classification: "vertical"
        depth_cap: null
rejected_capabilities:
  - capability_slug: "{slug}"
    domain: "{domain}"
    reason: "no-scan-signal-and-no-mandatory-profile-condition"
    source: "inferred_from_code"
deferred_capabilities:
  - capability_slug: "{slug}"
    domain: "{domain}"
    features: [ ... ]
    defer_reason: "scaffold-only-no-active-usage"
    v1_1_trigger: "when-capability-ships-active-code"
    target_release: "v1.1"
constraint_trace:
  applied: [ ... ]
  not_applicable:
    - id: "CTC-XXX"
      why_not_applicable: "..."
      source: "scan-index:{path}" | "profile:{field}"
depth_caps:
  global: null | "Standard"
  per_feature: {}
  note: "{evidence-cited justification if cap set}"
within_domain_coverage_gaps:
  {domain}:
    assessment: "{one-sentence summary}"
    gaps:
      - implied_need: "{capability name}"
        source_quote: "KB Inclusion rule that fires on profile"
        closest_existing_feature: "{KB feature id}"
        coverage: "missing"
        recommended_action: "user-review-at-codify-checkpoint"
feature_classification:
  - id: "{feature-id}"
    type: "vertical"
inferences_pending_review: [ ... ]
```

Decision manifest at `decision_manifest_path`:

```yaml
decisions:
  - capability_slug: "{slug}"
    tier: 2
    grounding_source: "scan-index:patterns.framework_idioms" | "kb:{domain}.md#{feature-id}" | "profile:{field}"
    recommendation: "selected | deferred | rejected"
    alternatives_considered: [ ... ]
    confidence: "high | medium | low"
  # one entry per capability decision, per depth-cap decision, per within-domain gap
```

Resolution trace at `resolution_trace_path` per resolution.md schema (R3 path dominant).

No product LTM writes. All output is under STM.

## Failure Modes

- `scan_index_missing` — `scan_index_path` does not exist or is not valid JSON.
- `missing_related_proposal` — domain-selection or project-profile proposal not present at the supplied path, or file exists but cannot be parsed / lacks required keys.
- `kb_domain_dir_missing` — `kb_domain_dir` does not exist or contains no domain markdown files.
- `ltm_resolution_failed` — Resolution Protocol raised an error; skill halts and returns the trace path for triage.
- `insufficient_signal` — no manifests, no trees, no framework idioms for ANY selected domain. Emit the artifact with empty `selected_capabilities` and every candidate in `within_domain_coverage_gaps`; mark meta.confidence `low`. Do NOT fabricate a selection.
- `scan_status_exhausted` — scan-index has `scan_status: budget_exhausted`; proceed but force meta.confidence to `low` and set `scan_status_warning`.
- `output_parent_missing` — `output_path` parent cannot be created; return structured failure.

## Boundaries

- Read-only against the codebase. The scan-index is the sole code-side input — this skill does NOT open source files directly.
- Capability universe is strictly `selected_domains` ∩ KB capabilities. Never select a capability outside the domain-selection proposal.
- Signals not listed in the Step 4 table MUST NOT be invented; if scan-index lacks a signal, the capability tends toward deferred or within-domain-gap, never a confident selection.
- No writes outside `{stm_base}/{issue}/evidence/codify/proposals/scope/` and the two companion files (decision manifest, resolution trace).
- This skill does NOT re-derive domains. If scan signals appear to suggest a domain not in the domain-selection proposal, that belongs to an amendment of domain-selection, not a scope override.
