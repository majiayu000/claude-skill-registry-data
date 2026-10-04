---
name: derive-systems-inventory
description: Stage 1 skill of /arch. Walks selected capabilities, identifies the system (and any sub-systems) that serves each one, and populates the product's systems-inventory by pulling KB-grounded systems with provenance or authoring novel systems as stm_research with the required KB-extension shape. Output is the inventory every later /arch stage reads.
version: 0.1.0
user-invocable: false
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# derive-systems-inventory

> **Decision Surfacing Discipline:** This skill emits a `decision-manifest-derive-systems-inventory.yaml` alongside its primary artifact. Every inferred system selection and sub-system definition is recorded with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Called by `tech-architect` during `arch` Stage 1. Produces one file per system at `{product_base}architecture/systems-inventory/{system-id}.md` plus a decision manifest.

## Purpose

Establish the product's systems inventory before any other /arch stage runs. Every component in logical and physical architecture later RESOLVES to a system or sub-system in this inventory — components are SELECTED from inventory, not invented at logical-time. This skill is the gate that makes that traceability possible.

A "system" is a real product or platform the architecture depends on: ERP, CRM, CMS, DAM, identity provider, payment gateway, search engine, observability platform, content store, etc. A "sub-system" is a child surface of the same system — a CMS with an authoring app and a delivery API, an ERP with a finance module and an inventory module. Sub-systems are nested INSIDE the parent system's file, not stored as separate inventory files.

Systems are sourced from one of two paths:
- **KB pull-to-product** when the system already has a canonical KB file under `core/components/memory/knowledge/arch/systems/{system-id}.md` — the file is copied into product space with a provenance header and frozen (`editable: false`).
- **stm_research** when the system is not yet in KB — the agent authors a new file in product space with `origin: stm_research`, `editable: true`, and the full KB-extension required sections. Promotion to KB happens later via `/enrich` after vetting; this skill does NOT write to KB.

## Input

Receive from the `tech-architect` agent. All paths resolve against `{product_base}` and `{ltm_base}` supplied by the play via JSON contract.

- `scope_path` (path, required) — `{product_base}scope/scope.yaml`. When missing or DRAFT (C1 soft pre-flight), the play's question fallback writes `{product_base}specification/capabilities-stand-in.yaml` with `origin: stm_user_answer` and this skill reads that instead. Either way, the skill ingests a `selected_capabilities[]` list.
- `enriched_capabilities_path` (path, optional) — `{product_base}scope/garura:enriched-capabilities.yaml`. Provides business rules and constraint notes per capability for system reasoning.
- `domain_research_dir` (path, optional) — `{product_base}research/`. Domain context per selected domain.
- `project_profile_path` (path, required) — `{product_base}user-provided/project-profile.yaml`. Skill consults `grounded_tools.systems[]` for pinned system choices.
- `kb_systems_dir` (path, required) — `{ltm_base}components/memory/knowledge/arch/systems/`. The KB catalogue — authoring surface only. NEVER written to by this skill.
- `kb_extension_rules_path` (path, required) — `{ltm_base}components/memory/standards/rules/kb-extension.md`. The required-sections shape every inventory file must satisfy.
- `inventory_dir` (string, required) — `{product_base}architecture/systems-inventory/`. The skill's primary write target.
- `decision_manifest_path` (string, required) — `{product_base}architecture/decision-manifest-derive-systems-inventory.yaml`.
- `grounding_questions_path` (string, required) — `{product_base}user-provided/grounding-questions.md`. Append-only path for multi-candidate halts (C20).

## Output

### Per-system inventory file

One file per system at `{inventory_dir}{system-id}.md` with frontmatter then KB-extension sections.

**Frontmatter** (YAML, between `---` fences):

