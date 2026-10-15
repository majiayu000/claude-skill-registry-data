---
name: recommend-mvp
description: Produce the MVP recommendation artifact at .garura/product/scope/mvp-recommendation.md. Narrows the capability walk by selecting primary use cases from the brief, deferring the rest with v1.1+ triggers, and recording any architecture directions committed at spec time. Called by product-keeper during specify Stage 2.75 (between domain-selection and configure-capabilities).
user-invocable: false
model: opus
allowed-tools: Read, Write, Grep, Glob
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# recommend-mvp

Model-invocable skill for authoring the MVP recommendation — the scope-narrowing decision artifact that sits between domain-selection (Stage 2) and configure-capabilities (Stage 3) in the `specify` pipeline. Implements Defect 6 as a first-class pipeline step.

## Purpose

Without an MVP recommendation, `configure-capabilities` walks every feature of every selected domain indiscriminately and produces a bloated v1 scope that tries to serve every use case the brief names. The result is an epic inventory that exceeds the project-profile's team_size × delivery_ambition × timeline envelope and a scope contract the team cannot ship. The MVP recommendation artifact is the bridge: it reads the opportunity landscape + domain shape + user-provided grounding answers and commits to a narrowed v1 scope with explicit deferrals.

This skill produces `.garura/product/scope/mvp-recommendation.md` conforming to `core/components/memory/standards/schemas/mvp-recommendation.yaml`. It does NOT make architectural choices — it commits to a product scope. Any architecture direction it records is capability-level, not tech-stack level (Rule 14 / specify C16 Abstraction-Layer Boundary).

## Input

Receive from the `product-keeper` agent via the play's JSON contract. All paths resolve against `{product_base}` supplied by the play — do not hard-code `.garura/product/` or assume a working directory.

- `project_brief_path` (path, required) — typically `{product_base}user-provided/project-brief.md`. The authoritative source for use cases, target audience, stated constraints, and the product's positioning. Every narrowing decision MUST trace to a quote or an absence in this file.
- `market_brief_path` (path, required) — typically `{product_base}specification/market-brief.md`. Provides the risk register, competitive landscape, and market gaps. The risks in particular seed the "risks that could kill this MVP" section of the output.
- `project_profile_path` (path, required) — typically `{product_base}specification/project-profile.yaml`. Provides team_size, delivery_ambition, budget_sensitivity, timeline, audience, and other dimensions that bound what v1 can realistically ship.
- `domain_selection_path` (path, required) — typically `{product_base}specification/domain-selection.yaml`. Lists the domains in scope for the product; the MVP narrowing operates on the capabilities within those domains.
- `product_research_path` (path, required) — typically `{product_base}research/`. The product's frozen domain library (per rules/product.md Rule 15 Pull-to-Product). This skill reads domain content from the product's research folder ONLY — never directly from `core/components/memory/knowledge/domain/`. Passing `ltm_domain_taxonomy_path` is a structural failure (specify F13).
- `grounding_questions_path` (path, required) — typically `{product_base}user-provided/grounding-questions.md`. Contains cumulative user answers to prior inferences from configure-capabilities and other skills. The recommender READS this file at start to pick up any user-stated narrowing preferences and APPENDS new questions if it encounters an ambiguity that requires user grounding.
- `domain_grounding_path` (path, optional) — typically `{product_base}specification/domain-grounding.yaml`. When present, provides the ubiquitous language + bounded-context map. The recommender uses bounded contexts as the natural grouping for "capabilities in scope" in section 2.1 of the output.
- `mvp_recommendation_schema_path` (path, required) — typically `core/components/memory/standards/schemas/mvp-recommendation.yaml`. The canonical schema documenting the required section order and validation rules. The recommender reads this at start to anchor its output shape.
- `output_path` (string, required) — typically `{product_base}scope/mvp-recommendation.md`. The recommendation file written at this path. Per Defect 9 / ADR 017, the file lives in `scope/` (not `specification/`) because it is a scope-narrowing decision artifact.

## Process

Resolve each input path by substituting `{product_base}` from the incoming JSON contract; do not re-prefix with `.garura/product/` or assume a working directory.

### 1. Load inputs

