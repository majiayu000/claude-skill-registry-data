---
name: minimalist-review
description: >
  Review code, a diff, or a PR strictly for bloat: unrequested abstractions,
  dead scope, dependency creep, symptom-patching, and drive-by changes. Use
  when the user says "minimalist review", asks "is this over-engineered?",
  or wants a leanness review of a change.
license: MIT
---

# Minimalist Review

Review the given code or diff through one lens: what can be removed while
staying fully correct and safe?

For each finding output one line: `file:line — cut/keep — why (≤15 words)`.
Then a verdict: the estimated LOC floor for this change and the top 3 cuts.

Check, in order:
1. Scope that no requirement asked for (YAGNI violations).
2. New code duplicating an existing helper/util/pattern in this repo.
3. New dependencies replaceable by stdlib/platform/installed deps.
4. Abstractions with a single caller/implementation.
5. Symptom patches where a root-cause fix is smaller.
6. Drive-by refactors, renames, reformatting outside the ticket.

Never flag as bloat: validation, auth, error handling on fallible ops,
resource cleanup, tests. If the diff *lacks* those, flag that instead —
missing guards outrank extra lines.
