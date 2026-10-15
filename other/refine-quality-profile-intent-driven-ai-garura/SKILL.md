---
name: refine-quality-profile
description: Stage 2 skill of /arch. Reads the /specify quality profile, refines targets against architectural reality (inventory constraints, project-profile pins, epic constraints), and writes the refined quality profile to architecture/ with a delta log of every adjustment. The refined QP describes the NFRs physical must deliver; it does NOT name mechanisms.
version: 0.1.0
user-invocable: false
---

# refine-quality-profile

> **Decision Surfacing Discipline:** This skill emits a `decision-manifest-refine-quality-profile.yaml` alongside its primary artifact. Every refinement to a /specify QP target is recorded as a decision with tier, grounding source, recommendation, and alternatives. The orchestrator drives the tiered surfacing flow after this skill completes.

Called by `tech-designer` during `arch` Stage 2. Produces `quality-profile.yaml` at `{product_base}architecture/quality-profile.yaml` plus a decision manifest.

## Purpose

The /specify play authored a first-cut quality profile from product intent. /arch refines it against the architectural reality surfaced during Stages 1-2 — the systems chosen in inventory carry their own scale, reliability, and security ceilings; project-profile pins may set hard floors; epic constraints may demand stricter targets than the first-cut allowed for. This skill is the bridge.

The refined QP **describes** the NFRs the product must deliver. It does NOT name delivery mechanisms — those belong in physical-architecture. Same NFR, two views: this artifact is the target, physical is the mechanism.

Outputs always carry a `delta_log[]` recording every adjustment (field, before, after, rationale citing the architectural driver). Security characteristics ratchet UP only — any security-related adjustment where `after < before` is a structural violation. Adjustments without a cited architectural driver are blocking.

## Input

Receive from the `tech-designer` agent. All paths resolve against `{product_base}` and `{ltm_base}` supplied by the play via JSON contract.

- `specify_qp_path` (path, required) — `{product_base}specification/quality-profile.yaml`. When missing or DRAFT under C1 soft pre-flight, the play writes `{product_base}specification/quality-profile-stand-in.yaml` from user answers; this skill reads that instead.
- `scope_path` (path, required) — `{product_base}scope/scope.yaml`.
- `epics_dir` (path, required) — `{product_base}scope/epics/`. Per-epic constraints may force a stricter target than the /specify QP allowed for.
- `inventory_dir` (path, required) — `{product_base}architecture/systems-inventory/`. Each system file's Scale Profile and Tradeoffs sections may cap or force NFR targets.
- `project_profile_path` (path, required) — `{product_base}user-provided/project-profile.yaml`. `grounded_tools.nfr_floors[]` and security/compliance pins are authoritative.
- `kb_quality_dir` (path, required) — `{ltm_base}components/memory/knowledge/quality/`. ISO 25010 characteristic definitions and standard targets.
- `output_path` (string, required) — `{product_base}architecture/quality-profile.yaml`.
- `decision_manifest_path` (string, required) — `{product_base}architecture/decision-manifest-refine-quality-profile.yaml`.

## Output

### Refined quality profile

YAML at `{output_path}` mirroring the /specify QP structure (every ISO 25010 characteristic with relevance, target, rationale) PLUS top-level `refined_from` and `delta_log[]` blocks.

```yaml
refined_from:
  source_path: {product_base}specification/quality-profile.yaml
  source_sha: {sha256 at read time}
  refined_at: {ISO 8601 timestamp}

# ISO 25010 characteristics — same structure as /specify QP.
characteristics:
  functional_suitability:
    relevance: high | medium | low | not_applicable
    target: {prose target or quantified threshold}
    rationale: {why this level for this product}
  performance_efficiency:
    relevance: ...
    target: ...
    rationale: ...
  compatibility:
    ...
  interaction_capability:
    ...
  reliability:
    relevance: ...
    target: ...                # e.g. "99.9% monthly uptime; RTO 4h; RPO 15min"
    rationale: ...
  security:
    relevance: ...
    target: ...
    rationale: ...
  maintainability:
    ...
  flexibility:
    ...
  safety:
    ...

# Delta log — one entry per refinement made versus the /specify QP.
delta_log:
  - id: D-001
    characteristic: reliability               # ISO 25010 characteristic
    field: target                             # which field changed
    before: "99.99% monthly uptime"
    after: "99.9% monthly uptime"
    direction: tightened | loosened | clarified
    driver:                                   # MUST cite one architectural reality
      kind: inventory_constraint | project_profile_pin | epic_constraint | regulatory_pin
      reference: {inventory file path | profile slot | epic id | regulation cite}
    rationale: |
      {2-4 lines of prose explaining why the adjustment was made}
```

