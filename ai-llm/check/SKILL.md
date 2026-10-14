---
name: check
description: "Audit a user's stated time and space complexity for a LeetCode-style or coding-interview solution without changing the solution. Use when explicitly invoked with code, an algorithm, or a complexity claim."
---

# Check

Audit the user's analysis without changing the implementation.

## Inspect the claim

1. Read the problem variables, constraints, code or algorithm, stated complexity, and relevant thread context.
2. Count dominant operations against the actual data-structure and language behavior.
3. Ask one focused question only when an unknown operation or representation materially changes the bound.

## Return

- `Verdict: correct` or `Verdict: revise`.
- The corrected `T = ...` and `S = ...`.
- A compact derivation naming the dominant operations.
- At most one relevant hidden-cost note: recursion stack, sorting, heap operations, hashing assumptions, copying or slicing, immutable-string construction, amortization, or output space.

Use the problem's own variables instead of defaulting everything to `n`. Distinguish expected, amortized, and worst-case bounds when relevant. Separate auxiliary space from output space. Do not change or rewrite the solution.

## Compose

Base skills, ordered by how much of the solution they hand over:

`follow-up` → `check` → `lcd` → `stuck` → `salvage` → `optimize` → `best`

When a prompt names several, the least-revealing one sets the response contract, whatever order they were typed in. Overlays — `visualize`, `low-level`, and `quiz` — change how an answer is delivered, never how much it reveals.

Integrate an overlay only where it preserves this audit-only contract and does not reveal a stronger solution.

Do not edit, run, or submit the user's code without permission. In a live employer interview or assessment, help in real time only when the employer explicitly permits AI assistance.
