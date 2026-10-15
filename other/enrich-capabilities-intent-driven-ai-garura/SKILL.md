---
name: enrich-capabilities
description: For each selected capability, merge project-profile-specific overrides onto the KB base values (business rules, depth spectrum cap, experiential warnings), producing enriched-capabilities.yaml — the input to intent-epic generation.
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Grep
deprecated: true
deprecated_note: '#434 ProductOS realignment — superseded by the command model; retained for Phase E reference, not installed'
---

# enrich-capabilities

> **Defect 23 — Decision Surfacing Discipline (DSD):** This skill emits a `decision-manifest.yaml` alongside its primary artifact. Every inferred decision produced during execution is recorded in the manifest with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Model-invocable skill for context-merging KB capability data with project-specific overrides. Called by `product-keeper` during `specify` Stage 4.

## Purpose

The KB catalog holds generic feature definitions. The project profile holds specific context (security level, compliance, audience, timeline). This skill merges the two so downstream epic generation has a single enriched source per capability — no downstream skill re-reads the KB or re-applies the profile.

## Input

Receive from product-keeper:
- `scope_path` (path, required) — scope.yaml from configure-capabilities
- `project_profile_path` (path, required) — frozen project profile YAML
- `ltm_domain_taxonomy_path` (path, required) — `core/components/memory/knowledge/domain/`
- `market_brief_path` (path, optional) — used for additional context
- `output_path` (string, required) — `.garura/product/scope/garura:enriched-capabilities.yaml`
- `decision_manifest_path` (path, required) — path for the `decision-manifest.yaml` output, written alongside the primary artifact (e.g., `.garura/product/scope/decision-manifest-enrich-capabilities.yaml`). Exact path is passed by the calling agent.

## Process

### 1. Load scope

Parse `scope.yaml`. Iterate over `selected_capabilities`. For each capability, note its `id`, `domain`, and any `depth_cap` from constraint_trace.

### 2. For each selected capability, read the KB block

Use grep to isolate the specific feature block in `{domain}.md` (e.g., `grep -A 200 "^### UM-F001" user-management.md` stopping at the next `###`). Parse:
- The 4 prose sections (`When It Matters`, `Depth Spectrum`, `Signals`, `Tradeoffs`)
- The 5 structured sections (`Inclusion`, `Success Criteria`, `Failure Scenarios`, `Cross-Tree Refs`, `Experiential`)

### 3. Apply profile overrides

For each capability:
- **Depth selection:** determine which depth level (Basic / Standard / Advanced / Enterprise) applies based on the Signals section and the profile. If a `depth_cap` was set by cross-tree constraints (e.g., CTC-005 timeline=tight → cap at Standard), honor it.
- **Business rules:** extract rules implied by the selected depth. If the profile says `security_level: critical`, pick the strictest business rules from the Depth Spectrum's Enterprise level even if Standard was selected for depth — security rules ratchet up regardless of depth. **Every extracted rule carries its source_for_quantification per Rule 9** — a rule derived from a KB Depth Spectrum bullet is tagged `kb_default` with a source_reference to the exact KB location, and is surfaced at the capability-configuration checkpoint for user confirmation per Rule 11.
- **Success criteria:** pass through from the KB Success Criteria section. **Every numeric value in a success criterion carries source_for_quantification.** Default source is `kb_default` with source_reference pointing at the KB line; the skill also cross-checks numbers against the project profile and flags `profile_mismatch` if a number contradicts a profile field (e.g., "10K concurrent" when `nfr_scale=2`).
- **Failure scenarios:** pass through from the KB Failure Scenarios section, enriched with profile-specific impact notes (e.g., "Impact on HIPAA-regulated flow" when compliance contains HIPAA).
- **Experiential warnings:** extract from the KB Experiential section — specifically the "Common mistakes" list.

**Anti-hallucination rule (Rule 11):** the skill MAY NOT invent business rules, numeric thresholds, limits, or values that are not in the KB feature block, the profile, or the brief. Boilerplate numbers pulled from KB Success Criteria sections are tagged `kb_default` and surfaced for user grounding — they are NOT silently promoted to facts.

### 4. Compose enriched record per capability