```yaml
id: {system-id}                          # kebab-case, unique within the inventory
name: {Human-readable name}
origin: kb | stm_research                # source of this file
kb_path: {ltm_base}components/memory/knowledge/arch/systems/{system-id}.md   # only when origin=kb
kb_version_sha: {sha256 of the KB file at copy time}                          # only when origin=kb
copied_at: {ISO 8601 timestamp}                                               # only when origin=kb
editable: false | true                   # false for kb-origin, true for stm_research
provenance_summary: |                    # one paragraph — why this system was selected for this product
  {prose}
capabilities_served:                     # capability IDs from scope.selected_capabilities this system serves
  - {capability_id}
sub_systems:                             # optional; nested child surfaces of THIS system
  - id: {sub-system-id}                  # kebab-case, unique within this system's sub_systems[]
    name: {Human-readable name}
    responsibilities:
      - {one bullet per primary responsibility}
    capabilities_served:
      - {capability_id from scope.selected_capabilities}
```

**Required sections** (Markdown headings after the frontmatter). Section list mirrors the existing arch KB shape so KB-pulled and stm_research-authored files are interchangeable downstream:

```markdown
# {Name}

## When to Use
{Prose. Conditions under which this system is the right choice for the kind
of capability listed in capabilities_served. References product profile and
NFR dimensions in context, not conditional rules.}

## When to Avoid
{Anti-conditions. Just as important as When to Use.}

## Scale Profile
{Sweet spot in team size, user count, data volume, throughput. Where it
shines, where it stretches, where it breaks.}

## Capabilities Served
{Prose list — same set as the frontmatter capabilities_served, with one
line per capability explaining the fit.}

## Sub-Systems
{When the system has multiple capability-distinct surfaces, list each
sub-system here with a one-paragraph description that mirrors the
frontmatter sub_systems[] entry. When there are no sub-systems, write
"None — this system is treated as a single surface."}

## Tradeoffs
{Cost, vendor lock-in, operational burden, integration cost, exit cost,
ecosystem maturity. Helps later /arch stages reason about NFR delivery
and risks.}

## Anti-Patterns
{Common mistakes when using this system. Misuses to call out for the
implementing team.}
```

### Decision manifest

One YAML file at `{decision_manifest_path}` with one entry per system written AND one entry per sub-system defined.

```yaml
manifest:
  skill: derive-systems-inventory
  written_at: {ISO 8601 timestamp}
  decisions:
    - decision_id: SI-001
      decision_type: system_selection | sub_system_definition
      tier: high | mid | low
      grounding_source:
        kind: project_profile_pin | kb_catalog_single_candidate | kb_catalog_multi_candidate_user_approved | user_direct_answer | agent_default_with_user_approval
        citation: {profile slot | kb file path | grounding-question ID | checkpoint ID}
      recommendation: {chosen system or sub-system id}
      alternatives_considered:
        - id: {alt}
          why_rejected: {one line}
      agent_reasoning_summary: |
        {2-4 line prose summary of how the agent arrived at the recommendation}
      user_response: accept | override | orbit | pending    # set by orchestrator after surfacing
      user_response_detail: {free text — null when pending}
```

## Process

### 1. Read inputs

- Read `scope_path` (or its stand-in) → list of selected capability IDs with names.
- Read `enriched_capabilities_path` if present → per-capability business rules and constraint notes.
- Read every file under `domain_research_dir` if present → domain context for capability framing.
- Read `project_profile_path` → `grounded_tools.systems[]` (may be empty).
- Glob `kb_systems_dir` → KB catalogue of known systems with their declared `capabilities_served`.
- Read `kb_extension_rules_path` → confirm required-sections list and provenance-header rules.

### 2. Validate pre-conditions

- Required inputs must exist OR a documented stand-in must exist (`capabilities-stand-in.yaml` for missing scope).
- `inventory_dir` exists (create if not).
- `grounding_questions_path` exists (create if not, with the standard preamble).

Missing required input with no stand-in → structured failure with `what_failed: missing_input` and the path.

### 3. Walk capabilities and identify systems

For each capability in the selected list, in scope-declared order:

1. **Pin check.** If `project_profile.grounded_tools.systems[]` carries an entry for this capability (matched by capability ID), the pinned system is authoritative. Record decision with `tier: high`, `grounding_source.kind: project_profile_pin`. Proceed to Step 4 with the pinned system as the choice.

