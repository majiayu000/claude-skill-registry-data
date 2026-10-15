---
name: configure-capabilities
description: Load the domain-taxonomy capability catalog, apply project-profile-driven inclusion rules, walk every cross-tree constraint explicitly, present optional capabilities to the user, produce scope.yaml with selected/rejected capabilities and the constraint_trace audit.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# configure-capabilities

> **Defect 23 — Decision Surfacing Discipline (DSD):** This skill emits a `decision-manifest.yaml` alongside its primary artifact. Every inferred decision produced during execution is recorded in the manifest with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Model-invocable skill for selecting capabilities from the KB catalog against a project profile. Called by the `product-keeper` agent during `specify` Stage 3.

## Purpose

Deterministic capability selection — given a project profile and a KB catalog, produce a scope.yaml that lists:
- `selected_capabilities` — capabilities that are in-scope, with per-capability rationale
- `rejected_capabilities` — capabilities that were excluded, with reason
- `constraint_trace` — every cross-tree constraint walked, whether it fired, and what it forced

Every decision is recorded. No silent exclusion, no silent inclusion.

## Input

Receive from product-keeper agent:
- `project_profile_path` (path, required) — frozen project profile YAML
- `project_brief_path` (path, required) — the user-provided brief; used by the within-domain coverage analysis pass (per `rules/product.md` Rule 10)
- `market_brief_path` (path, optional) — informs domain selection when market data suggests specific domains
- `mvp_recommendation_path` (path, required) — typically `.garura/product/scope/mvp-recommendation.md`. Per `rules/product.md` Rule 13 and C15, this file must exist and be non-empty before capability selection begins. The skill reads the primary use cases and deferred use cases from it and uses them to narrow the capability walk — non-primary capabilities land in `deferred_capabilities` of the output scope.yaml. Missing or empty file returns a structured failure with `what_failed: missing_mvp_recommendation`.
- `product_domain_library_path` (path, required) — typically `.garura/product/research/`. Per `rules/product.md` Rule 15 (Pull-to-Product, Defect 8), this is the ONLY read path for domain content during capability selection. Every selected domain must have a corresponding `{domain}.md` file here with a provenance header (either `origin: kb` for a KB copy, or `origin: stm_research` for freshly-authored research). Missing a domain here is a structured failure — the Stage 2 domain-selection step is responsible for populating this directory (either by copying from KB with provenance, or by dispatching research).
- `ltm_cross_tree_constraints_path` (path, required) — typically `core/components/memory/knowledge/domain/_cross-tree-constraints.yaml`. This is the ONLY file this skill reads from the KB directory. It holds cross-tree constraint rules that apply globally across domains. It is NOT a read path for domain content — domain content comes from `product_domain_library_path` only.
- `ltm_kb_extension_conventions_path` (path, required) — the parser guide at `core/components/memory/standards/rules/kb-extension.md`
- `ltm_domain_taxonomy_path` (path, optional, DEPRECATED for this skill's reads) — typically `core/components/memory/knowledge/domain/`. This path exists in the product pipeline but is only used by the Stage 2 domain-selection step to source KB content for copying into `product_domain_library_path`. configure-capabilities itself does NOT read from this path — it reads exclusively from `product_domain_library_path`. The input is accepted for back-compatibility but emits a warning if the upstream Stage 2 step did not populate the product research folder.
- `selected_domains` (list, required) — the domain names selected in Stage 2 (e.g., `["user-management", "experimentation", "metrics-and-scoring"]`)
- `optional_capability_selections` (list, optional) — user-approved optional capabilities from checkpoint
- `output_path` (string, required) — typically `.garura/product/scope/scope.yaml`
- `grounding_questions_path` (string, required) — typically `.garura/product/user-provided/grounding-questions.md`. Per rules/product.md Rule 12, this file is the cumulative question log: the skill READS it at start to pick up prior user answers, APPENDS new questions during Step 1e, and NEVER overwrites existing entries.
- `decision_manifest_path` (path, required) — path for the `decision-manifest.yaml` output, written alongside the primary artifact (e.g., `.garura/product/scope/decision-manifest-configure-capabilities.yaml`). Exact path is passed by the calling agent.

## Domain Library Reads (single read path per Rule 15 Pull-to-Product)

Per `rules/product.md` Rule 15 and C17, this skill reads the domain library from `product_domain_library_path` (typically `.garura/product/research/`) ONLY. It does NOT read from the KB directory directly. The KB is the authoring surface for canonical domain content; the product's research folder is the frozen snapshot that this product run consumes.

**Responsibility split:**
- **Stage 2 domain-selection step (upstream, NOT this skill):** for each selected domain, if the domain exists in the KB, copies the KB file into `product_domain_library_path` with a provenance header (`origin: kb`, `kb_source_path`, `copied_at`, `kb_sha_at_copy`, `editable: false`). If the domain does NOT exist in the KB, dispatches research to author `{product_domain_library_path}/{domain}.md` with `origin: stm_research`, `editable: true`, and the 9 required sections per `kb-extension-conventions.md`.
- **This skill (configure-capabilities):** reads every selected domain's file from `product_domain_library_path`. If a domain is missing, returns a structured failure with `what_failed: missing_domain_in_product_research` and the list of missing domains. The upstream Stage 2 step is responsible for ensuring the domain is present; this skill does NOT fall back to the KB read path.

Capabilities whose source markdown carries `origin: stm_research` in the provenance header are marked in the output `scope.yaml` with `source: provisional_stm_research` and are carried through the rest of the pipeline with that provenance. Downstream skills (`enrich-capabilities`, `generate-intent-epics`) treat provisional capabilities the same as kb-origin capabilities EXCEPT that the intent epics they generate carry `kb_source.provisional: true`. The `validate-intent-epics` validator allows this flag and does NOT treat provisional epics as dangling references.

Promotion from STM research back to the KB is a separate, user-approved concern handled by a future `/capture-learning` flow (not this skill). Until promotion, provisional capabilities remain scoped to the current product run.

## Process

### 0. MVP recommendation pre-flight (rules/product.md Rule 13, C15)

- Verify that `mvp_recommendation_path` (typically `.garura/product/scope/mvp-recommendation.md`) exists and is non-empty. If missing or empty, return structured failure with `what_failed: missing_mvp_recommendation`. The upstream Stage 2.75 step is responsible for authoring it; this skill does NOT author it and does NOT proceed without it.
- Parse the recommendation to extract: primary use cases (with persona, scoring source, rationale), deferred use cases (with defer reason, v1.1+ triggers), and any architecture directions committed at spec time. These become the narrowing filter for the capability walk in later steps.

### 1. Load and parse

- Read the project profile YAML into an ordered mapping.
- Read `_cross-tree-constraints.yaml` from `ltm_cross_tree_constraints_path` in full — it's small and always needed. This is the only file this skill reads from the KB directory.
- For each `selected_domain`:
  1. Look for `{product_domain_library_path}/{domain}.md`.
  2. If not found, add the domain to a `missing_domains` list. Do NOT fall back to reading from the KB directly — that is a Rule 15 (Pull-to-Product) violation.
- If `missing_domains` is non-empty, return structured failure with `what_failed: missing_domain_in_product_research` and the list. The calling play must re-run the Stage 2 domain-selection step to populate the product research folder (either by copying from KB or by dispatching research); this skill does not fabricate capabilities and does not perform the copy itself.
- For every domain file that WAS found, extract its provenance header (the `<!-- Provenance ... -->` block at the top), then extract every feature block (heading `### {PREFIX}-F\d+:`) and parse its `### Inclusion`, `### Cross-Tree Refs`, and metadata per `kb-extension-conventions.md`. Record the provenance `origin` (kb or stm_research) per feature for later provenance tagging — features whose file has `origin: stm_research` flow through the pipeline as `source: provisional_stm_research`.

### 1b. Within-domain coverage analysis (rules/product.md Rule 10)

For each domain that resolved (LTM or STM), check whether the existing feature catalog is deep enough for the product's implied scope. This is a second-order gap check — distinct from the "does the domain exist?" binary check in step 1.

For each selected domain:
1. Read `project_brief_path` and extract the implied needs that fall within this domain's scope. Example: for `user-management` on a product that stores third-party API keys, implied needs include *secrets vault*, *per-user quota*, *service-account identity*, *third-party credential linking*.
2. For each implied need, search the domain's feature list for a matching feature. A match is either a feature whose `name` and `When It Matters` section directly address the need, OR a feature whose business rules explicitly mention the need.
3. Classify the coverage per implied need:
   - `full` — a dedicated feature exists and addresses the need completely
   - `partial` — the need is mentioned as a sub-bullet of an existing feature but not as a first-class feature
   - `missing` — no feature in the current catalog addresses the need
4. For `partial` and `missing`, record a gap entry with:
   - `implied_need` — short description (e.g., "secrets vault with rotation, revocation, per-scope access, and audit log")
   - `source_quote` — sentence from the brief that implied the need
   - `closest_existing_feature` — feature ID if partial, or null if missing
   - `coverage` — `full | partial | missing`
   - `recommended_action` — `extend-existing-feature` / `add-new-feature` / `research-domain-extension`
5. Append the gap entries to a per-domain `within_domain_coverage_gaps` list. This list is emitted in scope.yaml (see Step 7) and surfaced at the capability-configuration checkpoint.

**Non-blocking:** this step does not halt the skill. It surfaces gaps for user review at the checkpoint. The user decides whether to accept the narrow scope, trigger research, or add features inline. The scope proceeds with whatever the user approves.

**Agent context:** this step needs an LLM judgment call (matching brief language against feature descriptions). The calling agent (`product-keeper`) runs the analysis in-context and feeds structured gap entries back into the skill output. No new sub-agent is required.

### 1c. Vertical-vs-component classification (rules/epics.md Rule 1)

For each resolved feature, classify it as `vertical` or `component`:

- **vertical** — the feature has a user-observable outcome. A reviewer can test it end-to-end. The feature will become its own intent epic.
- **component** — the feature is a subsystem of a user-observable flow. It does NOT become its own epic; it rolls up into a parent vertical's `in_scope` items at epic-generation time.

**Classification signals (all must be considered):**

| Signal | Implies |
|--------|---------|
| Feature name ends in `Agent`, `Pipeline`, `Interface`, `Store`, `Catalog`, `Schema`, `Vault`, `Ledger`, `Registry`, `Worker`, `Adapter`, `Handler` | likely `component` |
| Feature's `When It Matters` section describes what another subsystem does with the feature (e.g., "the improver reads the analyst output") | `component` |
| Feature has ≥2 incoming cross-tree refs from other domains AND no standalone user-facing UX described in its Depth Spectrum | `component` |
| Feature's Depth Spectrum's Standard tier describes backend behavior (API endpoints, queue workers, cron jobs, token issuers) with no user-facing surface | `component` |
| Feature's Depth Spectrum's Standard tier names a user action the reviewer can perform and observe | `vertical` |
| Feature has explicit admin persona references (admin-facing catalog, plugin management, etc.) | `vertical` (admin-facing) |

**Parent resolution:** every `component` feature must declare its `rolls_up_into: <parent_feature_id>`. The parent is the vertical feature whose user flow the component serves. Example: AO-F001 Analyst Agent rolls up into EX-F002 Experiment Configuration & Execution.

**Output to scope.yaml:**
```yaml
feature_classification:
  - id: UM-F001
    type: vertical
  - id: AO-F001
    type: component
    rolls_up_into: EX-F002
  - id: MS-F001
    type: vertical         # admin-facing catalog management
```

**Gate:** every `component` must have a valid `rolls_up_into` pointing at another selected_capability tagged `vertical` in the same scope. If the parent doesn't exist, halt with `what_failed: orphan_component` and halt scope generation until the user either adds the parent feature or reclassifies the component as vertical.

### 1d. Provenance tagging (rules/features.md Rule 8, rules/product.md Rule 11)

For each feature in `selected_capabilities`, attach a `provenance` block with:

- `source`: one of `brief_explicit` (brief directly names the capability), `brief_inferred` (brief implies via concrete language but doesn't name it), `rule_derived` (cross-tree constraint fired), `research_supplemental` (Rule 10 within-domain research), `profile_default` (profile field directly implied it), `assumption` (no source — pure guess).
- `source_quote`: verbatim brief text for `brief_*`, CTC id for `rule_derived`, profile field for `profile_default`, `'needs_user_grounding'` for `assumption`.
- `confidence`: `high` (brief_explicit, rule_derived, profile_default), `medium` (brief_inferred, research_supplemental), `low` (assumption).

**Enforcement per Rule 11:**

- Features with `source == assumption` MUST NOT appear in `selected_capabilities`. They move to a new top-level `inferences_pending_review` section in scope.yaml and MUST be surfaced at the capability-configuration checkpoint before the pipeline proceeds.
- Features with `source == kb_default` are ALSO surfaced at the checkpoint (the user confirms whether the KB default applies to THEIR product before it's written to scope).
- Features with `confidence == medium` are flagged in the checkpoint summary with "confirm or reject" prompts — they are NOT silent facts.

**Never allowed:** the skill writes scope.yaml with zero `assumption`-sourced capabilities. Every capability in `selected_capabilities` has been user-confirmed (directly or via the checkpoint protocol).

### 1e. Capture inferences to user-provided/grounding-questions.md (rules/product.md Rule 12)

Every inference produced in Steps 1b-1d (within-domain gaps, kb_default capabilities, assumption capabilities, kb_default constraints, unexplained numeric values) MUST be appended as a question entry to `.garura/product/user-provided/grounding-questions.md`. This file is cumulative and durable across pipeline runs — new runs APPEND, never overwrite.

Per inference, write one question entry:

```yaml
- id: Q-<topic>-<NNN>                     # stable, unique across runs
  asked_at: <ISO-8601>
  topic: scale | rate_limits | feature_count | cost_quota |
         scope_creep | time_windows | agent_budgets |
         experiment_config | oauth_providers | vocabulary |
         bounded_contexts | within_domain_gap
  question: "<plain-English question for the user>"
  pipeline_source: "configure-capabilities Step 1b | 1c | 1d"
  pipeline_guess: "<value the pipeline would use if user says 'go with your guess'>"
  impact_if_unknown: "<what lands in scope.yaml / which epic / which risk>"
  user_decision: null
  user_answer: null
  resolved_at: null
  resolved_by_run: null
```

**Read before write:** on every invocation, the skill first READS `grounding-questions.md` to see which questions already have user answers. For any question in the file whose `user_decision` is non-null and whose `user_answer` matches one of the current run's inferences, the skill uses the stored answer as a fact — it does NOT re-ask.

**Append, never overwrite:** new questions append to the file. Old questions (even stale ones from prior runs) stay visible so the user has full context. A periodic cleanup (via `/capture-learning` or a dedicated skill) may archive resolved questions to `user-provided/grounding-questions.archive.md`, but this skill never deletes.

**File creation:** if `grounding-questions.md` does not exist yet, create it with a top-level header and a Questions section. The frontmatter includes the product slug and a note: "questions are cumulative across pipeline runs — answer inline or in a separate checkpoint."

### 2. Auto-include mandatory features

For every feature in every selected domain:
- If `Inclusion` says `Default: **mandatory**` AND no `Exclude when` condition matches the profile → INCLUDE.
- If `Inclusion` has `Mandatory when` condition AND the condition matches the profile → INCLUDE.

Record each inclusion in `selected_capabilities` with `rationale: "mandatory by default"` or `rationale: "mandatory-when condition matched: {condition}"`.

### 3. Walk cross-tree constraints explicitly

For EVERY constraint in `_cross-tree-constraints.yaml` (not just those that fire):
- Evaluate the `condition` expression against the project profile and the currently-selected capability set.
- If the condition matches:
  - For each `implies_include` feature ID → add to `selected_capabilities` if not already present, with `rationale: "cross-tree constraint {id}: {description}"`.
  - For each `implies_exclude` feature ID → add to `rejected_capabilities` with `reason: "excluded by {id}: {description}"`.
  - For each `implies_include_depth` / `implies_exclude_depth` → record the depth cap in `depth_caps`.
  - Append to `constraint_trace.applied` with full detail (id, description, condition_evaluated, action_taken, rationale, source).
- If the condition does NOT match:
  - Append to `constraint_trace.not_applicable` with id, description, why_not_applicable (short human-readable reason), source.

The output has two sub-sections — see Step 7 for the exact shape. Per `rules/product.md` Rule 9 (audit vs scope separation), `applied` is scope-shaping content and `not_applicable` is audit content. The two must not be mixed in a single flat list.

Constraints that do NOT fire are still recorded (under `not_applicable`) — the walk is complete, the audit is complete.

### 4. Apply conditional features

For every feature with `Default: **conditional**`:
- Evaluate the `Mandatory when` condition against the profile.
- If matched → INCLUDE with rationale.
- Otherwise → leave for user decision in step 5.

### 5. Present optional features

Features with `Default: **optional**` that were NOT included by a cross-tree constraint are returned in a `pending_user_selection` list. The calling play presents these at the capability-configuration checkpoint.

If `optional_capability_selections` was passed in (user already selected them via a previous checkpoint cycle), add them to `selected_capabilities` with `rationale: "user-selected at checkpoint"`.

### 6. Apply depth caps from CTC-005 / CTC-010

If any cross-tree constraint fired `implies_exclude_depth`, record a global `depth_ceiling` for affected features. Downstream enrichment honors this ceiling when deriving business rules from the Depth Spectrum.

### 7. Write scope.yaml

```yaml
slug: <from project_profile.name>
status: DRAFT
created_at: <ISO-8601>
project_profile_path: <echoed>
selected_capabilities:
  - id: UM-F001
    domain: user-management
    name: "Login / Authentication"
    source: ltm          # ltm | provisional_stm_research
    rationale: "mandatory by default (Inclusion); cross-tree CTC-001 also implies MFA"
    depth_cap: null | advanced | enterprise
  - ...
rejected_capabilities:
  - id: UM-F007
    domain: user-management
    name: "Social Login (OAuth2)"
    reason: "excluded by CTC-009 (SSO-only auth excludes social login)"
  - ...
pending_user_selection:
  - id: UM-F006
    domain: user-management
    name: "User Profile (Extended / Preferences)"
    default: optional
    recommendation: "consider if UX maturity >= 3"
constraint_trace:
  applied:                                    # rules that fired — shaped the scope
    - id: CTC-001
      description: "High-security profiles require MFA"
      condition_evaluated: "security_level in ['high','critical']"
      action_taken: ["UM-F004"]
      rationale: "NIST 800-63B high-sensitivity baseline"
      source: ltm
    - ...
  not_applicable:                             # rules walked for audit, did not fire
    - id: CTC-002
      description: "Healthcare compliance (HIPAA) requires audit logging"
      why_not_applicable: "compliance=[] (need HIPAA entry)"
      source: ltm
    - id: CTC-003
      description: "Regulated industries require MFA"
      why_not_applicable: "industry='productivity_saas' (need BFSI/healthcare/gov)"
      source: ltm
    - ...
depth_caps:
  global: null | advanced | enterprise
  per_feature: {}
within_domain_coverage_gaps:             # per rules/product.md Rule 10 — surfaced at checkpoint
  user-management:
    - implied_need: "Secrets vault with rotation, revocation, per-scope access, audit log"
      source_quote: "users store API keys for external scoring services"
      closest_existing_feature: UM-F005
      coverage: partial
      recommended_action: extend-existing-feature
    - implied_need: "Per-user quota and cost ledger"
      source_quote: "solo-founder economics: $5-30 per overnight run"
      closest_existing_feature: null
      coverage: missing
      recommended_action: add-new-feature
    - ...
```

### 7b. Emit decision manifest

Before returning the output contract, write `decision-manifest.yaml` to `{decision_manifest_path}`.

Record every inferred decision produced during Steps 1b–1e. Each decision entry follows the schema below. Assign tier at runtime based on grounding source: **high** when the decision was a direct match against a KB rule, file, or catalog entry (including `kb_catalog_single_candidate`); **mid** when context was built via web research because no KB grounding existed; **low** when neither KB nor research yielded a grounding source.

**Decisions to record** (decision_id prefix: `D-cc-`):

| decision_id | decision_type | What is being decided |
|-------------|---------------|-----------------------|
| `D-cc-001` | `within-domain-gap-classification` | Coverage classification (`full`/`partial`/`missing`) for each implied need against domain features (Step 1b) |
| `D-cc-002` | `vertical-vs-component-classification` | Whether each resolved feature is `vertical` or `component` and its `rolls_up_into` assignment (Step 1c) |
| `D-cc-003` | `provenance-tagging` | Source classification for each feature (`brief_explicit`, `brief_inferred`, `rule_derived`, `research_supplemental`, `assumption`) (Step 1d) |
| `D-cc-004` | `grounding-question-generation` | Which within-domain gaps and assumption-sourced features warrant grounding questions, and what the question text is (Step 1e) |

Each decision entry in the manifest:

```yaml
schema_version: "1.0"
skill: "configure-capabilities"
generated_at: "{ISO8601}"
decisions:
  - decision_id: "D-cc-001"
    decision_type: "within-domain-gap-classification"
    tier: high | mid | low   # assign at runtime per grounding source
    grounding_source:
      kind: kb_path | web_citation | none
      ref: "{KB file path | URL | null}"
      excerpt: "{optional short quote when kind=kb_path}"
    recommendation: "{the agent's proposed classification per implied need}"
    alternatives_considered:
      - alt: "{alternative classification}"
        why_not: "{one-line dismissal reason}"
    agent_reasoning_summary: "{2-3 sentence explanation}"
    user_response: null        # filled in by orchestrator after surfacing flow
    user_response_detail: null
  # ... one entry per decision listed above
```

**NOTE:** This skill is the canonical exemplar for the 1-by-1 Q&A flow (configure-capabilities' existing grounding-question pattern). The manifest adds a durable audit record alongside the existing interaction flow — preserve all current user-question behavior in Steps 1b–1e; the manifest is additional, not a replacement.

### 8. Return the output contract

```yaml
scope:
  path: <written path>
  selected_count: <int>
  rejected_count: <int>
  pending_count: <int>
  constraints_walked: <int>    # should equal total constraints in the file
  constraints_fired: <int>     # equals len(constraint_trace.applied)
  constraints_not_applicable: <int>  # equals len(constraint_trace.not_applicable); constraints_fired + this = constraints_walked
  dangling_feature_refs: <int> # must be 0 — any >0 is a structured failure
decision_manifest:
  path: <written path>
  decisions_recorded: <int>   # count of decision entries in the manifest
```

## Constraints

- NEVER skip a cross-tree constraint. All constraints are walked, whether or not they fire. Missing from the trace is a compliance violation.
- NEVER invent feature IDs. Every ID in `selected_capabilities`, `rejected_capabilities`, and `pending_user_selection` must resolve to a real feature in a domain-taxonomy markdown file under `product_domain_library_path` (`.garura/product/research/`). Features whose source file carries `origin: stm_research` in its provenance header are tagged with `source: provisional_stm_research` in the scope output.
- NEVER read domain content from `core/components/memory/knowledge/domain/` directly. Per `rules/product.md` Rule 15 (Pull-to-Product, Defect 8), the Stage 2 upstream step is responsible for copying KB content into `product_domain_library_path` with a provenance header. This skill reads only from `product_domain_library_path`. Missing domain files there return a structured failure (`what_failed: missing_domain_in_product_research`), NOT a KB fallback read.
- NEVER proceed without `mvp_recommendation_path`. Per `rules/product.md` Rule 13 / C15, a missing or empty MVP recommendation is a pre-flight structural failure (`what_failed: missing_mvp_recommendation`). The recommendation narrows the capability walk; without it, the skill would produce a bloated scope.
- NEVER silently exclude a capability. Every exclusion has a `reason` recorded in `rejected_capabilities`.
- NEVER silently include a capability. Every inclusion has a `rationale`.
- NEVER write content to `output_path` containing any abstraction-layer deny-list token. Per `rules/product.md` Rule 14 / C16, scope.yaml and any scope-shaping artifact this skill produces must stay implementation-agnostic. The deny-list includes specific database engines (Postgres, MySQL, SQLite, DynamoDB, Redis, etc.), specific SDK/framework method names and parameters (query(), resume=, output_format, temperature=0, etc.), specific programming languages (Python class definitions, TypeScript interfaces as code), specific build tools (lint rules, CI steps), specific table schemas with column lists and types, specific wire protocols (REST endpoint paths, gRPC method signatures), specific cryptographic constructions (sha256(prev_hash || ...)), and specific model or version identifiers (claude-sonnet-4-6, gpt-4o, etc.). Allowed is domain-level language: "append-only ledger", "structured-output enforcement", "role-isolated execution", "write-once baseline", "pluggable measurement adapter", "controlled-determinism contract".
- NEVER write outside `{output_path}`. Scope.yaml is the only file this skill writes.
- ALWAYS evaluate cross-tree conditions against BOTH the project profile AND already-selected capabilities (for constraints that reference prior selections).
- ALWAYS record the full constraint trace — fired constraints under `constraint_trace.applied` and not-fired under `constraint_trace.not_applicable`. Per rules/product.md Rule 9, the two sub-sections are structurally separate; never mix them in a flat list.
- ALWAYS narrow the capability walk by the primary use cases parsed from `mvp_recommendation_path`. Capabilities that serve only deferred use cases land in a `deferred_capabilities` section of scope.yaml with defer_reason and v1_1_trigger fields, not in `selected_capabilities`. Per `rules/product.md` Rule 13.
- ALWAYS read the feature files selectively (grep for the feature heading and parse the block); do not bulk-load every domain file into memory.
- ALWAYS run the within-domain coverage analysis pass (Step 1b) per `rules/product.md` Rule 10. Gaps are non-blocking but must be surfaced in scope.yaml under `within_domain_coverage_gaps` so the user can review at the checkpoint.
- ALWAYS run vertical-vs-component classification (Step 1c) per `rules/epics.md` Rule 1. Every feature is tagged `vertical` or `component`; components carry `rolls_up_into`.
- ALWAYS attach a `provenance` block to every selected_capability (Step 1d) per `rules/features.md` Rule 8. Every capability has source + source_quote + confidence; never silently accept `assumption` sources in the scope body.
- NEVER write kb_default or assumption-sourced features / constraints as silent facts. Surface them at the capability-configuration checkpoint under `inferences_pending_review` and wait for user grounding per `rules/product.md` Rule 11.
- ALWAYS capture every inference as a question in `.garura/product/user-provided/grounding-questions.md` (Step 1e) per `rules/product.md` Rule 12. Append-only, cumulative across runs. Read the file at the start of every invocation to re-use prior user answers; never re-ask a question the user has already resolved.
- NEVER commit an inferred decision to the primary artifact (scope.yaml) without recording it in `decision-manifest.yaml` first.
- NEVER tag a decision `tier: high` unless the `grounding_source.kind` is `kb_path` AND the referenced KB file exists.
- ALWAYS include `alternatives_considered` (≥1 entry) for every decision, even high-confidence ones.

## Version

| Field | Value |
|-------|-------|
| Version | 0.2.0 |
| Category | product-planning |
| Created | 2026-04-14 |
| Related | `core/components/agents/product-keeper.md`, `core/components/memory/standards/rules/kb-extension.md`, `core/components/memory/knowledge/domain/_cross-tree-constraints.yaml` |