- Read `project_brief_path` in full. Extract the use cases it enumerates (typically in a "Who It's For" or "Use Cases" section). Every narrowing in the output must trace to this list.
- Read `market_brief_path`. Extract the Risks section — this feeds section 7 of the output.
- Read `project_profile_path`. Load team_size, delivery_ambition, budget_sensitivity, timeline, audience, scale, security_level, nfr dimensions, qp dimensions.
- Read `domain_selection_path` to understand which domains are in scope.
- Read `grounding_questions_path` if it exists. For any Q-*-NNN entry whose `user_decision` is non-null, treat the answer as a fact during this run — do NOT re-ask.
- Read `domain_grounding_path` if present. Use the bounded_contexts list to structure section 2.1 of the output.
- Read `mvp_recommendation_schema_path` to confirm the required section order and validation rules.

### 2. Narrow the primary use cases

For each use case the brief names:

- Classify as `v1-primary` if ALL of: (a) the use case is named in the brief, (b) it can be delivered within the project-profile envelope (team_size × delivery_ambition × timeline × budget_sensitivity), (c) it does not require capabilities that are only available from deferred use cases, (d) the user has not explicitly directed it out via grounding-questions.
- Classify as `v1.1+-deferred` otherwise. Record a defer reason (citing the specific constraint) and a v1.1+ trigger (a named observable signal that would justify unlocking the capability).

**Aggressive questioning (rules/product.md Rule 11):** if the classification is ambiguous — the brief doesn't clearly say whether a use case is in or out, and the profile doesn't force the answer — append a question to `grounding_questions_path` asking the user to decide. Do NOT invent a classification. Exit with `what_failed: ambiguous_narrowing_needs_user_grounding` and the list of ambiguous use cases if there are any the user must resolve before proceeding.

**Compact recommendations:** the typical v1 narrowing selects 1-3 primary use cases from a brief that names 3-7. If the brief names only 1 use case, all capabilities for that use case are in scope — the output still has a section 3 (Deferred to v1.1+) listing the v2 features the brief explicitly named as out-of-v1. If the brief names 8+ use cases and the project profile is solo/MVP/normal, the skill strongly narrows to 2 primary use cases and surfaces an inference question if it had to pick two specific ones without user direction.

### 3. Compose the recommendation sections

Author the 9 required sections per the schema:

1. **Snapshot** — bulleted summary block with product one-liner, MVP launch profile (audience + delivery ambition + budget + timeline from project-profile), primary use cases, deferred use cases, architecture commitments (empty or listed).

2. **Primary Focus** — three sub-sections:
   - 2.1 Use cases in scope (table with Status column: "v1 — in scope" or "v1.1+ — deferred")
   - 2.2 Why this narrowing (prose rationale citing brief quotes, project-profile dimensions, market-brief risks, grounding-questions answers)
   - 2.3 v1.1+ reuse pattern (how the narrowing positions v1.1+ growth — what architectural or capability pattern unlocks later verticals)

3. **Launch Scope (v1)** — two sub-sections:
   - 3.1 Capabilities in scope (organized by bounded context from domain-grounding.yaml if present, else by domain from domain-selection.yaml). Explicitly call out what is OUT of v1 scope per bounded context.
   - 3.2 Epic breakdown (preview — formal list at Stage 5). Count consistent with team_size × delivery_ambition. Solo+MVP+normal = 5-7 vertical epics.

4. **Deferred to v1.1+** — table with columns: Capability, Defer reason, v1.1+ trigger. Every brief-named use case not in section 1.1 MUST appear here.

5. **Architecture Directions Committed at MVP-Recommendation Time** — empty by default ("none — all architectural choices deferred to Stage 6"). Non-empty only when the user has directed a specific committment via grounding-questions. Each committed direction must be capability-level (Rule 14 Abstraction-Layer Boundary), explain why it's committed at spec time rather than Stage 6, and explicitly defer tech-stack choices.

6. **Pricing Direction** — directional, not diligence-grade. Tier structure + price ranges grounded in budget_sensitivity + brief cost mentions + market-brief competitor pricing. MUST contain the exact phrase "directional, not diligence-grade".

7. **Success Criteria — v1 is successful** — table mapping brief KPIs to thresholds. Any narrowing-specific override (e.g., relaxing a completion rate for a high-risk sub-capability) must be explicitly marked and sourced to the narrowing. Plus: go / no-go triggers for v1.1+ unlock.

8. **Risks That Could Kill This MVP** — inherited from market-brief.md risks + mvp-recommendation-specific new risks (e.g., "committing to architecture direction X at spec time means risk Y if X turns out wrong"). Each risk carries severity + mitigation + enforcing-gate reference where applicable.

9. **Rationale Summary** — 3-5 paragraph narrative. A PM should be able to read ONLY this section and understand the MVP choice.

### 4. Self-validate against the schema rules

