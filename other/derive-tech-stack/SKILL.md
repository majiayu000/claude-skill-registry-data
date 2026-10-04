---
name: derive-tech-stack
description: Stage 5 skill of /arch. Picks languages, runtimes, frameworks, libraries, tools, and design patterns per box (component, group of components in a layer, or product-wide). Patterns referenced MUST be industry-documented with literature citations — invented patterns are rejected. System-level decisions (monolith / microservice / serverless / modular monolith) are patterns and live here, not in a separate artifact. Every entry carries source_type, scope, and rationale citing a QP target, a project-profile pin, or a user answer.
version: 0.1.0
user-invocable: false
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# derive-tech-stack

> **Decision Surfacing Discipline:** This skill emits a `decision-manifest-derive-tech-stack.yaml` alongside its primary artifact. Every inferred decision — language pick, runtime, framework, library, tool, pattern — is recorded with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Called by `tech-architect` during `arch` Stage 5. Produces `tech-stack.yaml` at `{product_base}architecture/tech-stack.yaml` plus a decision manifest.

## Purpose

Pick the technology and patterns that govern how the product is built — languages, runtimes, frameworks, libraries, tools, AND patterns. Same stack across all boxes or different per box; this artifact is where the choice is recorded.

The **patterns rule** is load-bearing: every pattern named here MUST be industry-documented. Gang of Four, "Patterns of Enterprise Application Architecture" (Fowler), microservices.io, RFCs, OWASP, and a small set of canonical sources are honored directly. Patterns from other sources are accepted only when the KB at `core/components/memory/knowledge/arch/patterns/` carries a file naming the pattern with a literature citation. **Invented patterns are rejected.** A name like "garura pattern" or "this team's pattern" never enters the catalog.

System-level decisions — monolith vs. microservice vs. modular monolith vs. serverless — ARE patterns and live in this artifact, not in a separate one.

## Input

Receive from the `tech-architect` agent. All paths resolve against `{product_base}` and `{ltm_base}` supplied by the play via JSON contract.

- `logical_path` (path, required) — `{product_base}architecture/logical-architecture.yaml`. Stage 3 output. Source of component IDs and layers.
- `physical_path` (path, required) — `{product_base}architecture/physical-architecture.yaml`. Stage 4 output. Deployment targets and comms protocols shape language/framework picks.
- `inventory_dir` (path, required) — `{product_base}architecture/systems-inventory/`. System Tradeoffs sections may favor specific ecosystems (e.g., a Salesforce-grounded component favors Apex / LWC patterns).
- `refined_qp_path` (path, required) — `{product_base}architecture/quality-profile.yaml`. QP targets shape framework selection (performance, maintainability, security).
- `project_profile_path` (path, required) — `{product_base}user-provided/project-profile.yaml`. `grounded_tools.tech_stack[]` pins authoritative; `team_skills[]` and `incumbent_tech[]` provide grounding for tier resolution.
- `kb_stacks_dir` (path, required) — `{ltm_base}components/memory/knowledge/arch/stacks/`. Per-language stack files (frontend-react-nextjs, backend-nodejs, backend-go, etc.).
- `kb_patterns_dir` (path, required) — `{ltm_base}components/memory/knowledge/arch/patterns/`. Pattern catalog — extensibility surface for the citation allowlist.
- `kb_agentic_dir` (path, optional) — `{ltm_base}components/memory/knowledge/arch/agentic/`. For AI / agent / LLM patterns.
- `kb_tech_dir` (path, optional) — `{ltm_base}components/memory/knowledge/tech/`. Stack-specific deep knowledge when present.
- `output_path` (string, required) — `{product_base}architecture/tech-stack.yaml`.
- `decision_manifest_path` (string, required) — `{product_base}architecture/decision-manifest-derive-tech-stack.yaml`.
- `grounding_questions_path` (string, required) — `{product_base}user-provided/grounding-questions.md`. Append-only for multi-candidate halts.

## Output

### Tech stack

YAML at `{output_path}`.

