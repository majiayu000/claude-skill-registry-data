---
name: ui-spec-reconcile
description: Reconcile a UI spec package with the current implementation after code fixes or redline audits. This skill ensures the specification remains the source of truth by incorporating resolved defects, confirmed implementation details, and approved design decisions back into the spec files.
status: draft
---

# UI Spec Reconcile

A skill for synchronizing an existing UI spec package with the actual state of the implementation. Use this after a round of development, bug fixing, or redline audits to ensure that the documentation accurately reflects the intended (and implemented) reality.

## When to use this skill

Use this skill:
- After implementing fixes based on a `ui-redline` audit.
- When the implementation has evolved beyond the original spec and those changes are accepted as "target" behavior.
- To clear "stale" findings in a spec package after they have been addressed in code.
- To promote implementation-driven discoveries (e.g., edge cases found during coding) into the official specification.

## Core principles

1. **Spec as Source of Truth:** The goal is not to blindly copy code into the spec, but to update the spec so it correctly describes the *intended* state, using implementation as evidence of what is possible and verified.
2. **Conservative Updates:** Do not silently update the spec. Always propose changes first, especially if they represent a design decision rather than just a bug fix.
3. **Evidence-based:** Prefer `ui-redline` reports or `ui-inspector` reports as primary evidence for reconciliation.
4. **Distinguish Intent:** Clearly separate bug fixes (reconciling spec to intended state) from design changes (updating the intended state based on implementation reality).

## Reconciliation Rules

To prevent "canonizing" accidental implementation drift, follow these rules:

1. **Never promote implementation behavior to target spec unless:**
   - It resolves an accepted redline item.
   - It is explicitly approved by the user/product owner.
   - It is already required by an upstream product/UX contract.
2. **Flag Drift:** If the implementation differs from the spec but is NOT a verified fix, mark it as "Implementation Drift" in the report and ask for a product decision before updating the spec.
3. **Evidence Hierarchy:** A verified `ui-redline` fix is stronger evidence than raw source code.

## Workflow

### Step 1 — Gather Evidence

Identify the spec package to be reconciled and gather evidence. Search for all known redline/audit conventions:
- `redlines/redline-audit.md`
- `redlines/redline-report.md`
- `redlines/redline-*.md`
- `10-redline-report.md`
- `redlines/inspector-report.md`
- Direct source code inspection.

**Context:** Read the existing spec files (brief, blueprint, screen-spec, component-specs, microcopy, acceptance).

### Step 2 — Analyze Mismatches

Compare the implementation evidence against the current spec. Identify:
- **Resolved Items:** Redline findings that are now fixed in code and should be removed or marked as "Pass" in the spec/acceptance.
- **Implementation Drift:** Accepted changes in the UI that are not yet in the spec (e.g., a label changed during implementation for better clarity).
- **Stale Claims:** Statements in the spec that no longer apply to the implementation.

### Step 3 — Propose Reconciliation Plan

List every proposed change to the spec package. For each change, note:
- **File:** Which spec file is affected.
- **Change:** What exactly is being updated.
- **Reason:** Why this is being reconciled (e.g., "Matches verified fix for Redline Item #4").
- **Confidence:** High (verified by redline) or Low (inferred from code).

**Wait for user approval of the plan.**

### Step 4 — Apply Updates (Patch Mode)

If approved, update the spec files.
- Remove resolved defects from "Observed" sections.
- Update "Target" claims to match confirmed behavior.
- Update the `acceptance.md` checklist to reflect the new verified state.
- Update the `status` in the frontmatter if appropriate.

### Step 5 — Verify

Run `ui-spec-linter` on the updated package to ensure internal consistency.

## Output template

Produce a reconciliation report in the following format:

```markdown
# UI Spec Reconciliation Report: <scope>

## 1. Input Evidence
- Redline Audit: `redlines/redline-audit.md`
- Implementation: `src/components/...`

## 2. Reconciliation Summary
| Spec File | Changes Made | Resolved Items |
|---|---|---|
| `screen-spec.md` | Updated microcopy for primary action | #3, #5 |
| `component-specs/X.md` | Corrected accessibility role | #1 |
| `acceptance.md` | Marked 4 items as PASS | - |

## 3. Design Decisions Promoted
- [ ] List any implementation details that are now "canonical" design.

## 4. Remaining Gaps
- [ ] Items that could not be reconciled (e.g., pending product decision).

## 5. Result
**Status:** fully reconciled | target-only reconciled | implementation-only reconciled | partially reconciled | blocked by product decision

**Result Types:**
- **Fully reconciled:** Spec and implementation agree; no gaps remain.
- **Target-only reconciled:** Spec is stable and approved; implementation still awaits refactoring or completion.
- **Implementation-only reconciled:** Implementation state accepted as new target; spec has been updated to match.
- **Partially reconciled:** Some items resolved; others remain open (e.g., awaiting product decision).
- **Blocked by product decision:** Reconciliation cannot proceed until a product/UX decision is made.
```

## Acceptance criteria for this skill's output

- [ ] Every change to the spec is linked to evidence (redline, inspector, or code).
- [ ] Bug fixes are distinguished from intended design changes.
- [ ] `acceptance.md` is updated to reflect resolved items.
- [ ] Proposals are made before any edits are applied to the spec files.
- [ ] The report clearly states what was reconciled and what remains a gap.
