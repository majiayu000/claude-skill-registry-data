---
name: receipt
description: Verify that a requested bug fix changes observable behavior with a failing-before, passing-after reproduction and honest execution evidence.
---

# Receipt

> You fixed it? Show me the receipt.

Reuse supplied guidance; discover missing instructions only within authorized roots, never through an out-of-scope ancestor sweep. Report inaccessible evidence instead of broadening access.

For a current bug, select a regression on the actual affected path using the documented runner. Reuse valid before evidence; otherwise observe the defect-specific failure, implement the requested fix, then rerun unchanged assertions/inputs. Preserve neighboring behavior and required coverage. Inspect history only for unresolved behavior or implementation.

For an already-present fix, committed or not, requiring historical comparison, use the [isolated comparison procedure](references/existing-fix.md). Don't reverse patches in the user's working tree.

A required suite running that regression with matching inputs/runtime supplies after evidence; don't repeat it separately. Skipped, undiscovered or differently configured tests don't qualify. Changed relevant inputs invalidate reused results.

Batch final checks in one shell call, adapting the runner and paths:

```sh
python3 -B -m unittest -v && git diff --check -- app.py test_app.py && git diff -- app.py test_app.py
```

`&&` leaves later checks unrun after failure. If all must run, retain each exit explicitly, not just the shell's final status. Review untracked files separately; `git diff` omits them.

Setup failures aren't defect reproduction; mocks don't prove unobserved effects. Preserve user changes and scope; verification alone authorizes neither implementation nor publication.

Report the reviewed change, decisive before/after observations and commands, applicable revision identities and limits. Stop when the requested outcome and required checks are verified; no separate dossier or unrelated green checks.
