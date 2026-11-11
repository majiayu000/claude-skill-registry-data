---
name: pair-capability-map-subdomains
description: "Classifies business capabilities into DDD subdomains (core, supporting, generic) with a volatility rating, scoped to items just touched. Composed by /pair-process-refine-story, /pair-process-plan-initiatives, /pair-process-plan-epics, /pair-process-brainstorm; full-scope re-mapping only via /pair-process-bootstrap."
version: 0.6.0
author: Foomakers
---

# /pair-capability-map-subdomains — Subdomain Placement (Capability)

Classify business capabilities into Domain-Driven Design subdomains — core, supporting, or generic — and place them with a Volatility rating. A **capability**, not a standalone lifecycle step: always invoked scoped to the items the caller just touched, never as a full re-mapping outside `/pair-process-bootstrap`.

## Process Profile

<!-- process-step: id=define-subdomains -->

Executable form of the **`define-subdomains`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; under `$approval: auto` there is nobody to answer, so the run **HALTs**. <!-- approval-round: kind=gate; auto=halt -->

A **composed** invocation never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Arguments

| Argument | Required | Description                                                                                                                              |
| -------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `$scope` | Yes      | Items/areas touched by the caller (e.g. capability names, PRD sections, an initiative). `all` — full re-mapping, allowed only when composed by `/pair-process-bootstrap`. |
| `$approval` | No    | Approval-round mode: `interactive` (default — the Step 3 round runs as written) or `auto` (ask nothing: the proposed placement is accepted as-is, a **conflict** keeps the existing entry, and both are reported). See [approval rounds](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/approval-rounds.md). |

## Composed Skills

| Caller              | When                                                             |
| ------------------- | ----------------------------------------------------------------- |
| `/pair-process-refine-story`     | Functional/domain analysis phase — placement for the story's capability. |
| `/pair-process-plan-initiatives` | Domain placement for a new initiative's capability area.          |
| `/pair-process-plan-epics`       | Domain placement for an epic's capability area.                   |
| `/pair-process-brainstorm`       | Broad/functional discovery (phase 2) touching multiple capabilities. |
| `/pair-process-bootstrap`        | Initial full-catalog mapping — the only caller allowed `$scope: all`. |

Invocable independently with an explicit `$scope` for ad hoc placement.

## Algorithm

### Step 0: Resolve Scope and DDD Adoption State

1. **Check**: Does [`adoption/product/subdomain/`](../../../.pair/adoption/product/subdomain) contain `.md` files beyond README.md (DDD already adopted)?
2. **Check**: If not adopted, are PRD and initiatives available (business context to classify from)?
   - PRD: [`.pair/adoption/product/PRD.md`](../../../.pair/adoption/product/PRD.md)
   - Initiatives: query PM tool or check adoption files
3. **Act**: Resolve the working mode:
   - **DDD mode** — subdomain catalog exists, or PRD + initiatives are available for classification.
   - **System-areas fallback** — no subdomain catalog AND no PRD/initiatives. No DDD prerequisite is enforced; do not HALT. Proceed to Step 1 in fallback mode.
4. **Check**: Does `$scope` resolve to any item in the current context?
5. **Skip**: If `$scope` resolves to nothing → report "no domain impact" and return control to the caller. No file changes.
6. **Verify**: Mode and non-empty scope determined.

### Step 1: Detect Existing Subdomains

1. **Check**: Scan [`adoption/product/subdomain/`](../../../.pair/adoption/product/subdomain) for existing `.md` files (excluding README.md).
2. **Act**: Build a registry of existing subdomains:

   ```text
   EXISTING SUBDOMAINS:
   ├── [filename.md]: [Title] (Classification: [Core/Supporting/Generic], Volatility: [High/Medium/Low])
   └── ...
   ```

3. **Verify**: Registry built. Only entries touched by `$scope` are candidates for creation/update; the rest are left untouched.

### Step 2: Business Capability Analysis (DDD mode)

_Skip if in system-areas fallback — go to Step 2b._

1. **Act**: Analyze the capabilities in `$scope` (or the full PRD/initiatives set when `$scope: all`, bootstrap only):
   - Extract business function from PRD objectives and value propositions.
   - Map the touched initiative(s)/epic(s)/story to a business capability area.
   - Identify cross-cutting concerns and shared functionality patterns relevant to the scope.
2. **Verify**: Business capabilities in scope identified.

### Step 2b: System-Areas Fallback (no-DDD projects)

1. **Act**: Instead of business-capability analysis, derive placement from the codebase's existing structure: top-level packages/apps/services/modules touched by `$scope`.
2. **Act**: Treat each system area as a placeholder subdomain with `Classification: Generic` and `Volatility: Low` unless the caller has clear evidence otherwise — these are provisional, not a DDD classification.
3. **Verify**: Placement resolved to system area(s). Note in output that this is a fallback, not a DDD classification, and that `/pair-process-bootstrap` or a full `/pair-capability-map-subdomains` run can upgrade it later.

### Step 3: DDD Classification, Volatility & Catalog Delta

_Skip if in system-areas fallback — the Classification/Volatility already assigned in Step 2b (Generic/Low unless the caller has clear evidence otherwise) is final for this run; go straight to Step 4._

1. **Act** (DDD mode): Classify each in-scope capability:
   - **Core** — competitive advantage, high business value, high complexity. Build in-house, invest deeply. Default `Volatility: High`.
   - **Supporting** — operational necessity, medium value. Important but not differentiating. Default `Volatility: Medium`.
   - **Generic** — commodity function, low differentiation. Buy or use standard solutions. Default `Volatility: Low`. Additionally assess **implementation volatility** — the probability of switching provider/technology; when High, note that relationships toward this subdomain require an integration contract (feeds `/pair-capability-map-contexts` strength assessment).
