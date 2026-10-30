---
name: ponytail
description: >-
  Main coding-route simplicity method: understand the requested outcome,
  question unnecessary work, prefer fitting existing tools/code and standard
  facilities, then build the smallest clear complete solution. Use for coding,
  repair, refactoring and dependency choices, especially over-engineering or
  an explicit ponytail request. Simplicity must preserve capabilities,
  correctness, verification and the owner's confirmed scope.
argument-hint: "[lite|full|ultra]"
license: MIT
---

# Ponytail — less machinery, the whole result

Ponytail is part of the main working route, not an optional personality to become.
It means reducing needless work and maintenance while delivering the requested
working thing. It is not permission to skip understanding, cut the product down
silently or stop at the smallest demo.

## Understand before simplifying

Read the actual task, relevant code/callers, constraints and acceptance criteria.
Distinguish necessary complexity from speculative scaffolding. Before substantial
work ask: does it need to exist, and does an existing maintained solution already
cover it? Do not repeat a ladder report before each edit or each function.

If the premise is bad, explain the evidence and a concrete alternative. Discuss
material product/scope changes before substituting a smaller outcome. Ordinary
implementation choices are yours to make and verify.

## Choose the simplest fitting solution

- Reuse or extend maintained project code and dependencies where they fit.
- Prefer standard/native facilities when their behavior, compatibility and
  lifecycle satisfy the contract. Existing libraries may be safer than a custom
  "few lines" implementation, especially for crypto, parsing and protocols.
- Evaluate maintained external tools before reinventing substantial infrastructure.
  Compare actual fit and integration burden; popularity or feature overlap alone
  is not a reason to abandon the assigned task.
- Add abstractions for real concepts, trust boundaries or dependency seams, not
  hypothetical growth. A single consumer does not automatically make a useful
  boundary wrong; two similar call sites do not automatically deserve one helper.
- Choose clear code over compressed one-liners. The fewest lines/files is not the
  acceptance criterion; the smallest coherent change that meets the task is.

Fix the cause in the right place. Inspect affected callers and preserve their
contracts rather than adding a guard to every symptom or moving complexity around.
A behavior-preserving simplification should reduce actual friction, not just a count.

## Make trade-offs visible

For a real deliberate limitation, record the reason, present ceiling and condition
for revisiting it in the project's convention. A `ponytail:` comment is useful
when it explains something non-obvious, not as a stamp on every shortcut.

```python
# ponytail: one shared lock is sufficient for current throughput;
# revisit if measured contention becomes load-bearing.
```

Do not mark speculative future work or narrate obvious code. Measured claims need
measurements; a complexity score or estimated savings is not proof.

## Preserve what matters

Never simplify away required behavior, input validation at trust boundaries,
data integrity, error handling that prevents loss, security, accessibility or
observable failures. Hardware and external systems need real calibration,
timeouts and lifecycle handling even when the minimal paper model does not.
Removal uses the workspace's data-preservation/trash route; "less code" is not
permission to discard existing work.

Verification is part of the solution. Use the project's existing framework,
fixtures and appropriate tests, not a forced one-assertion self-check. Exercise
the actual usage interface and risk-relevant cases; follow testing-discipline
and verification-before-completion. A tiny diff can still break a critical path.

## Intensity shorthand, not authority modes

If the owner uses these names, interpret them as emphasis:

| Level | Emphasis |
|---|---|
| `lite` | Explain a worthwhile simpler alternative alongside the assigned implementation |
| `full` | Default: actively remove unnecessary machinery while meeting the complete contract |
| `ultra` | Challenge expensive/speculative design choices more strongly; do not cut confirmed scope without discussion |

There is no hidden persistent mode, required slash-command tool or change of
permissions. These labels never weaken safety or verification and never mandate
terse output where the owner needs a reasoned discussion.

## Result

Deliver the working outcome, explain meaningful simplifications and their limits,
and report actual checks. Keep explanations proportionate to the task, not capped
at three lines. Continue agreed unfinished work; efficiency is less wasted work,
not premature closure.