2. **KB candidate query.** Glob `kb_systems_dir/*.md` and collect every file whose frontmatter `capabilities_served` includes this capability ID (or its parent domain when capability-level matches are absent).

3. **Resolve by candidate count:**
   - **Exactly one candidate** → record decision with `tier: high`, `grounding_source.kind: kb_catalog_single_candidate`, citation = KB path. Proceed to Step 4.
   - **Multiple candidates** → halt this slot per C20. Append a `Q-arch-NNN` question to `grounding_questions_path` listing the candidate set with one-line summaries from each KB file's frontmatter. Record decision with `tier: mid`, `grounding_source.kind: kb_catalog_multi_candidate_user_approved`, citation = question ID. user_response stays `pending` until the orchestrator drives surfacing.
   - **Zero candidates** → enter research mode (Step 5).

### 4. Write the system file (KB pull-to-product path)

When the chosen system is grounded in a KB file:

- Compute SHA-256 of the KB file content.
- Read the KB file content.
- Write `{inventory_dir}{system-id}.md` with the canonical frontmatter (origin: kb, kb_path, kb_version_sha, copied_at, editable: false) prepended to the KB body. Append `capabilities_served:` for this product run (the subset relevant to this product), and `provenance_summary:` explaining why this system was selected here.
- Preserve KB body byte-for-byte under the inventory frontmatter.

If the file already exists from an earlier capability walk (same system serves multiple capabilities), MERGE: add the new capability ID to `capabilities_served` and extend `provenance_summary` with the additional reason. Do NOT re-pull from KB if `kb_version_sha` matches.

### 5. Author the system file (stm_research path)

When no KB file exists for the chosen system:

- Agent gathers context from KB tech-stacks, KB platforms, KB patterns, and web research as needed.
- Agent drafts the file at `{inventory_dir}{system-id}.md` with:
  - frontmatter carrying `origin: stm_research`, `editable: true`, `provenance_summary` explaining the research basis.
  - All required sections (When to Use, When to Avoid, Scale Profile, Capabilities Served, Sub-Systems, Tradeoffs, Anti-Patterns) populated with non-empty prose.
- Record decision with `tier: low`, `grounding_source.kind: agent_default_with_user_approval` (citation = next stage checkpoint ID), `alternatives_considered` listing any other systems the agent considered.
- Orchestrator surfaces this one-by-one per C19 LOW-tier discipline before the file influences any downstream stage.

### 6. Define sub-systems where capability surfaces diverge

For each system file written or merged in Steps 4-5, examine the union of capabilities the system now serves. When two or more capabilities require capability-distinct surfaces of the same system (e.g., a CMS where one capability is content authoring and another is content delivery to consumers), define sub-systems:

- Author each sub-system inside the parent system file's frontmatter `sub_systems[]` block with `id`, `name`, `responsibilities[]`, `capabilities_served[]`.
- Update the file body's `## Sub-Systems` section with prose mirroring the frontmatter.
- Record one decision-manifest entry per sub-system with `decision_type: sub_system_definition`.

Do NOT define sub-systems for every system reflexively — only when the served capabilities have genuinely different responsibility shapes inside the same system. A monolithic CRM serving multiple sales capabilities through the same surface does NOT need sub-systems.

### 7. Emit the decision manifest

Write `{decision_manifest_path}` with one entry per system selection and one per sub-system definition, populated per the schema in the Output section. Set `user_response: pending` on every entry — the orchestrator updates these after surfacing.

### 8. Validate output

Before returning, verify:

- Every capability in `selected_capabilities` is claimed by `capabilities_served` of at least one inventory file (system-level or sub-system-level).
- Every inventory file has frontmatter `id`, `origin`, `provenance_summary`, `capabilities_served[]` non-empty, and all required Markdown sections present and non-empty.
- KB-origin files: `kb_version_sha` matches a re-computed hash of the KB master at `kb_path`; the file body matches the KB body byte-for-byte (after the inventory frontmatter is stripped).
- stm_research files carry `editable: true` and have all sections populated.
- Decision manifest exists and every entry has all required fields (with `user_response: pending` acceptable at this stage).

