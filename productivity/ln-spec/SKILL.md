---
name: ln-spec
description: "Crystallize shared understanding into a reviewable spec, or update an existing one. Use when the problem needs a written specification, when assumptions or decisions have changed, or when the user says 'write a spec'."
argument-hint: "[feature or problem to specify]"
---

# Ln Spec

Crystallize understanding into a **spec** — the reviewable decision record between shared agreement and actionable plan. Every section should close a decision; a spec that restates the conversation instead of narrowing the solution space has failed.

`memory/SPEC.md` plus `memory/PLAN.md` are the only canonical planning state. Do not spin up sidecar specs, decision logs, or assumption ledgers without explicit permission.

Skip steps that are unnecessary (e.g. already covered by prior skills in this session). This is not a checklist — it is a workflow.

## Input

The feature or problem: $ARGUMENTS

## Procedure

**Mode detection.** If the user provides a specific finding, research result, or decision to record — not a new feature area — this is a **patch**, not a full pass. Skip to step 5.

1. **Capture the problem** from the user's perspective — what they want and *why*. The *why* shapes the solution space.
2. **Explore the codebase** to verify assertions, understand current state, and find existing patterns. If `memory/SPEC.md` exists, read it first — this is an update, not a blank-slate write.
3. **Interview** (if understanding is thin), to close remaining gaps. Walk each branch of the design tree. For each question, provide your recommended answer. If the codebase can answer a question, explore it instead of asking. Use `ln-grill` if it hasn't already been run.
4. **Sketch modules** to build or modify. Apply Ousterhout's depth test — favor deep modules with small interfaces and large hidden implementations, testable in isolation. Check with the user that modules match expectations. Use `ln-design` if it hasn't already been run.
5. **Write or update** `memory/SPEC.md`.

## Output

Write or update `memory/SPEC.md` following the [spec template](assets/spec-template.md). If the file already exists, read it first — preserve existing content, evolve sections that need change.

### Identifier scheme

Before adding any new cross-referenceable item, derive the session's author suffix from the local user name: take `basename "$HOME"`, then uppercase its first character. Example: `/Users/lunelson` → `L`. Append this suffix to every new item identifier: `A47-L`, `D12-L`, `I47-L`, etc.

When assigning the numeric part for a new item:

1. Scan existing identifiers with the same prefix (`A`, `D`, `I`, requirement/oracle prefixes if present).
2. Compute the next number from legacy unsuffixed IDs plus IDs with the same author suffix.
3. Ignore IDs with other author suffixes for incrementing, so parallel sessions can safely produce `I47-L` and `I47-K`.
4. Do not rename or renumber existing IDs just to add a suffix; only preserve and update them unless a deliberate cleanup is requested.
5. Use the full suffixed ID in every cross-reference (`Depends on: D12-L`, `Proves: R3-L / D8-L`).

If `$HOME` is unavailable or the basename is empty, ask the user for the suffix instead of inventing one.

### SPEC shape

Use the mature SPEC shape unless the existing project clearly predates it and the user only asked for a narrow patch:

- **Product Contract** — concept, constraints / non-goals, grouped capability requirements.
- **Live Architecture Register** — open assumptions, active decisions, critical invariants.
- **Future Direction Register** — directional bets that shape sequencing but are not current product contract.
- Compact model / architecture sections only when they still serve as SPEC authority.
- Lexicon and Verification Design.

SPEC is a live register, not an archive. Keep stable product contract separate from live architectural uncertainty and future direction. Prefer short guardrails plus links to PLAN/design docs over long design-doc-scale prose.

### Verification Design boundary

ln-spec owns the **inner loop** of verification design: verification commands, verification policy, and inner-loop oracle items (type checks, fast unit tests, linting). Middle and outer loop oracle strategy, diagnostic assessment, and blind spots are owned by `ln-oracles`. Not every scoped slice requires a full oracle-design pass, but frontier items or slices involving LLM behavior, visual rendering, or compositional/system-level claims should route through `ln-oracles` before implementation. When writing or updating §Verification Design, preserve any content written by ln-oracles (§Verification Stance, §Diagnostic Assessment, §Oracle Strategy middle/outer tiers, §Design notes, §Acknowledged Blind Spots).