**Security ratchet rule.** For every delta where `characteristic = security`, `direction` MUST be `tightened` or `clarified`. A `loosened` security delta is a structural violation and halts the skill with `what_failed: security_ratchet_violation`.

### Decision manifest

One YAML file at `{decision_manifest_path}` with one entry per delta_log entry.

```yaml
manifest:
  skill: refine-quality-profile
  written_at: {ISO 8601 timestamp}
  decisions:
    - decision_id: RQP-001
      decision_type: target_refinement
      tier: high | mid | low
      grounding_source:
        kind: inventory_constraint | project_profile_pin | epic_constraint | regulatory_pin | agent_default_with_user_approval
        citation: {path or slot or cite}
      recommendation: {summarized adjustment, e.g. "tighten reliability target to 99.9% per Salesforce SLA"}
      alternatives_considered:
        - option: {alt target}
          why_rejected: {one line}
      agent_reasoning_summary: |
        {2-4 line prose}
      user_response: accept | override | orbit | pending
      user_response_detail: {free text — null when pending}
```

## Process

### 1. Read inputs

- Parse `specify_qp_path` (or stand-in). Capture its full structure as the baseline. Compute `source_sha`.
- Glob `epics_dir/*.yaml` → collect every per-epic constraint that names a quality dimension (performance budget, reliability, security level, compliance flag).
- Glob `inventory_dir/*.md` → collect every system's Scale Profile + Tradeoffs sections.
- Parse `project_profile_path` → `grounded_tools.nfr_floors[]`, security level pins, compliance flags.
- Read `kb_quality_dir` index for ISO 25010 characteristic definitions when reasoning about relevance.

### 2. Validate pre-conditions

- Required inputs exist OR documented stand-in exists.
- Output path's parent directory exists.

Missing required input with no stand-in → structured failure with `what_failed: missing_input`.

### 3. Establish the refined baseline

Copy every characteristic block from the /specify QP into the refined QP's `characteristics:` section verbatim. Set top-level `refined_from.source_path` and `refined_from.source_sha`. The refined QP starts as a byte-for-byte copy of the input — every divergence MUST be recorded as a delta_log entry.

### 4. Walk each characteristic against architectural reality

For each ISO 25010 characteristic, run these checks in order:

1. **Project-profile pin check.** If `project_profile.grounded_tools.nfr_floors[]` carries a pin for this characteristic, the pin sets a floor. If the /specify target is below the pin, force a tightening delta. If equal or above, no delta needed.

2. **Inventory constraint check.** For every system in inventory whose Scale Profile or Tradeoffs section names a hard ceiling that conflicts with the /specify target, propose a delta. Examples:
   - A chosen SaaS identity provider's published SLA caps reliability at 99.9% when /specify asked for 99.99% → propose `tightened: false, loosened: true` to align with the achievable ceiling, OR escalate (the choice of system may need to change).
   - A chosen analytics platform's data residency limitations contradict a compliance flag → propose tightening security/compliance or escalate.

3. **Epic constraint check.** For every epic whose constraints name a quality dimension stricter than the /specify QP target, propose a `tightened` delta with the epic ID as the driver.

4. **Regulatory pin check.** When `project_profile.compliance[]` lists regulations (HIPAA, PCI-DSS, SOC 2, GDPR) and the /specify target is below the regulatory floor for the relevant characteristic, force a `tightened` delta with the regulation as the driver.

A delta is proposed whenever any of these checks fires. Multiple checks may converge on the same characteristic — record each as a separate delta_log entry so traceability is preserved.

### 5. Apply each delta and write the log

For each proposed delta:

- Verify the security-ratchet rule (Step 4 may have surfaced a loosening proposal for security characteristic — that halts with `what_failed: security_ratchet_violation`).
- Update `characteristics.{characteristic}.target` and/or other fields per the delta.
- Append a delta_log entry with id, characteristic, field, before, after, direction, driver, rationale.
- Record a decision-manifest entry for the delta with tier resolution:
  - `tier: high` when grounding is a project-profile pin or regulatory pin (deterministic).
  - `tier: mid` when grounding is an inventory constraint with a published SLA / scale figure (sourced but agent-reasoned).
  - `tier: low` when grounding is agent reasoning over inventory Tradeoffs prose with no quantified source.