Any failure → structured failure with `what_failed` and the offending file or capability.

## Output Contract

On success:

```json
{
  "status": "success",
  "skill": "derive-systems-inventory",
  "outputs": {
    "inventory_dir": "{product_base}architecture/systems-inventory/",
    "inventory_files": [
      { "system_id": "...", "path": "...", "origin": "kb|stm_research", "capabilities_served": [...] }
    ],
    "decision_manifest_path": "{product_base}architecture/decision-manifest-derive-systems-inventory.yaml",
    "decisions_count": <int>,
    "halted_slots": [
      { "capability_id": "...", "grounding_question_id": "Q-arch-NNN" }
    ]
  }
}
```

On failure:

```json
{
  "status": "failure",
  "skill": "derive-systems-inventory",
  "what_failed": "missing_input | empty_capability_orphan | malformed_frontmatter | kb_sha_mismatch | missing_required_section | manifest_incomplete",
  "details": "..."
}
```

## Evals

| Eval | Failure Bound | Check |
|------|---------------|-------|
| SS-1 | F23 (logical/physical inventory grounding) | Every capability in `selected_capabilities` is named in `capabilities_served` of at least one inventory file (system-level OR sub-system-level). |
| SS-2 | F22 (system without provenance) | Every inventory file frontmatter declares `origin` ∈ {kb, stm_research}, and KB-origin carries `kb_path`, `kb_version_sha`, `copied_at`, `editable: false`. |
| SS-3 | F22 | KB-origin file body matches the KB master byte-for-byte under the inventory frontmatter. |
| SS-4 | F22 | stm_research file carries `editable: true` and has all 7 required Markdown sections populated with non-empty prose. |
| SS-5 | F16 (manifest missing/malformed) | `decision-manifest-derive-systems-inventory.yaml` exists with one entry per system written and one per sub-system defined; every entry has decision_id, decision_type, tier, grounding_source, recommendation, alternatives_considered. |
| SS-6 | F14 (multi-candidate without asking) | When a capability had multiple KB candidates and no project-profile pin, the manifest records `grounding_source.kind: kb_catalog_multi_candidate_user_approved` and a `Q-arch-NNN` question exists in grounding-questions.md OR the slot is recorded as `user_response: pending` for orchestrator surfacing. |
| SS-7 | F13 (source_type discipline) | No decision is recorded with `grounding_source.kind: agent_default_unilateral`. |
| SS-8 | C16 (KB read-only) | The skill wrote NO file under `kb_systems_dir`. |

## Constraints

- The skill writes ONLY to `{inventory_dir}`, `{decision_manifest_path}`, and (for multi-candidate halts) appends to `{grounding_questions_path}`. No other write paths.
- The skill NEVER modifies `kb_systems_dir` — KB is authoring surface, /enrich is the promotion path.
- The skill NEVER names a tech product, runtime, or library when reasoning about capability-to-system fit. Tech selection belongs to `derive-tech-stack`.
- The skill respects C20 (multi-candidate halt) and emits decisions to the manifest for C18/C19 surfacing discipline.
- The skill is read-only with respect to `scope.yaml`, `enriched-capabilities.yaml`, `project-profile.yaml`, and every domain research file.

## Failure modes

- `missing_input` — a required input path is absent and no stand-in exists.
- `empty_capability_orphan` — a selected capability has no inventory file claiming it after Steps 3-5 complete.
- `malformed_frontmatter` — an inventory file's frontmatter is missing required fields.
- `kb_sha_mismatch` — a KB-origin file's body diverges from the KB master at `kb_path`.
- `missing_required_section` — an stm_research file lacks one or more of the 7 required Markdown sections.
- `manifest_incomplete` — the decision manifest is missing or any entry lacks required fields.
- `kb_write_attempt` — the skill attempted to write under `kb_systems_dir` (structural violation, halts immediately).