```yaml
entries:
  - id: backend-runtime-process-layer        # kebab-case, unique within entries[]
    scope:
      kind: components | components_in_layer | components_with_system_ref | global
      targets:                                # interpretation depends on kind
        - { ref_kind: component, ref_id: order-orchestrator-fn }
        - { ref_kind: component, ref_id: inventory-api-svc }
        # OR for components_in_layer:
        # - { ref_kind: layer, ref_id: process }
        # OR for components_with_system_ref:
        # - { ref_kind: system_ref, ref_id: shopify-functions }
        # OR for global (kind = global, targets omitted or empty)
    category: language | runtime | framework | library | tool | pattern
    name: TypeScript                          # specific product or pattern name
    version: "5.3"                            # null when not applicable
    rationale: |
      {one paragraph — citing QP target, project-profile pin, or user answer}
    source_type: project_profile_pin | kb_catalog_single_candidate | kb_catalog_multi_candidate_user_approved | user_direct_answer | agent_default_with_user_approval
    source_citation: {pin slot | kb file path | grounding-question id | checkpoint id | kb pattern file}
    alternatives_considered:
      - option: Go 1.22
        why_rejected: |
          {one line}
    pattern_citation:                         # REQUIRED when category = pattern; null otherwise
      source: "Gang of Four — Design Patterns (1994)"
      reference: "Observer, p. 293"
      url: null                               # optional
```

**Schema rules:**
- Every entry has non-empty `id`, `scope.kind`, `category`, `name`, `rationale`, `source_type`.
- When `scope.kind != global`, `targets[]` is non-empty.
- When `category = pattern`, `pattern_citation.source` and `pattern_citation.reference` are non-empty AND the source passes the allowlist + KB extensibility check (see Step 5).
- Every component in `logical-architecture.yaml` is covered by at least one entry whose scope resolves to include it (see Step 6 — coverage validation).

### Decision manifest

One YAML file at `{decision_manifest_path}` with one entry per tech-stack entry written.

```yaml
manifest:
  skill: derive-tech-stack
  written_at: {ISO 8601 timestamp}
  decisions:
    - decision_id: TS-001
      decision_type: language_pick | runtime_pick | framework_pick | library_pick | tool_pick | pattern_pick
      entry_id: backend-runtime-process-layer
      tier: high | mid | low
      grounding_source:
        kind: project_profile_pin | kb_catalog_single_candidate | kb_catalog_multi_candidate_user_approved | kb_pattern_extension | upstream_artifact | user_direct_answer | agent_default_with_user_approval
        citation: {profile slot | kb file path | grounding-question id | checkpoint id | kb pattern file path}
      recommendation: {summarized pick}
      alternatives_considered:
        - option: ...
          why_rejected: ...
      agent_reasoning_summary: |
        {2-4 lines of prose}
      non_obvious: true | false
      user_response: accept | override | orbit | pending
      user_response_detail: {free text — null when pending}
```

## Process

### 1. Read inputs

- Parse `logical_path` → component IDs, layers, system_refs.
- Parse `physical_path` → per-component deployment_target and comms protocols.
- Glob `inventory_dir/*.md` → Tradeoffs sections per system_ref.
- Parse `refined_qp_path` → characteristics with relevance and targets.
- Parse `project_profile_path` → `grounded_tools.tech_stack[]`, `team_skills[]`, `incumbent_tech[]`.
- Glob `kb_stacks_dir/*.md` → per-language stack files with When-to-Choose / Avoid prose.
- Glob `kb_patterns_dir/*.md` → KB pattern catalog. Build a set of {pattern_name, pattern_citation.source, pattern_citation.reference} from each file's frontmatter or first heading block.
- Glob `kb_agentic_dir/*.md` if present.

### 2. Validate pre-conditions

- `logical_path` and `physical_path` exist and parse cleanly.
- `refined_qp_path` exists.
- Required inputs exist OR documented stand-in exists.

### 3. Walk slot inventory

Build the list of slots to fill, ordered:

1. **System-level pattern** — one entry per architecture pattern in play for the product (monolith / modular monolith / microservice / serverless). May be multiple when different layers run different system-level patterns (e.g., monolithic backend + serverless edge).
2. **Per-layer language and runtime** — one entry per (layer × deployment_target kind) where the layer has deployable components. SaaS-grounded components have no language/runtime entry (the vendor owns the stack).
3. **Per-layer framework** — one or more per layer (web framework, API framework, ORM, template engine, etc.).
4. **Cross-cutting libraries** — HTTP client, logger, telemetry, validation, retry, observability.
5. **Tools** — build, lint, format, package manager, CI, IaC, container orchestration tooling.
6. **Layer-level patterns** — MVC, MVVM, hexagonal, layered, onion, clean architecture per layer where applicable.
7. **Component-level patterns** — repository, CQRS, event-sourcing, anti-corruption layer, etc.
8. **Cross-cutting patterns** — circuit breaker, retry-with-backoff, idempotency key, outbox, saga, bulkhead, dead-letter-queue, etc. Required when the refined QP names resilience, idempotency, or consistency.

For each slot, resolve via Steps 4 and 5.

### 4. Resolve language / runtime / framework / library / tool entries

For each slot:

