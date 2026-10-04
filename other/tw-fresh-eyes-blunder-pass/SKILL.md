---
name: tw-fresh-eyes-blunder-pass
description: Run a targeted fresh-eyes blunder pass over code, specs, plans, reviews, closure gates, or skill edits. Use when asked to reread with fresh eyes, find obvious bugs, catch mistakes/oversights/omissions, check for embarrassing misses, or do a second independent pass before closure. Use it as the final falsification/check pass for another workflow, not as a substitute for implementation or verification.
---

# Fresh-Eyes Blunder Pass

A reusable second-pass falsifier. Reread the current artifact set as if another agent produced it, treating prior confidence as untrusted. The goal is to catch what your own momentum hid.

## Modes

- `implementation`: new code, modified code, neighboring unchanged code, tests, imports, callsites, invariants.
- `closure`: handoff packet, closure gates, verification evidence, readiness claim, reopen trigger.
- `review`: findings, severity, direction, mutation approval, handoff agenda.
- `spec`: authoritative brief, evidence, decision packet, proof bar, rollback, non-goals, requirement-to-test traceability.
- `plan`: convergence claim, owners, dates, rollback, requirements, proof, scope, execution order.
- `skill-edit`: trigger description, boundaries, validation requirements, stale paths, duplicate sections, false/missed activation.

## Universal prompt

> Carefully reread the artifact set with fresh eyes, looking for blunders, mistakes, errors, oversights, omissions, misconceptions, bugs, confusion, stale assumptions, scope creep, missing proof, and anything that would be embarrassing if it reached the user unchanged.

## Method

1. Pick the mode and name the exact artifacts in scope.
2. Reread each surface cold — do not trust comments, prior summaries, or your earlier reasoning.
3. For every suspected issue, attach concrete evidence (a file:line, a counterexample, a contradicted claim). Discard hunches with no anchor.
4. If the pass changes the artifact, rerun the narrowest credible verification owned by the parent workflow.
5. If nothing material is found, report `material_delta: no` rather than inventing low-value findings.

## Required result

```yaml
fresh_eyes_pass:
  mode: implementation | closure | review | spec | plan | skill-edit
  artifact_state: "..."           # branch/head/diff or file set inspected
  checked_surfaces: []
  material_delta: yes | no
  findings: []                    # each with evidence anchor
  fixes_or_required_updates: []
  verification_to_rerun: []
  fresh_eyes_delta: "none | summary"
```

## Guardrails

- This is a check pass, not an implementation, review-adjudication, or verification pass — it sharpens those, it does not replace them.
- Do not manufacture findings to look thorough. "No material issue" is a valid, valuable result.
- Every finding must survive its own evidence check before you report it.