### Traceability

If `memory/PLAN.md` exists, verify that changed requirements, assumptions, decisions, and invariants still align with affected frontier items. If it does not exist yet, close the reference chain as far as current artifacts allow: assumptions should still name dependent decisions and validation approaches, and frontier links can be added later by `ln-plan`.

### Weight management

Use the same unit-of-record rules as `ln-build` §Same-item tests. Before adding a row, compare against nearby items in the same feature area. Prefer **update**, **merge**, or **omit** over **add** when the seam is the same.

**Units of record:**

- **Requirement** = stable product capability or externally observable contract.
- **Assumption** = one unresolved question at one seam that still shapes work.
- **Decision** = one committed spine choice between alternatives at one seam.
- **Invariant** = one seam-level structural property protected by tests or an explicit planned oracle.
- **Future direction** = a directional bet that influences sequencing but is not yet product contract.

**Validated assumptions retire by default.** If evidence settles an assumption, do not leave it live just as history. Either remove it during `ln-sync`, or promote the durable residue into Product Contract, Active Decisions, Critical Invariants, Lexicon, or PLAN traceability if it still constrains active work.

**These are not new rows** — they are updates, merges, links, or no-ops:
- confidence changes, validation narratives, added evidence
- helper names, file layout, or implementation mechanics
- one more branch/state/kind/phase/action example of an existing rule
- one implementation step under an already-recorded decision
- detailed rationale better held by a design doc
- future acceptance criteria better held by PLAN until the work is active

**Smell checks before adding:**
- The sentence starts with "for this slice" or names a temporary cutover step → probably an update, not a new item
- The difference is only approve/reject, confirm/force-close, or kind/phase/state variants of one shared rule → merge into the seam-level row
- The item would stop making sense once the code ships and no alternative remains live → probably not a tracked decision
- The item is an implementation mechanic inside an already-chosen boundary → no-op
- The row mainly names test files or records implementation history → probably belongs in code/tests or should merge into a broader invariant

Large cleanup is `ln-sync` work. When writing or patching, keep the touched area coherent; do not attempt a risky whole-document consolidation.

### Cross-reference integrity

Every amendment must close its reference chain as far as the current lifecycle stage allows. After editing, verify:

- **New requirement** → has: product capability area and PLAN/frontier references if it changes upcoming work
- **New assumption** → has: suffixed identifier, dependent decision(s) or invariant(s), validation approach, and implicated frontier item(s) in `memory/PLAN.md` **if `memory/PLAN.md` already exists**
- **New decision** → has: suffixed identifier, dependent assumption(s) where relevant, supersession note, and enough rationale to identify the chosen seam
- **New invariant** → has: suffixed identifier, establishing frontier item in `memory/PLAN.md` **if known** (or scoped slice if already defined), protecting test/oracle (or `planned` / `manual (outer loop)`), proved decision or requirement
- **New future direction** → has: PLAN frontier/horizon pointer or design-doc pointer; not full acceptance detail unless already active
- **New constraint** → has: rationale for exclusion
- **New inner-loop oracle item** → names the invariant(s) it protects

## Routing

After filing the spec, present these options to the user (use `tool-ask-question`):

| #   | Label            | Target        | Why                                               |
| --- | ---------------- | ------------- | ------------------------------------------------- |
| 1   | Plan frontier    | `ln-plan`     | Spec is complete, break it into frontier items    |
| 2   | Design oracles   | `ln-oracles`  | Spec needs middle/outer loop verification design  |
| 3   | Grill it more    | `ln-grill`    | Spec has gaps that need deeper understanding      |
| 4   | Back to triage   | `ln-consult`  | Direction needs reassessment                      |

Recommended: **1** (then **2** after planning, or **2** now if verification is the pressing concern)

---
*Adapted from [mattpocock/skills/write-a-prd](https://github.com/mattpocock/skills/tree/main/write-a-prd).*