1. **Pin check.** If `project_profile.grounded_tools.tech_stack[]` carries an entry for the slot (matched by category + scope), use the pinned value. `source_type: project_profile_pin`, tier `high`.
2. **KB candidate query.** Walk `kb_stacks_dir` (or `kb_agentic_dir` for agentic slots) for files matching the slot's category and constraint set (deployment_target, language, layer role). Collect candidates.
3. **Resolve:**
   - Single candidate → use, `source_type: kb_catalog_single_candidate`, tier `high`.
   - Multiple candidates → halt per C20: append `Q-arch-NNN` to grounding-questions OR defer to Stage 5 checkpoint. `source_type: kb_catalog_multi_candidate_user_approved`, tier `mid`, `user_response: pending`.
   - Zero candidates → agent default mode: propose with alternatives. `source_type: agent_default_with_user_approval`, tier `low`. Surface one-by-one at the checkpoint.

Record one decision-manifest entry per slot.

### 5. Resolve pattern entries (with industry-citation gate)

Pattern slots have an additional gate beyond Step 4 resolution:

1. **Pattern-name proposal.** Agent identifies the pattern needed (e.g., "circuit breaker" for resilience NFR).
2. **Allowlist check.** Match the pattern name against the canonical-source allowlist below. If matched, record `pattern_citation` from the allowlist entry.
3. **KB extension check.** If not on the allowlist, query `kb_patterns_dir` for a file claiming the pattern with citation. If found, copy the file's `pattern_citation` into the entry. `grounding_source.kind: kb_pattern_extension`.
4. **Rejection.** If neither matches, REJECT the pattern. The skill MAY propose an alternative pattern that IS documented (e.g., "circuit breaker" instead of an invented "fail-safe-wrapper"). If no documented alternative exists, halt with `what_failed: undocumented_pattern` and surface the gap.

**Canonical allowlist** (hard-coded; extensible via KB only):

| Source | Coverage |
|--------|----------|
| Gang of Four — "Design Patterns" (1994) | Classical OO design patterns (Observer, Factory, Strategy, Decorator, etc.) |
| Fowler — "Patterns of Enterprise Application Architecture" (PoEAA, 2002) | Enterprise data, domain, presentation patterns (Repository, Unit of Work, Active Record, MVC, MVP, etc.) |
| Evans — "Domain-Driven Design" (2003) | Bounded context, aggregate, value object, anti-corruption layer, repository, etc. |
| Nygard — "Release It!" (2007 / 2018) | Circuit breaker, bulkhead, timeout, steady-state, fail fast |
| Hohpe & Woolf — "Enterprise Integration Patterns" (2003) | Messaging, channel, router, transformer, endpoint patterns |
| Newman — "Building Microservices" (2015 / 2021) | Service decomposition, API gateway, saga, choreography vs orchestration |
| Kleppmann — "Designing Data-Intensive Applications" (2017) | CQRS, event sourcing, log-structured systems, idempotent receiver |
| Davis — "Cloud Native Patterns" (2019) | Sidecar, ambassador, adapter, bulkhead, scale cube |
| microservices.io (Richardson) | Service registry, API composition, database-per-service, saga, outbox |
| IETF RFCs | Wire/protocol patterns (idempotency-key RFC drafts, OAuth, OIDC, etc.) |
| OWASP — ASVS / Top 10 / Cheat Sheets | Security patterns and controls |
| NIST SPs (e.g. SP 800-63, SP 800-207) | Identity, zero trust, cryptographic constructions |
| W3C standards | Web platform patterns |
| ISO/IEC standards | Quality / process patterns where pattern-naming applies |

A pattern NOT covered by the allowlist requires a KB pattern file at `{kb_patterns_dir}{pattern-id}.md` with a `pattern_citation` block in its frontmatter. Authoring KB extension files is a /enrich activity, not this skill's job — when KB lacks a needed pattern AND the allowlist doesn't cover it, this skill HALTS rather than fabricating.

Per-pattern decision manifest entry records `decision_type: pattern_pick` with `grounding_source.kind` = `kb_catalog_single_candidate` (allowlist) or `kb_pattern_extension` (KB file).

### 6. Coverage validation

For every component in `logical-architecture.yaml`:

- The component is covered by at least one entry whose `scope` resolves to include it. Scope resolution:
  - `scope.kind: global` → covers every component.
  - `scope.kind: components` → covers each component listed in `targets[]`.
  - `scope.kind: components_in_layer` → covers every component whose `layer` matches a target layer id.
  - `scope.kind: components_with_system_ref` → covers every component whose `system_ref` matches a target system id.

A component with NO covering entry → halt with `what_failed: component_coverage_gap` and the orphan component id.

