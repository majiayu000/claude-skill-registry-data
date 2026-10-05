---
name: flow-verify
description: Adversarially verify an implementation against its objective, acceptance criteria, definition of done, and prohibitions using fresh evidence. Use for completion gates, release readiness, or independent verification after implementation and review.
---

# Verify completion adversarially

Read [workflow](../../references/workflow.md), [artifacts](../../references/artifacts.md), and [safety](../../references/safety.md) before verification.

The goal is to refute completion, not confirm the implementation narrative. Treat summaries and prior test claims as untrusted until reproduced.

## Inputs

Resolve, in order:

1. objective;
2. acceptance criteria;
3. definition of done;
4. prohibitions and safety constraints;
5. changed files and implementation evidence;
6. prior review findings.

If no verifiable contract exists, return `BLOCKED` and list the missing truths. Do not invent acceptance criteria after implementation.

## Procedure

1. Convert every contract statement into an independently testable truth.
2. For each truth, choose the command, inspection, or counterexample most likely to disprove it.
3. Run fresh verification and record the exact result; do not rely on earlier output.
4. Inspect the final diff for scope violations and prohibited behavior.
5. Reconcile unresolved review findings with the truth list.
6. Calculate passed truths and identify critical failures.
7. When rejected, write bounded correction tasks only if artifact persistence is authorized.

## Verdicts

- `APPROVED`: every truth passes and no prohibition is violated.
- `WITH_CAVEATS`: all critical truths pass; only explicitly low-impact caveats remain.
- `REJECTED`: any critical truth fails, a prohibition is violated, or required evidence contradicts completion.
- `BLOCKED`: verification cannot run or the contract is absent.

Never weaken a failing criterion to obtain approval.

## Output

Return a truth table with `Truth`, `Refutation attempt`, `Evidence`, and `Result`, followed by the verdict and correction paths. Persist the verification report only when the user requested it or an active Flow phase already authorizes artifacts.