Before writing, confirm:

- All 9 sections present and non-empty (section 5 may carry "none" as a single line)
- Every narrowing in section 1.1 traces to a brief quote or an absence
- Every deferred capability in section 3 has a defer_reason and a v1_1_trigger
- Section 5 pricing contains the exact phrase "directional, not diligence-grade"
- Section 7 KPI thresholds cite either a brief-explicit K-id or a narrowing override source
- Section 8 rationale summary is 3-5 paragraphs
- No section contains abstraction-layer deny-list tokens (see Constraints below)

If any self-check fails, halt with `what_failed: schema_violation` and the list of failures.

### 5. Invoke validate-abstraction-layer on the output

After writing `output_path`, invoke the `validate-abstraction-layer` skill against the written file. If it returns any violations, DELETE the written file and halt with `what_failed: abstraction_layer_violation` + the violation list. This prevents the file from being committed with prohibited tech-binding content.

### 6. Append provenance

Write section 9 Provenance:
- `authored_by`: "specify Stage 2.75 recommend-mvp skill"
- `authored_on`: ISO-8601 date
- `inputs_read`: list of every input path consumed
- `user_directives_honored`: list of Q-*-NNN ids from grounding-questions.md whose answers shaped the recommendation
- `abstraction_layer_compliance`: "compliant — no tech bindings (validated by validate-abstraction-layer)"
- `pull_to_product_compliance`: "domain references resolve to product/research/ only"

### 7. Return output contract

```yaml
mvp_recommendation:
  path: <output_path>
  primary_use_cases_count: <int>
  deferred_use_cases_count: <int>
  architecture_commitments_count: <int>  # typically 0
  sections_written: 9
  schema_compliance: passed
  abstraction_layer_compliance: passed
  pull_to_product_compliance: passed
  inference_questions_appended: <int>  # to grounding-questions.md
```

## Constraints

- NEVER invent use cases the brief did not name. Every primary use case in section 1.1 must trace to a brief quote.
- NEVER include tech-binding tokens in any section. Deny-list: specific database engines (Postgres, MySQL, SQLite, DynamoDB, Redis, etc.), specific SDK/framework method names and parameters, specific programming languages, specific build tools, specific table schemas with column lists and types, specific wire protocols (REST endpoint paths, gRPC method signatures), specific cryptographic constructions, and specific model or version identifiers. Architecture directions in section 4 describe capability-level shape, not tech stack. Rule 14 / specify C16.
- NEVER read domain content from `core/components/memory/knowledge/domain/` directly. Per Rule 15 / specify C17, this skill reads from `product_research_path` only. Passing `ltm_domain_taxonomy_path` is a structural failure.
- NEVER skip `validate-abstraction-layer` invocation after writing. The post-write validation is the enforcement boundary — without it, the skill could silently produce a file that violates C16.
- NEVER write to paths outside `output_path`. The mvp-recommendation.md is the only artifact this skill writes.
- NEVER proceed with ambiguous narrowing. If the brief + profile + grounding-questions together do not make the primary use cases clear, append a question and halt with `ambiguous_narrowing_needs_user_grounding` — Rule 11 Aggressive Questioning applies.
- NEVER treat pricing numbers as diligence-grade. The pricing section MUST carry the exact phrase "directional, not diligence-grade".
- ALWAYS cite brief quotes, project-profile dimensions, and grounding-questions answers as sources for narrowing decisions. Provenance in section 9 must list every source consulted.
- ALWAYS respect prior grounding-questions answers. A Q-*-NNN with `user_decision: in_scope` or `out_of_scope` is authoritative for this run.
- ALWAYS use the domain-grounding.yaml bounded_contexts as the structural grouping for section 2.1 when the file exists. This keeps the MVP recommendation aligned with the ubiquitous language the downstream epics will use.
- ALWAYS append an `inferences_pending_review` entry to grounding-questions.md for every ambiguous narrowing decision — Rule 12 User Questions Are First-Class Artifacts.

## Version

| Field | Value |
|-------|-------|
| Version | 0.1.0 |
| Category | product-planning |
| Created | 2026-04-15 |
| Related | `core/components/memory/standards/schemas/mvp-recommendation.yaml`, `core/components/memory/standards/rules/product.md` (Rule 13 MVP Focus), `core/components/plays/specify/reference/intent.yaml` (C15), `core/components/skills/configure-capabilities/SKILL.md` (primary consumer), `core/components/skills/validate-abstraction-layer/SKILL.md` (self-check invocation) |
