---
name: gate-discipline-diagnose
description: Diagnoses a failing CI gate, lint, or audit and fixes the artefact rather than weakening the gate. Use when a gate fails. Use when tempted to bypass a check with --no-verify, blanket suppression, severity-threshold lowering, or exemption-list addition. Use when a pre-commit hook blocks a commit. Use when a required status check on a PR shows red.
derives_from: ../../governance/gate-discipline.md
---

# Gate Discipline: Diagnose, Then Fix the Artefact

## Overview

A failing gate is signal, not noise. The artefact is what needs fixing, not the gate. This skill walks through the correct-response hierarchy from the canonical rule [`governance/gate-discipline.md`](../../governance/gate-discipline.md) when a gate fails, named to make the reflex "diagnose, then act" rather than "silence, then proceed".

The rule is the source of truth for normative content (the full enumeration of prohibited responses, tool-specific anti-pattern examples, the exception-handling protocol, the framework-alignment table). This skill is the workflow wrapper: the diagnose-then-act sequence applied to a gate failure.

## When to Use

- A CI gate, lint, type check, test suite, or audit failed during the current task.
- A pre-commit hook blocked a commit you are trying to make.
- A required status check on a PR is showing red and you are deciding how to respond.
- A generator-output `--check` reports drift between the source and the committed artefact.
- You are tempted to use `--no-verify`, a blanket suppression directive, `|| true`, severity-threshold lowering, or exemption-list addition to make a gate pass.
- A reviewer suggests adding the failing file to an exemption list as a drive-by fix.

## Process

The correct-response hierarchy from the canonical rule, executed in order of preference:

1. **Read the failure output.** Do not act before reading the gate's actual finding. The output names the artefact and the rule it violated. Resist the urge to start typing the workaround before you understand what the gate is reporting.
2. **Fix the artefact.** Almost always the right answer. The gate exists because the defect class matters; the defect class is present in this artefact; fix it. The cost of the fix accrues to the team that introduced it; the cost of letting one defect through accrues to every future reader of the artefact.
3. **If the gate is genuinely wrong** (false positive, stale rule, environmental fluke), fix the gate. Document the rationale in the same commit. Treat the gate-fix as a substantive change subject to the same review discipline as any code change. A gate that is wrong today may be right tomorrow; weakening it has compounding cost.
4. **If the artefact and gate are both correct but the fix is impractical in this PR** (cross-team coordination, vendor patch outstanding, tooling limitation), file a tracked issue with a remediation deadline and document a temporary exception per the project's exception register. The exception is temporary by construction; renewal requires re-approval.
5. **If the failure is environmental** (CI runner OOM, network flake, transient dependency outage), re-run. If the flake recurs, document it so the gate can be hardened (e.g., retry logic; idempotency check; deterministic seed). Do not normalize re-running as a strategy.

The first question on a failure is "what does it mean?", not "how do I make it go away?".

## Red Flags

These responses must never substitute for a real fix without an explicit, documented exception:

- `git commit --no-verify` to bypass pre-commit hooks.
- Force-pushing past a failing required check.
- Lowering a severity threshold to silence a finding (fail-on-High becomes fail-on-Critical only).
- Adding the failing file or rule to an exemption list as a drive-by fix.
- Deleting failing test cases instead of investigating.
- Blanket suppression directives (`# noqa`, `// eslint-disable`, `// @ts-nocheck`, `# type: ignore`, `# nosec`, `pragma: no cover`) without a documented rationale on the same line.
- Replacing an assertion with a log statement so the pipeline keeps running.
- Marking a required CI job non-required to dodge branch protection.
- Wrapping a check in `|| true`, `set +e`, removing `set -e`, or `try / except: pass`.
- Re-running CI repeatedly until it passes by coincidence (intermittent failure is signal of a race condition or timing dependency; diagnose it).
- Regenerating a checked artefact in CI itself to bypass the generator-drift check (defeats the check by construction).

## Verification

The gate-discipline response is verified when:

- The failure output has been read and the underlying rule named in your reasoning.
- The artefact has been fixed (or the gate fix is documented with rationale in the same commit), and the same gate now passes when re-run standalone.
- No suppression, threshold lowering, or exemption-list addition was used as the resolution.
- If an exception was the chosen path, the exception is recorded with approver, scope, deadline, and a link to the tracked issue for remediation.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It is just one finding; let me suppress it and move on." | The finding is what the gate is for. Suppressing it without addressing the underlying issue normalizes the bypass and lets the defect class leak into future changes. |
| "The gate is too strict for this case." | If the gate is genuinely wrong, fix the gate as its own substantive change. Drive-by exemptions hollow out the audit programme. |
| "I will fix it properly in a follow-up PR." | The exception register is the documented channel for that posture. Verbal "I will fix it later" is not. |
| "Re-running the CI fixed it last time." | Intermittent failure is a race condition or timing dependency; left undiagnosed, it will fail when stakes are higher. |

## See Also

- Canonical rule [`governance/gate-discipline.md`](../../governance/gate-discipline.md): framework alignment (OWASP ASVS V15.1 / V15; NIST SSDF PW.7.2 / PO.4.1; CSA CCM CCC-01 to 04 / GRC-04 / GRC-05; ISO 27001 Annex A.5.4 / A.5.36 / A.8.28), tool-specific anti-pattern examples for git / lint / type check / test suite / CI-CD config / generator-output drift, and the exception-handling protocol that the project's exception register implements.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): verify the fix actually closed the underlying defect before claiming the gate is back to green.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): when a gate failure exposes an ambiguity (e.g., the gate is reporting a defect in a way that suggests two interpretations), use clarify-before-acting before picking a response.
- Related skill [`validation-sweep`](../validation-sweep/SKILL.md): after this skill diagnoses and fixes a gate failure, run the sweep to verify the fix did not surface a sibling failure elsewhere in the project's in-scope artefacts.
