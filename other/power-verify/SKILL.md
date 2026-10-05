---
name: power-verify
description: Use when about to claim work is complete, fixed, or passing, and when a finished feature needs adversarial verification before integration
---

# Evidence Before Claims

Read [collaboration](../../references/collaboration.md) when dispatching the `verifier` — its
status is at most ten lines and its report is never pasted into your context — and
[artifacts](../../references/artifacts.md) before writing `verdict.md` or `state.md`.

## Route

- no argument, mid-work: the gate below, then continue
- `<feature-slug>`: full adversarial verification, ending in a verdict
- `--strict`: two verifier lenses in parallel; the verdict is the worse of the two

## The gate

Before any claim that something works, fixed, passes, or is done:

1. **Identify** the command that would prove it. `.planning/power/context/project.md` records
   this repository's real test, lint and build commands; use those rather than the ones that are
   conventional for the ecosystem.
2. **Run** it, fresh and complete. Not a cached result, not a subset.
3. **Read** the whole output: the exit code, the failure count, the warnings.
4. **Verify** the output actually says what you are about to claim.
5. Only then, claim it.

Skipping a step is not verifying faster; it is asserting.

| Claim | Requires | Not sufficient |
|---|---|---|
| "Tests pass" | the full suite run now, output read | the last run, before your change |
| "It builds" | the real build command | the linter passed |
| "The bug is fixed" | the regression test failing before and passing after | the symptom is gone |
| "Nothing else broke" | the full suite | the touched file's tests |
| "The agent did it" | the VCS diff | the agent said `DONE` |

**No satisfaction before evidence.** Not "Great!", not "Perfect!", not "That should do it".
Those phrases commit you to a conclusion you have not yet checked, and having committed, you
will read the output looking for agreement.

## Adversarial verification

When verifying a whole feature, dispatch the `verifier` subagent. Its instruction is not
"check whether this is complete" — it is **"try to refute that this is complete"**.

Give it the spec, the plan, the ledger, and the branch range. It falsifies each stated truth —
objective, acceptance criteria, definition of done, prohibitions — with real commands, and
reports what survived.

`--strict` runs two lenses in parallel:

- **Functional**: does it do what the spec says, under the spec's exact values?
- **Compliance**: does it respect the prohibitions, conventions and non-functional constraints?

The final verdict is the worse of the two. A feature that works but violates a stated
prohibition is not approved.

## Verdicts

| Verdict | Meaning | Next |
|---|---|---|
| `APPROVED` | Every stated truth survived refutation. | `pwdev-power:power-finish` |
| `CAVEATS` | Approved, with findings recorded that nothing blocks on. | `pwdev-power:power-finish`, caveats surfaced |
| `REJECTED` | At least one stated truth was falsified. | fix plan, then re-verify |

Write the verdict to `.planning/power/features/<slug>/verdict.md` with the evidence — the
commands run and their output — and record the gate in `state.md`.

## Correction cap

A `REJECTED` verdict produces `fix-<NN>.md`, executed through `pwdev-power:power-execute`. At
most **two** correction cycles. A third rejection stops and goes to the human; it never becomes
an approval by attrition.