### 6. Loosening escalations

When a proposed delta is `loosened` (e.g., a system ceiling forces a relaxation of the /specify target):

- For non-security characteristics: surface at Stage 2 checkpoint per C19 tier. Loosening is a real adjustment but may be acceptable; the user decides.
- For security characteristics: halt with `what_failed: security_ratchet_violation`. The orchestrator surfaces the conflict — either the system choice changes (orbit to Stage 1) or the /specify target was wrong.

### 7. Write outputs

Write `{output_path}` with the full refined QP — every characteristic plus the delta_log. Write `{decision_manifest_path}` with one entry per delta. All `user_response` start as `pending`.

### 8. Validate output

- Every characteristic in the /specify QP appears in the refined QP with at least its `relevance` carried forward.
- Every delta_log entry has id, characteristic, field, before, after, direction, driver (with kind AND reference), and rationale (non-empty).
- No security delta has direction `loosened`.
- Refined QP names NO delivery mechanisms (regex check: rejects any phrase matching `delivered by`, `via {tool}`, `using {product}`, etc. — those are physical's concern).
- Decision manifest has one entry per delta.

Any failure → structured failure with `what_failed` and the offending block.

## Output Contract

On success:

```json
{
  "status": "success",
  "skill": "refine-quality-profile",
  "outputs": {
    "refined_qp_path": "{product_base}architecture/quality-profile.yaml",
    "decision_manifest_path": "{product_base}architecture/decision-manifest-refine-quality-profile.yaml",
    "delta_count": <int>,
    "tightenings": <int>,
    "loosenings": <int>,
    "clarifications": <int>,
    "halted_slots": [
      { "characteristic": "...", "reason": "loosening_pending_user_decision | security_ratchet_violation" }
    ]
  }
}
```

On failure:

```json
{
  "status": "failure",
  "skill": "refine-quality-profile",
  "what_failed": "missing_input | security_ratchet_violation | delivery_mechanism_named | delta_without_driver | manifest_incomplete",
  "details": "..."
}
```

## Evals

| Eval | Failure Bound | Check |
|------|---------------|-------|
| RQ-1 | F8 (NFR with no delivery mechanism — upstream check) | Every characteristic with `relevance != not_applicable` in the /specify QP appears in the refined QP. |
| RQ-2 | F12 (QP delta uncited) | Every entry in `delta_log[]` has field, before, after, direction, driver.kind, driver.reference, and rationale, all non-empty. |
| RQ-3 | C6 — security ratchet | No delta_log entry has `characteristic: security` AND `direction: loosened`. |
| RQ-4 | Skill purity | Refined QP body contains no text matching `delivered by`, `via {tool}`, or named product/runtime tokens (delivery mechanism leakage). |
| RQ-5 | F16 (manifest missing/malformed) | Decision manifest exists with one entry per delta; every entry has decision_id, decision_type, tier, grounding_source, recommendation, alternatives_considered. |
| RQ-6 | C16 (KB read-only) | The skill wrote NO file under `kb_quality_dir`. |
| RQ-7 | F13 (source_type discipline) | No decision has `grounding_source.kind: agent_default_unilateral`. |

## Constraints

- Writes ONLY to `{output_path}` and `{decision_manifest_path}`. Read-only on every input.
- NEVER names a delivery mechanism in the refined QP — physical owns that.
- Security characteristics ratchet UP only. Loosening security is a structural violation.
- Every delta cites an architectural driver (inventory constraint, project-profile pin, epic constraint, or regulatory pin). Agent reasoning alone is not a driver; it must reference one of the four kinds.
- The skill NEVER modifies the /specify QP at `{product_base}specification/quality-profile.yaml` — that file is the authored intake and stays unmodified.

## Failure modes

- `missing_input` — a required input path is absent and no stand-in exists.
- `security_ratchet_violation` — a delta with `characteristic: security` has `direction: loosened`.
- `delivery_mechanism_named` — the refined QP body contains text naming a delivery mechanism.
- `delta_without_driver` — a delta_log entry has no `driver.kind` or no `driver.reference`.
- `manifest_incomplete` — the decision manifest is missing or any entry lacks required fields.
