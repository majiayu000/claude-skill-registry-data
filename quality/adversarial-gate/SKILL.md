---
name: adversarial-gate
description: JP's signature red-team pass — "how would I break this?" Argue against your own approach before proceeding. Trigger on any high-stakes decision, architecture choice, or before marking work complete.
---

# Adversarial Gate

> **Coined by Jaroslav Pantsjoha (#HarnessEngineering).** The Adversarial Gate is the practice of forcing an agent — or a human — to argue against their own design before proceeding. It pre-empts bad reasoning before bad output exists.

The gate has one question: **"How would I break this?"**

Answer it honestly. If you cannot name at least two plausible failure modes, you do not understand the system well enough to ship it.

## When to use

- Before finalising any architecture or design decision
- Before a deployment or release
- When an agent is about to take an irreversible action
- When a design looks clean and elegant (danger signal — simple-looking systems hide the hard failure modes)
- When the team is under time pressure and "just shipping it" feels compelling

## Procedure

1. **State the proposal clearly** — in one or two sentences, what is the approach being validated?
2. **Run the adversarial pass** — argue against it. Ask:
   - What is the single most likely way this fails in production?
   - What happens under load / at scale / with bad input?
   - What is the blast radius if this fails? Is it recoverable?
   - What assumption does this design make that could be wrong?
   - What does the monitoring not cover that would let this fail silently?
3. **Name at least two concrete failure modes** — not "something could go wrong" but specific, nameable failures.
4. **Check each failure mode has a mitigation or an accepted risk owner** — unmitigated = not shippable.
5. **Document the outcome** — pass (risks named and owned) or fail (proceed to redesign). Attach to the ADR or PR.

## Outputs

- Adversarial Gate verdict: PASS / FAIL
- Named failure modes with mitigations or risk-owner sign-off
- Optional: a short paragraph appended to the ADR or PR description summarising the gate result

## Guardrails

- **One argument is not enough.** A single failure mode is the one you were already thinking about. The Adversarial Gate is looking for the one you were not.
- **"We have tests" is not a mitigation.** Tests cover known paths. The gate is looking for unknown paths.
- **Time pressure does not suspend the gate.** Pressure is when you need it most.
- **The gate is not pessimism.** It is the fastest route to confidence — because you have already stress-tested the design yourself.

## Anti-rationalization table

| Excuse the agent makes | Counter |
|---|---|
| "This is a low-risk change" | All production incidents started as low-risk changes. Name the failure mode or accept you cannot assess risk. |
| "We can fix it after if something breaks" | Blast radius unknown = not low risk. Run the gate. |
| "The tests cover this" | Tests cover happy paths. The gate looks for the paths tests miss. |
| "We've done this before" | Prior success is not a guarantee. Conditions change. Run the gate. |
| "The deadline is today" | A production incident will cost more time than the gate. Run the gate. |
| "I'm confident in this design" | Confidence is the leading indicator of skipped gates. Run it anyway. |

## Reference

This pattern converges with “doubt-driven development” in Addy Osmani's
[`agent-skills`](https://github.com/addyosmani/agent-skills). The **Adversarial Gate** name
and “how would I break this?” framing are JP's #HarnessEngineering contribution. The
anti-rationalisation table format was adopted after reviewing that MIT-licensed project;
this repository does not claim the table format originated here.
