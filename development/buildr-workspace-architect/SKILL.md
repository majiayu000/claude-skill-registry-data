---
name: buildr-workspace-architect
description: |
  Runs a mandatory five-phase preflight architecture pipeline on a human
  project description before any workspace generation is allowed. Produces
  structured artifacts that freeze purpose, map absences, define minimal
  architecture, challenge assumptions, and synthesize approval or rejection.

  USE THIS SKILL when: a new workspace-generation request arrives via the
  advanced operator flow. The advanced operator identity always invokes this
  skill first. It is never optional.

  Triggers on: every new project description received by the Buildr Advanced
  Operator before workspace generation begins.

  This skill does NOT generate the workspace. It does NOT execute a workspace.
  It produces the preflight artifacts that gate workspace generation.

  v1 implementation: prompt-enforced gates (agent compliance).
  v2+ future: code-enforced schema validation in forge/bridge.
---

# Buildr Workspace Architect

## What This Skill Does

Takes a human project description and runs a mandatory five-phase architecture pipeline that produces structured artifacts. These artifacts gate workspace generation: no workspace may be created unless this skill outputs `PREFLIGHT_APPROVAL.json` with `status: approved`.

## What This Skill Does NOT Do

- It does not generate workspaces (that is operator-like generation).
- It does not execute workspaces (that is `buildr-executor`).
- It does not replace the operator pipeline — it precedes it.
- It does not make implementation decisions — it makes architectural commitments.
- It is not advisory — its approval gate is mandatory and blocking.

## Why This Is a System Skill

This skill orchestrates a multi-phase pipeline that gates a critical system boundary (workspace generation). It cannot be expressed as a vault item because:

- Vault items are single-purpose, self-contained instructions (max 60 lines for skills).
- This pipeline requires five sequential phases with inter-phase dependencies, binary gates, and structured artifact generation.
- It governs the system itself, not a task within a project.
- It satisfies the governance classification: "a system-level pipeline for orchestrating the Buildr system itself."
- It avoids the "Comfortable Package" anti-pattern: removing this skill would leave workspace generation ungated — a material regression in output quality. See `references/architecture.md` for the full justification.

## Trigger Rules

| Trigger | This Skill? | Instead Use |
|---------|------------|-------------|
| New project description via advanced operator | YES | — |
| Resume an existing workspace | NO | `buildr-executor` |
| Execute a generated workspace | NO | `buildr-executor` |
| Create a vault item | NO | `buildr-smith` |
| Research an external source | NO | `buildr-scout` |
| Direct operator invocation (basic/legacy path) | NO | `buildr-operator` |

This skill activates exclusively for new workspace-generation requests in the advanced flow. It never competes with executor, smith, or scout triggers.

## Required Inputs

- `project_description`: The full human project description (string, non-empty).
- `project_slug`: Derived by the advanced operator per slug rules (string, `[a-z0-9-]`, max 64 chars).

## Staging Path

All artifacts are written to:

```
v2/.buildr/preflight/<project-slug>/
```

## Output Artifacts

| Phase | Markdown | JSON | Produced By |
|-------|----------|------|-------------|
| 1 | `PREFLIGHT_PURPOSE.md` | `PREFLIGHT_PURPOSE.json` | Purpose Extraction |
| 2 | `PREFLIGHT_ABSENCE_MAP.md` | `PREFLIGHT_ABSENCE_MAP.json` | Absence Mapping |
| 3 | `PREFLIGHT_ARCHITECTURE.md` | `PREFLIGHT_ARCHITECTURE.json` | Minimal-Inevitable Architecture |
| 3 | `PREFLIGHT_ACCEPTANCE.md` | `PREFLIGHT_ACCEPTANCE.json` | Acceptance Criteria Packaging |
| 4 | `PREFLIGHT_CHALLENGE.md` | `PREFLIGHT_CHALLENGE.json` | Skeptical Challenge |
| 4 | `PREFLIGHT_DECISIONS.md` | `PREFLIGHT_DECISIONS.json` | Decision Record |
| 5 | `PREFLIGHT_APPROVAL.md` | `PREFLIGHT_APPROVAL.json` | Approval Synthesis |
| 5 | `PREFLIGHT_BUILD_ORDER.md` | — | Build Order |