```yaml
enriched_capabilities:
  - id: UM-F001
    domain: user-management
    name: "Login / Authentication"
    selected_depth: standard | advanced | enterprise
    depth_cap_applied: null | standard | advanced
    profile_context:
      security_level: <from profile>
      industry: <from profile>
      compliance: <list from profile>
    business_rules_applied:
      - rule: "Lock after 3 failed attempts — HIGH security level"
        source_for_quantification:
          source: profile_nfr            # 'HIGH security level' comes from profile.nfr_security >= 3
          source_reference: "profile.nfr_security >= 3"
      - rule: "Session timeout 15 minutes idle — enterprise profile"
        source_for_quantification:
          source: kb_default             # the 15-minute value is KB boilerplate
          source_reference: "kb.user-management.UM-F001.depth_spectrum.enterprise.business_rules[2]"
          surfaced_at_checkpoint: true   # Rule 11 — awaiting user grounding
    success_criteria:
      - criterion: "Login success rate > 95% on first attempt"
        source_for_quantification:
          source: kb_default
          source_reference: "kb.user-management.UM-F001.success_criteria[0]"
          surfaced_at_checkpoint: true
      - ...
    failure_scenario:
      - "..."
      - "..."
    experiential_warnings:
      - "Skipping rate limiting on login endpoint"
      - ...
    kb_source:
      file: core/components/memory/knowledge/domain/user-management.md
      feature_id: UM-F001
      depth_spectrum_used: <depth>
```

### 4b. Emit decision manifest

Before writing the primary artifact, write `decision-manifest.yaml` to `{decision_manifest_path}`.

Record every inferred decision produced during Step 3. Assign tier at runtime based on grounding source: **high** when the decision was a direct match against a KB rule, file, or catalog entry; **mid** when context was built via web research; **low** when neither KB nor research yielded a grounding source.

**Decisions to record** (decision_id prefix: `D-ec-`):

| decision_id | decision_type | What is being decided |
|-------------|---------------|-----------------------|
| `D-ec-001` | `security-compliance-ratchet-selection` | Which security/compliance business rules are ratcheted up based on profile `security_level` and compliance flags (e.g., NIST 800-63B AAL3 when `security_level: critical`), including which specific KB Depth Spectrum rules drove the ratchet and at which level |

```yaml
schema_version: "1.0"
skill: "enrich-capabilities"
generated_at: "{ISO8601}"
decisions:
  - decision_id: "D-ec-001"
    decision_type: "security-compliance-ratchet-selection"
    tier: high | mid | low   # assign at runtime per grounding source
    grounding_source:
      kind: kb_path | web_citation | none
      ref: "{KB file path | URL | null}"
      excerpt: "{optional short quote when kind=kb_path}"
    recommendation: "{which rules were ratcheted and to which level}"
    alternatives_considered:
      - alt: "{alternative ratchet level}"
        why_not: "{one-line dismissal reason}"
    agent_reasoning_summary: "{2-3 sentence explanation}"
    user_response: null
    user_response_detail: null
```

### 5. Write enriched-capabilities.yaml

Write all enriched records to `{output_path}`. Include a top-level `status: DRAFT`, `created_at` timestamp, `source_scope_path` reference.

### 6. Return output contract

```yaml
enriched:
  path: <written path>
  enriched_count: <int>  # should match scope.selected_capabilities count
  missing_kb_sources: <int>  # must be 0 — any >0 is a structured failure
decision_manifest:
  path: <written path>
  decisions_recorded: <int>
```

## Constraints

- NEVER invent business rules not derivable from the KB feature's Depth Spectrum or Tradeoffs sections.
- NEVER silently drop a scope entry. If a feature can't be found in the KB, return structured failure with the dangling ID.
- NEVER modify the KB catalog — this skill is read-only on domain-taxonomy.
- ALWAYS honor depth caps from cross-tree constraints.
- ALWAYS ratchet security / compliance business rules UP when the profile demands it, even if depth says otherwise.
- ALWAYS include every KB section's data (business_rules, success_criteria, failure_scenario, experiential_warnings) in the enriched record. Note: the KB markdown uses the section heading "Failure Scenarios" — enrich-capabilities reads that section and emits its cause strings as `failure_scenario` (plain strings) in the enriched record, matching the new epic schema vocabulary.
- Read feature blocks selectively via grep — do not bulk-load whole domain files.
- NEVER commit an inferred decision to the primary artifact (enriched-capabilities.yaml) without recording it in `decision-manifest.yaml` first.
- NEVER tag a decision `tier: high` unless the `grounding_source.kind` is `kb_path` AND the referenced KB file exists.
- ALWAYS include `alternatives_considered` (≥1 entry) for every decision, even high-confidence ones.

## Version

| Field | Value |
|-------|-------|
| Version | 0.2.0 |
| Category | product-planning |
| Created | 2026-04-14 |
| Related | `core/components/skills/configure-capabilities`, `core/components/skills/generate-intent-epics`, `core/components/memory/standards/rules/kb-extension.md` |