2. **Act**: Volatility default follows the classification above; the developer may override it (business-domain judgment, never inferred from commit history alone).
3. **Act**: Map relationships and data flow between in-scope subdomains and their existing dependencies.
4. **Check**: Does an in-scope subdomain already exist in the registry with a different classification, or a different Volatility that was **not** recorded as a human override? Compare against the existing file's recorded values, not a freshly-recomputed classification-derived default — a Volatility that already carries an override reason is never treated as conflicting with that same default recomputed again; only a change to classification, or an explicit new override request, is a conflict.
5. **Act**: If a conflict exists → propose the delta only (not a full re-map):

   > Existing: `[Name]` — Classification: [X], Volatility: [Y]
   > Proposed: Classification: [X'], Volatility: [Y']
   > Approve delta, keep existing, or override? <!-- approval-round: kind=keep-or-redo; auto=keep -->

   Under `$approval: auto` this question is not asked and the **existing entry is kept** — the conservative branch it already offers. The unapplied delta is reported (Output Format) so nothing is lost; overwriting a recorded classification nobody was asked about is the one outcome `auto` must not produce.

6. **Act**: Present the scoped catalog delta to the developer (`$approval: interactive`; under `auto` it is reported in the Output Format instead of asked):

   > Proposed subdomain placement (scope: [$scope]):
   > **[Classification]**: [Name] — Volatility: [Level] ([default | override: reason])
   >
   > Relationships: [key dependencies within scope]
   > Approve or adjust? <!-- approval-round: kind=confirm; auto=accept -->

7. **Verify** (`$approval: interactive`): Developer approves the delta. Under `auto` the delta is accepted as-is (already reported in item 6) and Step 4 writes it — except a conflict from item 5, which stays unapplied. <!-- approval-round: kind=confirm; auto=accept -->

### Step 4: Subdomain Specification

For each approved subdomain in scope:

1. **Check**: Does this subdomain already exist as a file?
2. **Act**: If exists and no conflict was raised → leave untouched; pre-existing entries without a `Volatility` field remain valid as-is (no forced migration — the field is added the next time this entry falls inside a `$scope`).
3. **Act**: If new, or an approved delta applies → create/update the subdomain file following [subdomain-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/subdomain-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)):
   - Fill all template sections: Classification, Volatility, Business Purpose, Key Capabilities, Strategic Importance, Complexity Assessment, Data Ownership, Dependencies, Team Recommendations, Implementation Priority.
   - File path: `adoption/product/subdomain/[kebab-case-name].md`
4. **Verify**: File created/updated and parseable. Entries outside `$scope` are untouched.

### Step 5: Update Catalog README

1. **Act**: Update [`adoption/product/subdomain/README.md`](../../../.pair/adoption/product/subdomain/README.md) for the entries touched by this run:
   - List all subdomains by classification (Core, Supporting, Generic), with Volatility.
   - Include links to individual files.
   - Update the Subdomain Relationship Matrix for affected entries only.
2. **Verify**: README reflects the current catalog.

## Output Format

```text
SUBDOMAIN PLACEMENT COMPLETE:
├── Scope:      [$scope]
├── Mode:       [DDD | System-areas fallback]
├── Touched:    [N subdomains]
├── Created:    [X new files]
├── Updated:    [Y existing files]
├── Volatility: [defaults applied: A, overridden: B]
├── Approval:   [interactive — approved | auto — accepted as-is, C conflict(s) kept unapplied]
├── Location:   adoption/product/subdomain/
└── Next:       /map-contexts (scoped to the same items)
```

The `Next:` line names only steps enabled by the project's [process profile](../../../.pair/knowledge/guidelines/technical-standards/ai-development/process-profiles.md): a disabled one is dropped, and when none is left the line names no skill.

## Edge Cases and Error Handling

- **Scope resolves to nothing** — report "no domain impact", caller proceeds without HALT.
- **Existing catalog conflicts with scoped update** — always propose the delta and require human approval before writing (idempotent behavior preserved). Under `$approval: auto` the write does not happen either: the existing entry is kept and the delta is reported unapplied (Step 3 item 5). <!-- approval-round: kind=keep-or-redo; auto=keep -->
- **Pre-existing files without `Volatility`** — treated as valid; field is added only when that entry falls inside a future `$scope`.
- **No `subdomain/` or `boundedcontext/` artifacts at all** — system-areas fallback (Step 2b); no error, no DDD prerequisite.
- **`$scope: all` requested by a caller other than `/pair-process-bootstrap`** — warn and downgrade to the caller's actual touched items; full re-mapping stays bootstrap-only.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (adoption/context inputs missing → warn, proceed with what's available rather than halting) for the standard scenarios. Additional cases:

- If initiatives are not available but PRD is, proceed with PRD-only analysis and warn.
- If neither PRD nor initiatives nor an existing catalog are available, use the system-areas fallback (Step 2b) rather than halting.
- If the adoption directory doesn't exist, create it.
- If README.md doesn't exist, create it from scratch.

## Notes

- This skill **creates/updates adoption files** — not PM tool issues. Subdomains are design artifacts.
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). This skill's check: detects existing files by filename; only entries inside `$scope` are evaluated for changes.
- Volatility is evaluated from the business domain (classification-derived default + human override), never from commit history alone.
- DDD classification and Volatility drive downstream assessments — see `/pair-capability-map-contexts` (relationship strength/distance/volatility) and the architecture-quality capability that consumes them.
- Migration: this skill was reclassified from a process skill (`process/map-subdomains`) to a capability (`capability/map-subdomains`) — see [skills-guide.md](../../../.pair/knowledge/skills-guide.md#migration-notes) for the rename and new invocation paths.