Both formats are required because:
- **Markdown** is for human review, discussion, and audit trail.
- **JSON** is for machine consumption: future forge/bridge validation, automated checks, and programmatic ingestion into workspace generation.

## The Pipeline

```
Phase 1: PURPOSE EXTRACTION
    |  Gate: all CRI fields populated, >= 1 purpose claim
    v
Phase 2: ABSENCE MAPPING
    |  Gate: all 6 ELS categories addressed, no unaddressed unknowns
    v
Phase 3: MINIMAL-INEVITABLE ARCHITECTURE
    |  Gate: N >= max(5, ceil(purpose_claims * 2)) acceptance criteria
    v
Phase 4: SKEPTICAL CHALLENGE
    |  Gate: all decisions have >= 2 alternatives, no ungated high-risk decisions
    v
Phase 5: APPROVAL SYNTHESIS
    |  Gate: all prior gates passed, status is approved|rejected|insufficient_information
    v
Output: PREFLIGHT_APPROVAL.json
```

---

## Phase 1: Purpose Extraction

### Objective

Extract the project's purpose from the human description and freeze it as structured, testable claims. Separate what the project IS from what the project DOES from who the project SERVES.

### Required Inputs

- `project_description` (the human's words, unmodified)

### Process

1. Read the full project description without filtering.
2. Extract purpose claims: discrete, testable statements about what the project must achieve. Each claim must be falsifiable — you could build a test that either passes or fails.
3. Extract CRI (Commercial Reality Invariants):
   - `target_customer_or_user_class`: Who uses this? Be specific. "Users" is not acceptable.
   - `primary_user_job_to_be_done`: One sentence. What job does the user hire this product to do?
   - `business_outcome_hypothesis`: What measurable outcome improves if this succeeds?
   - `monetization_model`: One of `none` | `subscription` | `usage` | `transaction_fee` | `ads` | `enterprise_contract` | `other`. If the intent is clearly for-profit but monetization is unspecified, set to `unknown`.
   - `must_have_constraints`: Time, budget, compliance constraints. Each marked `user_stated` or `unknown`.
   - `kill_switch_triggers`: Binary conditions that should stop the project entirely (e.g., "if we cannot process payments within 4 weeks, stop").
4. Identify explicit assumptions: what the description takes for granted.
5. Identify explicit exclusions: what the description rules out.
6. Identify provisional scope: what the description implies but does not confirm.

### Mandatory Questions to Resolve

- Is the purpose singular or compound? If compound, can it be decomposed?
- Are there implicit users not named in the description?
- Does the description contain contradictions?
- Are there unstated commercial constraints?

### Written Outputs

- `PREFLIGHT_PURPOSE.md`: Narrative purpose extraction with CRI summary.
- `PREFLIGHT_PURPOSE.json`: Structured payload per `preflight-handoff.schema.json`, including all CRI fields.

### Completion Condition (binary)

Phase 1 is COMPLETE when ALL of the following are true:
- At least one `purpose_claim` exists and is falsifiable.
- `target_customer_or_user_class` is populated and not "users" or "everyone."
- `primary_user_job_to_be_done` is a single sentence.
- `business_outcome_hypothesis` is populated.
- `monetization_model` is populated (may be `unknown` — triggers gate in Phase 5).
- Both `.md` and `.json` artifacts are written to staging.

### Fail Conditions

- Zero extractable purpose claims from the description.
- Description is too vague to identify even one target user class.
- Description contains irreconcilable contradictions that cannot be flagged as known unknowns.

If Phase 1 fails: write `PREFLIGHT_PURPOSE.json` with `status: insufficient_information` and `required_missing_inputs` listing what is needed. The pipeline terminates — no downstream phases run.

### What Phase 2 May Trust

- `purpose_claims` are stable (will not be revised by later phases unless preflight is reopened).
- `target_customer_or_user_class` is stable.
- `assumptions` and `exclusions` are provisional — Phase 2 may add to them but not remove confirmed ones.
- `monetization_model` value is frozen — downstream phases may flag it but not change it.

---

## Phase 2: Absence Mapping

### Objective

Systematically identify what is NOT in the project description: missing information, unstated assumptions, known unknowns, and expensive-late-failure risks. This phase makes the invisible visible.

### Required Inputs

- `PREFLIGHT_PURPOSE.json` (Phase 1 output)
- `project_description` (original)

### Process

1. Read Phase 1 outputs.
2. For each `purpose_claim`, ask: what information is needed to build this that the description does not provide?
3. For each assumption, ask: what happens if this assumption is wrong?
4. Run the Expensive-Late-Failure Scan (ELS) across all six mandatory categories.
5. Classify each absence as:
   - `derivable`: Can be inferred with high confidence from context (e.g., location implies payment provider).
   - `askable`: Must be answered by the user before proceeding.
   - `deferrable`: Can be deferred to execution without architectural risk.
   - `blocking`: Cannot proceed without resolution; architecturally load-bearing.

### ELS (Expensive-Late-Failure Scan)

Each of the following six categories MUST be addressed. Use `not_applicable` only with a one-line proof of why.

| Category | What to examine |
|----------|----------------|
| `security_abuse_and_threats` | AuthZ/AuthN model, tenancy boundaries, secrets management, injection surfaces, abuse vectors |
| `privacy_and_data_governance` | PII handling, data retention, deletion rights, jurisdictional constraints, consent model |
| `payments_and_money_movement` | Payment processing, refunds, disputes, currency handling, financial compliance |
| `operational_reliability` | SLO expectations, disaster recovery, backup strategy, monitoring hooks (as requirements, not implementation) |
| `accessibility_and_inclusive_design` | WCAG level, assistive technology support, responsive requirements (if user-facing UI exists) |
| `legal_and_policy_constraints` | Licensing, export controls, industry-specific regulations, terms of service requirements |

For each category, produce `els_risks[]` entries with:
- `risk`: What could go wrong.
- `why_late_discovery_is_expensive`: Concrete cost of discovering this late (rework hours, compliance fines, data breach).
- `earliest_cheap_mitigation_stage`: `preflight` | `workspace_gen` | `execution`.
- `residual_open_risk`: `true` if the risk cannot be fully mitigated at the identified stage.

### Written Outputs

- `PREFLIGHT_ABSENCE_MAP.md`: Narrative absence map with ELS section.
- `PREFLIGHT_ABSENCE_MAP.json`: Structured payload per schema, including `els_risks[]`.

### Completion Condition (binary)

Phase 2 is COMPLETE when ALL of the following are true:
- Every `purpose_claim` from Phase 1 has at least one associated absence check (even if the result is "no gaps found").
- All six ELS categories are addressed (each with at least one entry or an explicit `not_applicable` with proof).
- Every identified absence is classified (`derivable` | `askable` | `deferrable` | `blocking`).
- No `blocking` absence remains without being escalated to `required_missing_inputs`.
- Both `.md` and `.json` artifacts are written to staging.

### Fail Conditions

- One or more `blocking` absences exist that cannot be resolved through derivation.
- The description lacks enough substance to even map absences meaningfully.

If Phase 2 fails due to `blocking` absences: write `PREFLIGHT_ABSENCE_MAP.json` with all identified absences. Write `PREFLIGHT_APPROVAL.json` with `status: insufficient_information` and `required_missing_inputs` listing the blocking items. The pipeline terminates.

### ELS Binary Gate

If `residual_open_risk: true` for ANY item under `payments_and_money_movement` or `privacy_and_data_governance`: Phase 5 cannot set status to `approved` UNLESS:
- Status is set to `insufficient_information`, OR
- User-explicit acceptance is recorded in `PREFLIGHT_DECISIONS.json` with `owner_of_decision: user_explicit`.

### What Phase 3 May Trust

- The absence map is comprehensive within the limits of the available description.
- ELS categories have been addressed — Phase 3 does not re-scan.
- `derivable` absences may be resolved by Phase 3 through architectural decisions (recorded in decisions).
- `blocking` absences, if any survived, have already terminated the pipeline.

---

## Phase 3: Minimal-Inevitable Architecture

### Objective

Define the smallest set of architectural components that satisfies ALL purpose claims while respecting ALL constraints from Phases 1-2. Nothing speculative. Nothing optional. Only what is inevitable given the approved purpose.

### Required Inputs

- `PREFLIGHT_PURPOSE.json` (Phase 1)
- `PREFLIGHT_ABSENCE_MAP.json` (Phase 2)

### Process

1. Read Phase 1 and Phase 2 outputs.
2. For each `purpose_claim`, determine the minimum architectural components required to satisfy it.
3. Merge overlapping components — if two claims require the same component, it appears once.
4. For each component in the minimal set:
   - State why it is inevitable (which purpose claims require it).
   - State what happens if it is removed (which claims break).
   - Classify as `core` (required for any purpose claim) or `supporting` (required for integration/operation).
5. Define the `non_goals` list: components or capabilities explicitly excluded from the minimal set, with justification for each exclusion.
6. Produce the acceptance criteria package (see below).
7. Record any architectural decisions made in this phase in `PREFLIGHT_DECISIONS.json`.

### Acceptance Criteria Packaging

Define acceptance criteria that become normative for later execution:

- Each criterion has a stable `acceptance_id` (format: `AC-NNN`).
- Each criterion is objectively verifiable: pass/fail, not subjective.
- Subjective checks ("looks good", "feels responsive", "seems accessible") are forbidden. Replace with measurable proxies:
  - "Routes exist and return 200" instead of "navigation works"
  - "Form submits data and returns confirmation" instead of "form looks right"
  - "Error states render for invalid input" instead of "errors are handled"
  - "Auth gate returns 401 for unauthenticated requests" instead of "auth is secure"
- Each criterion maps to at least one `purpose_claim` via `purpose_claim_refs[]`.
- `non_goals` are listed: capabilities explicitly excluded from acceptance.

**Minimum count rule:** `N >= max(5, ceil(number_of_purpose_claims * 2))`. If this minimum cannot be met, Phase 3 fails.

**UI quality rule:** If any criterion references UI quality, it must specify measurable proxies (routes exist, forms submit, error states render, auth gates enforce). Exception: projects explicitly marked as non-UI in CRI.

### Written Outputs

- `PREFLIGHT_ARCHITECTURE.md`: Narrative architecture with minimal-inevitable set and justifications.
- `PREFLIGHT_ARCHITECTURE.json`: Structured payload per schema.
- `PREFLIGHT_ACCEPTANCE.md`: Narrative acceptance criteria with mappings.
- `PREFLIGHT_ACCEPTANCE.json`: Structured payload per schema.

### Completion Condition (binary)

Phase 3 is COMPLETE when ALL of the following are true:
- Every `purpose_claim` is satisfied by at least one component in the minimal-inevitable set.
- Every component has a justification (which claims require it, what breaks without it).
- `non_goals` list is populated (at least one exclusion, even if obvious).
- Acceptance criteria count meets minimum: `N >= max(5, ceil(purpose_claims * 2))`.
- Every acceptance criterion is objectively verifiable (no subjective language).
- Every acceptance criterion maps to at least one `purpose_claim`.
- All four artifacts (`.md` and `.json` for architecture and acceptance) are written to staging.

### Fail Conditions

- A `purpose_claim` cannot be satisfied by any conceivable minimal component.
- Acceptance criteria minimum cannot be met even with generous interpretation.
- Two purpose claims require mutually exclusive architectural components with no resolution.

If Phase 3 fails: write artifacts with the failure documented. Write `PREFLIGHT_APPROVAL.json` with `status: rejected` and `rejection_reasons`. The pipeline terminates.

### What Phase 4 May Trust

- The minimal-inevitable set is the proposed architecture — Phase 4 challenges it but does not redesign from scratch.
- Acceptance criteria are proposed — Phase 4 may flag criteria that are insufficient but does not rewrite them.
- Component justifications are available for challenge.

### What Remains Provisional

- The minimal-inevitable set is provisional until it survives Phase 4 challenge.
- Acceptance criteria are provisional until Phase 4 confirms they are testable and sufficient.

---

## Phase 4: Skeptical Challenge

### Objective

Challenge every architectural commitment from Phase 3. For each component in the minimal-inevitable set, demand justification. For each exclusion, demand proof it is safe to exclude. Surface decisions that carry high reversal cost. Record all decisions formally.

### Required Inputs

- `PREFLIGHT_PURPOSE.json` (Phase 1)
- `PREFLIGHT_ABSENCE_MAP.json` (Phase 2)
- `PREFLIGHT_ARCHITECTURE.json` (Phase 3)
- `PREFLIGHT_ACCEPTANCE.json` (Phase 3)

### Process

1. Read all prior phase outputs.
2. For each component in the minimal-inevitable set:
   - Challenge: "Is this truly inevitable, or merely conventional?"
   - Challenge: "Could the purpose claims be satisfied without this component?"
   - Challenge: "Does this component introduce complexity disproportionate to its purpose?"
3. For each exclusion in `non_goals`:
   - Challenge: "Is this exclusion safe, or does it create a latent risk?"
   - Challenge: "Will a user reasonably expect this capability?"
4. For each ELS risk with `residual_open_risk: true`:
   - Challenge: "Is the mitigation plan sufficient, or is the risk being minimized?"
5. Produce decision records for every significant architectural commitment.

### Decision Record Requirements

For each major architectural commitment, record:

- `decision_id`: Stable identifier (format: `DEC-NNN`).
- `decision_statement`: One sentence, testable (e.g., "The system uses PostgreSQL as the primary datastore").
- `alternatives_considered`: At least two real alternatives (not strawmen). Each must be a genuinely viable option.
- `rejection_rationale_per_alternative`: Specific, causal reason for rejecting each alternative. Not "it's worse" — why specifically.
- `selected_rationale`: Why the chosen option is correct, tied to `purpose_claims` and `minimal_inevitable_set`.
- `reversibility_cost_if_wrong`: `low` | `medium` | `high` with a concrete reason (e.g., "high: requires full data migration and schema rewrite").
- `owner_of_decision`: `user_explicit` | `inferred_high_confidence` | `inferred_low_confidence`.

### Challenge-Loop Rule

**One challenge pass only.** Phase 4 performs exactly one challenge pass over Phase 3 outputs.

- Items that survive challenge: confirmed and recorded in decisions.
- Items that fail challenge: recorded as `open_risks` or adjusted in the architecture (adjustment recorded in decisions with rationale).
- Unresolved items: carried forward as `known_unknowns` with explicit `open_risks` entries into Phase 5.

**No iteration between Phase 3 and Phase 4.** The cost of one thorough challenge pass is lower than unbounded iteration. The architecture at this stage is minimal-inevitable, not optimal — further iteration optimizes prematurely. If the challenge reveals fundamental flaws, the correct response is `rejected`, not more iteration.

### Decision Record Binary Gate

Phase 5 CANNOT approve if:
- Any decision has `reversibility_cost_if_wrong: high` AND `owner_of_decision` is NOT `user_explicit`, UNLESS there is a recorded `known_unknowns` entry with a mitigation plan tied to that `decision_id`.

### Written Outputs

- `PREFLIGHT_CHALLENGE.md`: Narrative challenge results, organized by component.
- `PREFLIGHT_CHALLENGE.json`: Structured payload per schema.
- `PREFLIGHT_DECISIONS.md`: Narrative decision record with rationales.
- `PREFLIGHT_DECISIONS.json`: Structured payload per schema, array of decision records.

### Completion Condition (binary)

Phase 4 is COMPLETE when ALL of the following are true:
- Every component in the minimal-inevitable set has been challenged.
- Every exclusion in `non_goals` has been challenged.
- Every ELS risk with `residual_open_risk: true` has been challenged.
- Every significant architectural commitment has a decision record.
- Every decision record has `alternatives_considered` with at least two entries.
- The decision record binary gate is satisfiable (no ungated high-risk decisions).
- All four artifacts are written to staging.

### Fail Conditions

- The challenge reveals a fundamental flaw that cannot be resolved by adjusting the minimal set — the purpose itself is incoherent.
- A high-reversibility-cost decision has `owner_of_decision: inferred_low_confidence` and no mitigation plan exists.

If Phase 4 reveals fundamental flaws: record the flaws in challenge artifacts. Write `PREFLIGHT_APPROVAL.json` with `status: rejected` and `rejection_reasons`. The pipeline terminates.

### What Phase 5 May Trust

- Components that survived challenge are confirmed.
- Decision records are complete and gated.
- Open risks are explicitly documented with mitigation plans where available.

### What Remains Provisional

- Nothing is provisional after Phase 4. All architectural commitments are either confirmed, adjusted, or flagged as open risks.

---

## Phase 5: Approval Synthesis

### Objective

Synthesize all phase outputs into a final approval determination. Verify all binary gates from prior phases. Produce the approval artifact that gates workspace generation.

### Required Inputs

- All artifacts from Phases 1-4.

### Process

1. Verify Phase 1 gate: All CRI fields populated, at least one purpose claim.
2. Verify Phase 2 gate: All six ELS categories addressed.
3. Verify Phase 2 ELS gate: No `residual_open_risk: true` under `payments_and_money_movement` or `privacy_and_data_governance` without user-explicit acceptance or `insufficient_information` status.
4. Verify Phase 3 gate: Acceptance criteria count meets minimum.
5. Verify Phase 4 decision gate: No ungated high-risk decisions.
6. Verify CRI monetization gate: If `monetization_model: unknown` for a clearly for-profit intent, status must be `insufficient_information` unless explicitly excluded via `non_goals` with user-explicit acknowledgment.
7. Compile `approval_basis`: the set of evidence supporting the determination.
8. Compile `open_risks`: risks acknowledged but accepted.
9. Compile `non_goals`: capabilities explicitly excluded.
10. Determine status: `approved` | `rejected` | `insufficient_information`.
11. If `approved`: produce `PREFLIGHT_BUILD_ORDER.md` with recommended execution sequencing.

### Status Determination Rules

**`approved`** when:
- All Phase 1-4 binary gates pass.
- `approval_basis` is non-empty.
- No blocking absences remain.
- All CRI constraints are satisfied or explicitly deferred with user acceptance.
- The minimal-inevitable set survived challenge.

**`rejected`** when:
- Any phase produced irreconcilable contradictions.
- The purpose is incoherent or internally contradictory.
- A mandatory architectural component is impossible given stated constraints.
- Challenge revealed fundamental flaws with no resolution path.

**`insufficient_information`** when:
- Blocking absences remain that require user input.
- CRI fields cannot be populated from the available description.
- `monetization_model: unknown` for clearly for-profit intent without explicit exclusion.
- ELS risks under `payments_and_money_movement` or `privacy_and_data_governance` have `residual_open_risk: true` without user-explicit acceptance.

### Written Outputs

- `PREFLIGHT_APPROVAL.md`: Narrative synthesis with determination rationale.
- `PREFLIGHT_APPROVAL.json`: Structured payload per schema. Must include:
  - `status`: `approved` | `rejected` | `insufficient_information`
  - `approval_basis`: Non-empty array of evidence strings (if approved).
  - `rejection_reasons`: Array of specific reasons (if rejected).
  - `required_missing_inputs`: Array of missing items (if insufficient_information).
  - `open_risks`: Array of acknowledged risks.
  - `non_goals`: Array of excluded capabilities.
  - `minimal_inevitable_set`: Array of confirmed architectural components.
  - `allowed_next_step`: `workspace_generation` | `rerun_preflight` | `user_input_required` | `project_cancelled`.
- `PREFLIGHT_BUILD_ORDER.md` (only if approved): Recommended build order based on architectural dependencies, component criticality, and risk mitigation priority.

### Completion Condition (binary)

Phase 5 is COMPLETE when ALL of the following are true:
- All prior phase gates have been explicitly verified (not assumed).
- `status` is one of the three valid values.
- If `approved`: `approval_basis` is non-empty and `allowed_next_step` is `workspace_generation`.
- If `rejected`: `rejection_reasons` is non-empty and `allowed_next_step` is `rerun_preflight` or `project_cancelled`.
- If `insufficient_information`: `required_missing_inputs` is non-empty and `allowed_next_step` is `user_input_required`.
- Both `.md` and `.json` artifacts are written to staging.
- `PREFLIGHT_BUILD_ORDER.md` exists if and only if status is `approved`.

### Fail Conditions

Phase 5 itself does not fail — it produces one of three valid statuses. If the synthesis process encounters an internal inconsistency (e.g., all gates pass but no approval basis can be stated), this indicates a bug in a prior phase. In this case, set `status: rejected` with `rejection_reasons` describing the internal inconsistency.

---

## Git, Retention, and Immutability Rules

### Gitignore

`v2/.buildr/` SHOULD be added to `.gitignore` by default. It is a runtime staging area.

**Exception for audit trails:** If the team requires reproducible evidence of preflight decisions, the following files MAY be committed:
- `PREFLIGHT_APPROVAL.json`
- `PREFLIGHT_DECISIONS.json`
- `PREFLIGHT_ACCEPTANCE.json`

This is a team-level decision, not a system default. The default is gitignored.

### Retention

- **Reruns for the same slug (non-approved):** Overwrite all existing artifacts in the directory.
- **Reruns for a slug with approved artifacts:** Create a new directory with timestamp suffix per collision handling rules. The original approved artifacts are preserved.
- **Abandoned runs:** Cleaned up on next run for the same slug (overwrite rule applies). No automatic cleanup otherwise.

### Immutability

- **After `status: approved`:** All artifacts in the staging directory are immutable. They may not be modified unless preflight is explicitly reopened (new run with a new timestamped slug, or user-triggered reopen).
- **Reopening preflight:** Requires explicit user action. Creates a new run. The previous approved artifacts are preserved under their original slug (or timestamped variant).
- **After `status: rejected` or `insufficient_information`:** Artifacts are mutable — they will be overwritten on the next run for the same slug.

---

## Canonical Reference

- **Execution procedure:** This file (`SKILL.md`).
- **Machine-readable contract:** `references/preflight-handoff.schema.json`.
- **Phase depth and anti-patterns:** `references/phases.md`.
- **Contract explanations:** `references/contracts.md`.
- **Approval semantics:** `references/approval.md`.
- **System placement justification:** `references/architecture.md`.
- **Operator integration:** `references/integration-with-operator.md`.
- **Ground repository backlog (schemas, validation, ingest, vault, docs):** `../../improve.md` (repo path `v2/improve.md`). Optional; run after v2 files exist — does not change preflight procedure.

`SKILL.md` is authoritative for procedure. The schema is authoritative for payload structure. Reference files provide depth and justification but do not override either.
