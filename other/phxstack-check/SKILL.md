---
name: phxstack-check
description: Check whether an implementation works, matches its local spec, and remains simple. Use when implementation is complete and before it is pushed.
---

# phxstack-check

Inspect the actual change and answer three questions with evidence. Report;
do not fix.

1. **Does it work?** Run the relevant checks. For Elixir work, use the
   applicable `phxstack-elixir` references and `reference/verify.md`; for UI,
   inspect the browser behaviour when available.
2. **Does it match the spec?** Compare the diff to the approved local spec.
   Name missing, partial, or unplanned work.
3. **Is it simple?** Identify only meaningful complexity; do not nitpick or
   redesign.

If no local spec exists, state that the second question cannot be proven.
Classify each finding as `BLOCKING` or `NON-BLOCKING`. Every blocking finding
must include location, problem, impact, and smallest correct fix.

Finish with exactly one verdict: `PASS` or `FAIL`. Inconclusive verification
is `FAIL`.
