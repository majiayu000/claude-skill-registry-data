---
name: infer-epics-from-code
description: Derive epic boundaries for a brownfield codebase by clustering capabilities from features.yaml, enriched-capabilities.yaml, scope.yaml, and domain-selection.yaml using co-change, KB domain grouping, version tags, and ADR titles. Produces one minimal intent-epic stub per derived epic. Used exclusively by product-keeper during /codify.
version: 0.1.0
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# infer-epics-from-code

> **TENET (non-negotiable): Epics are written for humans to read.** Even
> minimal codify-mode stubs must be readable by a non-technical reviewer at
> the /garura:enrich gate. `intent.goal`, every `intent.constraints` entry,
> every `intent.failure_scenario` entry, and every `provenance.business_rules`
> entry stays plain-language. See `rules/epics.md` Tenet section.

Called by `product-keeper` during the `/codify` play, after `infer-features-from-code`.
Produces one `scope/epics/{epic-id}.yaml` file per derived epic at
`{stm_base}/{issue}/evidence/codify/proposals/scope/epics/{epic-id}.yaml`,
plus a single decision manifest covering every epic-boundary decision.

## Purpose

`/codify` bootstraps the product LTM for a brownfield repo. Once features and
capabilities are inferred, the product trunk needs **epic boundaries** — the
user-intent bundles that group related capabilities into shippable milestones.
This skill clusters capabilities into epics using four code-resident signals:
git co-change (coupled files indicate coupled capabilities), KB domain
taxonomy (capabilities under the same domain commonly form one epic),
version tags (version-labeled milestones mark historical epic boundaries),
and ADR titles (ADRs typically correspond to epic-scope decisions).

Epics authored from code are **MINIMAL intent-epic stubs** shaped per the
four-section ICE schema (identity at the top; then `intent`, `expectations`,
`connections`, `provenance`). Fields like `expectations.success_scenario`,
`expectations.recovery`, and detailed `intent.failure_scenario` text are NOT
inferable from code alone — asserting them would be fabrication, not
inference. This skill leaves the expectations stub empty and marks
`intent.failure_scenario` entries with an explicit "knowledge_gap" prefix so
/garura:enrich can route them to stakeholders. Nothing is filled in
speculatively; a gap is recorded as a gap.

Tier-2 inference with `learning_category: product` and `sub_category: null`.

## Input

Receive from the /codify play orchestrator via JSON contract. All paths absolute.

| Field | Required | Description |
|-------|----------|-------------|
| `scan_index_path` | yes | Path to `scan-index.json` produced by `scan.py`. |
| `stm_base` | yes | STM root, resolved from `stm.base-path` in `.garura/core/config.yaml`. |
| `issue` | yes | Issue number (STM namespace). |
| `output_dir` | yes | `{stm_base}/{issue}/evidence/codify/proposals/scope/epics/`. This skill writes MULTIPLE files (one per epic), so `output_dir` is used instead of `output_path`. |
| `decision_manifest_path` | yes | `{stm_base}/{issue}/evidence/codify/proposals/scope/decision-manifest-infer-epics.yaml`. Single manifest for the whole invocation. |
| `resolution_trace_path` | yes | `{stm_base}/{issue}/evidence/codify/proposals/scope/resolution-trace-infer-epics.yaml`. |
| `ltm_context` | yes | Resolution Protocol context block from product-keeper (contains `product_base`, `kb_base`, already-resolved LTM paths). |
| `related_proposal_paths` | yes | Map with absolute paths to upstream proposals: `features_yaml`, `enriched_capabilities_yaml`, `scope_yaml`, `domain_selection_yaml`. |
| `kb_domain_dir` | yes | `core/components/memory/knowledge/domain/` — canonical domain catalog used for KB-based clustering. |

## Process

### 1. Validate inputs

- Confirm `scan_index_path` exists and is valid JSON. Missing → `scan_index_missing`.
- Confirm every path in `related_proposal_paths` exists and is valid YAML.
  Any missing → `missing_related_proposal` with `offending_path` set.
