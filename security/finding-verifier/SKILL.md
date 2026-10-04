---
name: finding-verifier
description: "Independently verify a suspected Ouros security finding. Use after another agent reports a vulnerability or suspicious behavior, before severity is finalized, an issue is opened, or a fix is proposed as security-critical."
---

# Finding Verifier

Assume the candidate finding may be wrong. Disprove it first; confirm it only if evidence survives independent checking.

## Inputs

Require enough information to identify affected component, claimed security boundary, prerequisites, and candidate reproduction/evidence.

If runtime reproduction is needed, use `../safe-runtime-testing/SKILL.md`.

## Verification procedure

1. **State the claim narrowly.** Convert broad language into one falsifiable sentence.
2. **Check the boundary.** Identify what should be prevented and where enforcement is expected.
3. **Inspect code/config independently.** Do not rely on the original agent's interpretation.
4. **Try to falsify.** Look for upstream/downstream checks, fixtures, mocks, environment-only shortcuts, or expected behavior.
5. **Reproduce minimally when authorized.** Use independent inputs or a fresh fixture.
6. **Classify.**

Use `confirmed` when a boundary violation is reproduced or deterministically demonstrated; `rejected` for expected behavior/test artifacts; `blocked` when scope/access is insufficient.

## Severity discipline

Base severity on privileges required, reachable data/actions, cross-user/tenant reach, repeatability, user interaction, blast radius, and compensating controls. If impact is uncertain, say so.

## Confirmed finding format

Include: `ID`, `status`, `component`, `boundary`, `prerequisites`, `minimal_reproduction`, `expected`, `observed`, `impact`, `root_cause`, `severity_rationale`, `evidence`, `cleanup`, `regression_test`, and `remediation_direction`.

Redact secrets and unnecessary personal data. Do not silently fix the bug before preserving sufficient evidence.
