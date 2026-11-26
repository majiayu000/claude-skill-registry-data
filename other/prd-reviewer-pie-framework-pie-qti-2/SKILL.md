---
name: prd-reviewer
description: Review an existing PRD for completeness, accuracy, and staleness. Use when the user asks to "review a PRD", "check if a PRD is up to date", "validate a PRD", or when opening a PR that touches a package covered by a PRD. Checks that the PRD accurately reflects the current implementation, that acceptance criteria are testable, that spec alignment is correct, and that rationale sections contain real context rather than code paraphrase.
---

# PRD Reviewer

You are reviewing a Product Requirements Document (PRD) for the PIE-QTI framework. Your job is to find problems that matter — not style nits.

## What you're checking for

### 1. Accuracy against current implementation

Read the source for the package(s) listed in the PRD. Compare against what the PRD claims.

Check:
- Do the listed supported/omitted attributes match what the code actually handles?
- Do the acceptance criteria match the real behavior (not an idealized version)?
- Are extension points documented at the right level of abstraction — i.e., do they reflect the actual interface contracts in the code?
- Are any design decisions documented that have since been reversed or changed?

Flag as **[STALE]** anything that no longer matches the code.

### 2. Spec alignment correctness

For interaction and architecture PRDs, verify QTI spec claims using the `qti-domain-expert` skill when needed.

Check:
- Are supported/omitted attributes listed accurately against QTI 2.2 (and 3.0 if applicable)?
- Are any documented divergences from spec actually divergences, or are they correct spec-compliant behavior?
- Are variable names (baseType, cardinality, response identifiers) correct?

Flag as **[SPEC-ERROR]** anything that misrepresents the QTI spec.

### 3. Acceptance criteria quality

Each AC should be self-contained and unambiguously testable. Apply this bar: could a QA engineer who has never seen this codebase verify the criterion using only the PRD and the demo app?

Reject criteria that:
- Reference internal state not visible through the UI or browser DevTools
- Describe implementation rather than observable behavior ("the component calls X method" is not an AC)
- Are too vague to have a clear pass/fail ("the interaction feels responsive" fails the bar)
- Are missing important edge cases that are called out in the Background section or known from the spec

Flag as **[WEAK-AC]** with a suggested rewrite.

### 4. Rationale completeness

The Background and Design Decisions sections should contain real constraints, not code paraphrase. "We used a registry because it's extensible" is not rationale. "We used a priority-based registry because vendor-supplied components must be able to override default components for specific interaction types without modifying framework code" is rationale.

Flag as **[THIN-RATIONALE]** when a section just restates what the code does without explaining why.

### 5. Missing coverage

Check whether the PRD covers the full scope of what its title implies.

For **interaction PRDs**: Are all QTI attributes (at minimum the ones in the spec's normative table) addressed? Are accessibility requirements for this specific interaction type present?

For **architecture PRDs**: Are all public extension points documented? Are cross-subsystem contracts (what this package expects from its callers, what it guarantees to its consumers) covered?

For **system PRDs**: Are all packages that participate in this cross-cutting concern mentioned?

Flag as **[MISSING]** with a description of what's absent.

### 6. Open questions hygiene

Open questions that have been resolved in the code but not removed from the PRD should be flagged as **[STALE-QUESTION]**.

---

## Output format

Report findings grouped by severity:

**Critical** — PRD is misleading or incorrect (STALE, SPEC-ERROR): must fix before merging.
**Important** — PRD is incomplete in a way that matters (MISSING, WEAK-AC): should fix before merging.
**Minor** — PRD could be better (THIN-RATIONALE, STALE-QUESTION): fix when convenient.

For each finding:
```
[SEVERITY] [TAG] Section: "..."
Issue: what's wrong
Fix: what to write instead (or what information to gather)
```

If the PRD passes review, say so explicitly and update its status in `docs/prds/INVENTORY.md` to `current` (or keep `needs-update` if you found issues).

---

## When to invoke this skill proactively

- When opening a PR that touches `packages/<name>` — check if a PRD exists for that package and flag if it needs updating.
- When a PR changes a public interface (type, registry, component API) — check the corresponding architecture PRD.
- When the user asks to write or update an AC or test — first check whether a PRD exists that should be the source of truth.

## Skills to use proactively

- **qti-domain-expert** — to verify spec claims in the QTI alignment section
- **pie-domain-expert** — when reviewing transform or PIE↔QTI boundary PRDs
- **accessibility-reviewer-assessments** — to validate completeness of accessibility AC sections
- **api-design-reviewer** — when the PRD covers a public extension API