- Confirm `output_dir` exists or is creatable. Failure → `output_dir_unwritable`.

### 2. Resolution Protocol walk (write resolution-trace first)

Per `core/components/memory/standards/rules/resolution.md`. Record every probe.

- **R1 — STM.** Skipped for /codify. Record skip reason `"codify-bootstrap"`.
- **R2 — Product LTM.** Probe `{product_base}/scope/epics/`. If present and
  LOCKED, emit proposals only for epics not already covered; overlaps surface
  as `alignment_confirmed` entries. Else proceed.
- **R3 — KB.** Read `{kb_domain_dir}/*.md` to harvest canonical domain slugs
  and feature IDs — the clustering vocabulary for Step 3b.
- **R4 — Web.** Not invoked; inference is closed-universe.

### 3. Cluster capabilities into epic candidates

Read `enriched-capabilities.yaml` to get the full capability list. Apply two
clustering heuristics in order; each capability may appear in at most one
emitted epic.

**3a. Co-change clustering.** From `scan_index.git.co_change_top`, map each
file to the capability it implements (via `features.yaml` evidence paths;
else via the capability's evidence path). Capabilities whose files co-change
across ≥ 2 pairs merge into one epic candidate. Record the pairs as `evidence`.

**3b. KB domain grouping.** For capabilities not yet clustered, group by
the domain slug from `enriched-capabilities.yaml` (or derived via
`domain-selection.yaml`). Same-domain capabilities form one epic candidate
unless 3a already split them.

**3c. Version-tag and ADR reinforcement.** Read `scan_index.git.tags_recent`
and `scan_index.docs.adrs`. Tags with semantic prefixes (e.g., `v2.0-payments`)
and ADR titles containing capability or domain names reinforce existing
candidates as additional `evidence`. Neither signal creates new epics alone.

**3d. Size check.** Target 1–10 epics per codebase. If the pipeline produced
> 20 candidates, halt with `too_many_epics`. If < 1 (no capabilities at all),
halt with `insufficient_signal`.

### 4. Populate minimal intent-epic stubs (four-section ICE schema)

For each surviving candidate, emit one YAML file to
`{output_dir}/{epic-id}.yaml`. Epic id format:
`epic-{domain-slug}-{short-name}-001` (mirrors the convention in
`.garura/product/scope/epics/`).

Brownfield proposals carry a top-level `meta:` block (proposal metadata) plus
identity and the four sections from the canonical schema at the SAME indent
level as `meta:` (no `epic:` wrapper). Populate ONLY these fields:

- `meta`: source_type, evidence paths, confidence, learning_category,
  sub_category, tier (see the per-epic artifact section below).
- Identity: `id`, `domain`, `capability` (the latter pulled from
  features.yaml; one capability per stub — minimal stub does not aggregate).
- `intent.goal`: one plain-language sentence synthesized from the clustered
  capability's name and description. Subject is a persona or canonical role
  (`user`, `admin`, `developer`, `operator`). Code-inferred goal is
  necessarily approximate — confidence will reflect that.
- `intent.constraints`: list of plain-language strings, strictly evidenced.
  Include a quantified entry only if a rate-limit, timeout, or SLO value
  exists in `scan_index.config_files`. Else emit an empty list `[]`.
- `intent.failure_scenario`: minimum 2 entries. When code evidence does not
  yield distinct failure modes, emit exactly two `"knowledge_gap: ..."`
  placeholder strings naming the gap, so the entry count satisfies Rule 4
  while flagging the gap for /garura:enrich.
- `expectations`: empty stub — `vetted.status: pending`, `success_scenario: []`,
  `recovery: []`. NEVER populated from code; `draft-epic-expectation` fills it
  after /garura:enrich promotes the proposal.
- `connections.before_chain.intents[]`, `after.intents[]`, `peers.intents[]`:
  populated only with epic ids that emerged in the same /codify run (sibling
  proposals). When no relationships are evidenced by co-change, emit empty
  lists.
- `connections.dependency_check`: when `before_chain.intents[]` is non-empty,
  emit a string referencing /garura:enrich review (e.g., "Verified at
  /garura:enrich review against the locked product epics."). When
  `before_chain.intents[]` is empty, emit "None — no inferred dependencies."
- `provenance.source.kind: brief_inferred`, `provenance.source.quote`:
  short summary of the scan-index evidence (file paths, ADR title, tag name)
  that drove the boundary, `provenance.source.confidence`: high / medium / low
  per the scan signals.
- `provenance.appetite`: emit a conservative default ("4 weeks") tagged in
  the decision manifest as a low-confidence inference for /garura:enrich.
- `provenance.business_rules`: rules traceable to KB entries or code-evidenced
  invariants (e.g., enforcing middleware). When none are evidenced, emit a
  single placeholder string `"knowledge_gap: Business rules require
  stakeholder grounding at /garura:enrich."` so the minimum-1 rule is met.
- `provenance.kb_source.capability`: equal to the top-level `capability`.
- `provenance.kb_source.rules_applied`: empty list when no KB rules
  evidenced; else the KB rule IDs.
- `provenance.kb_source.experiential_warnings`: empty list unless code
  evidence (e.g., commit messages, ADRs) directly cites a known pitfall.
- `provenance.uses_mocks`: `false` by default. Set `true` only when scan
  evidence shows mocks (`__mocks__/`, `mocks/`, stub fixtures in tests
  exercising production paths).
- `provenance.demock_epic_ref`: required only when `uses_mocks: true`.
  When unknown, emit `"knowledge_gap"` and route via the decision manifest.
- `provenance.foundation_investment`: `false` by default. Recompute after
  the full batch — if an epic ends up with ≥ 2 incoming `before_chain`
  references across the proposal set, flip to `true`.
- Optional alongside `meta`: `evidence_paths` — scan-index pointers and
  file paths that drove the boundary.

Do NOT emit any banned legacy top-level keys: `intents` (plural list),
`failure_conditions`, `in_scope`, `anti_goals`, `must_not_break`,
`cross_cutting_justification`, `problem_statement`, `hypothesis`,
`assumptions_requiring_validation`, top-level `appetite`, top-level
`business_rules`, top-level `constraints`, top-level `depends_on`,
top-level `dependencies`, top-level `foundation_investment`, top-level
`uses_mocks`, top-level `demock_epic_ref`, top-level `kb_source`,
top-level `expectation` (singular). The new four sections absorb all of
these.

### 5. Write artifacts, decision manifest, resolution trace

Write the decision manifest before the per-epic files so a crash mid-write
still preserves the audit trail. Every boundary decision (cluster formed,
cluster split, candidate rejected for insufficient signal, proposal
overlapping locked LTM) gets one `decisions[]` entry.

## Output

### Per-epic artifact — `{output_dir}/{epic-id}.yaml`

```yaml
meta:
  source_type: "inferred_from_code"
  evidence:
    - "<scan-index JSON pointer or file path>"
  confidence: "high" | "medium" | "low"
  learning_category: "product"
  sub_category: null
  tier: 2

# Identity (above the four sections)
id: "<epic-id>"
domain: "<domain-slug>"
capability: "<feature-id from features.yaml>"

# Section 1 — intent
intent:
  goal: "<one plain-language sentence; persona subject; observable outcome>"
  constraints: []        # evidenced only; empty if no rate-limit/SLO config found
  failure_scenario:
    - "knowledge_gap: Failure modes for this capability are not inferable from code alone. Stakeholder input required at /garura:enrich."
    - "knowledge_gap: Second failure mode placeholder so Rule 4 (>= 2 entries) is satisfied; /garura:enrich must replace both."

# Section 2 — expectations (empty stub; populated by draft-epic-expectation after /garura:enrich)
expectations:
  vetted:
    status: pending
    approved_by: null
    approved_at: null
  success_scenario: []
  recovery: []

# Section 3 — connections
connections:
  before_chain:
    intents: []          # populated only when co-change evidence supports it
  after:
    intents: []
  peers:
    intents: []
  dependency_check: "None — no inferred dependencies."   # or a /garura:enrich verification string when before_chain has entries

# Section 4 — provenance (LAST section)
provenance:
  source:
    kind: "brief_inferred"
    quote: "<short summary of scan-index evidence that drove the boundary>"
    confidence: "high" | "medium" | "low"
  appetite: "4 weeks"     # conservative default; flagged low-confidence in decision manifest
  business_rules:
    - "knowledge_gap: Business rules require stakeholder grounding at /garura:enrich."
  kb_source:
    capability: "<same as top-level capability>"
    rules_applied: []
    experiential_warnings: []
  uses_mocks: false
  demock_epic_ref: null   # required string when uses_mocks: true
  foundation_investment: false   # recomputed after the full batch if incoming before_chain >= 2

evidence_paths:
  - "<path into scan index or repo>"
```

Comment header in every file:
`# Minimal intent-epic stub under the four-section ICE schema. intent.failure_scenario`
`# entries marked "knowledge_gap:" are placeholders, NOT real failure modes —`
`# /garura:enrich must surface them to stakeholders. expectations is an empty`
`# stub — draft-epic-expectation populates it after /garura:enrich.`

### Decision manifest — `decision-manifest-infer-epics.yaml`

Standard Garura shape (`schema_version`, `skill`, `generated_at`,
`decisions[]`). One entry per epic-boundary decision: cluster formed, split
resolved, candidate rejected, overlap with locked LTM, new-epic proposal.
Each decision carries `decision_id`, `decision_type`, `tier` (per Decision
Surfacing Discipline), `grounding_source`, `recommendation`, `alternatives`,
`chosen_reason`.

### Resolution trace — `resolution-trace-infer-epics.yaml`

R1..R3 probes with `source`, `path`, `outcome`, extracted payload. R4 omitted.

### Return contract (to orchestrator)

```yaml
status: success
output_dir: "<output_dir>"
epic_artifact_paths:
  - "<output_dir>/<epic-id>.yaml"
decision_manifest_path: "<decision_manifest_path>"
resolution_trace_path: "<resolution_trace_path>"
epic_count: <int>
overall_confidence: "high" | "medium" | "low"
```

## Failure Modes

```yaml
status: failure
what_failed: "<code>"
detail: "<specific error>"
evidence:
  offending_path: "<file path if applicable>"
  offending_field: "<field name if applicable>"
```

Codes:
- `missing_related_proposal` — one of `features_yaml`,
  `enriched_capabilities_yaml`, `scope_yaml`, `domain_selection_yaml` is
  absent or unreadable.
- `scan_index_missing` — `scan_index_path` absent or not valid JSON.
- `ltm_resolution_failed` — R2 probe errored (path escapes sandbox or
  existing epic YAML not parseable).
- `insufficient_signal` — zero capabilities to cluster, or scan index carries
  no co-change, no tags, and no ADRs.
- `too_many_epics` — > 20 candidates. Halt and report for parameter tuning;
  no partial write.
- `output_dir_unwritable` — `output_dir` cannot be created.

## Boundaries

- Read-only against `scan_index_path`, upstream proposals, and `kb_domain_dir`.
- Writes MULTIPLE files under `output_dir` plus one decision manifest and one
  resolution trace. Never writes to `.garura/product/` in place.
- Emits minimal stubs — NEVER fabricates scenario fields. Those are explicit
  knowledge gaps routed to /garura:enrich for stakeholder input.
- Does NOT re-run `scan.py`; stale scan-index is the orchestrator's concern.
- Does NOT promote any epic to product LTM — that is /garura:enrich's job.