SaaS-grounded components (system_ref pointing at a SaaS inventory entry with `origin: kb` or `stm_research` declaring the system is fully vendor-hosted) are exempt from language/runtime/framework coverage — the vendor owns the stack. They ARE NOT exempt from pattern coverage when patterns apply at the integration boundary.

### 7. Write outputs

Write `{output_path}` with `entries[]`. Write `{decision_manifest_path}` with one entry per tech-stack entry. All `user_response` start as `pending`.

### 8. Validate output

- Schema rules from the Output section all hold.
- Every pattern entry has `pattern_citation.source` and `pattern_citation.reference`; source passes the allowlist OR a KB file with the pattern exists.
- Every component in logical-architecture has at least one covering entry (SaaS components covered for patterns at integration boundary; exempt from runtime coverage).
- No fabricated pattern names: deny-list rejects `{product_name}-pattern`, `{team_name}-pattern`, or any pattern whose `pattern_citation.source` is empty / "internal" / "team standard" / similar.
- Decision manifest complete.

## Output Contract

On success:

```json
{
  "status": "success",
  "skill": "derive-tech-stack",
  "outputs": {
    "tech_stack_path": "{product_base}architecture/tech-stack.yaml",
    "decision_manifest_path": "{product_base}architecture/decision-manifest-derive-tech-stack.yaml",
    "entry_count": <int>,
    "pattern_entry_count": <int>,
    "decisions_count": <int>,
    "halted_slots": [
      { "kind": "language | runtime | framework | library | tool | pattern", "slot_id": "...", "reason": "multi_candidate | undocumented_pattern", "grounding_question_id": "Q-arch-NNN" }
    ]
  }
}
```

On failure:

```json
{
  "status": "failure",
  "skill": "derive-tech-stack",
  "what_failed": "missing_input | component_coverage_gap | undocumented_pattern | fabricated_pattern_name | pattern_citation_missing | manifest_incomplete",
  "details": "..."
}
```

## Evals

| Eval | Failure Bound | Check |
|------|---------------|-------|
| TS-1 | F10 (tech-stack entry missing fields) | Every entry has non-empty id, scope.kind, category, name, source_type, rationale; scope.targets non-empty when kind != global. |
| TS-2 | F9 (pattern without literature, or system-level outside tech-stack) | Every `category: pattern` entry has `pattern_citation.source` and `pattern_citation.reference` non-empty; source matches the canonical allowlist OR a KB file at `{kb_patterns_dir}{pattern-id}.md` exists and claims the pattern. System-level decisions (monolith / microservice / serverless / modular monolith) appear as `category: pattern` entries here. |
| TS-3 | C16 — fabricated patterns | No pattern_citation.source is empty, "internal", "team standard", "{product_name}-pattern", "{team_name}-pattern", or any non-publication source. |
| TS-4 | Coverage | Every component in logical-architecture.yaml has at least one tech-stack entry covering it (SaaS-grounded components covered for integration patterns; exempt from runtime coverage). |
| TS-5 | F16 (manifest missing/malformed) | Decision manifest exists with one entry per tech-stack entry; every entry has decision_id, decision_type, entry_id, tier, grounding_source, recommendation, alternatives_considered. |
| TS-6 | F13 (source_type discipline) | No decision has `grounding_source.kind: agent_default_unilateral`. |
| TS-7 | C16 (KB read-only) | The skill wrote NO file under `kb_stacks_dir`, `kb_patterns_dir`, `kb_agentic_dir`, or `kb_tech_dir`. |

## Constraints

- Writes ONLY to `{output_path}`, `{decision_manifest_path}`, and (for multi-candidate halts) appends to `{grounding_questions_path}`.
- Read-only on every input path including all KB directories.
- NEVER fabricates a pattern name. NEVER cites an undocumented pattern. When neither the allowlist nor KB covers a needed pattern, halt — KB extension via /enrich is the path.
- System-level decisions LIVE HERE as `category: pattern` entries. They do NOT belong in a separate artifact.
- Multi-candidate slots → C20 halt with grounding question OR checkpoint defer.
- Respects C18/C19 surfacing tiers.

## Failure modes

- `missing_input` — required input path absent and no stand-in.
- `component_coverage_gap` — a logical component has no tech-stack entry covering it.
- `undocumented_pattern` — a needed pattern is not on the allowlist AND has no KB pattern file with citation.
- `fabricated_pattern_name` — a pattern entry's citation source matches the deny-list (empty, internal, team standard, etc.).
- `pattern_citation_missing` — a `category: pattern` entry has no pattern_citation.source or reference.
- `manifest_incomplete` — decision manifest missing or any entry lacks required fields.
