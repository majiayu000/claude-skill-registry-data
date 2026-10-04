---
name: xsq-code-review
description: Thermo-nuclear review of the squad's work product — security/correctness and code-quality reviewer subagents run in parallel over the scoped diff, findings synthesized and prioritized, then fixed by implementer subagents and re-verified until clean. Use for /xSq-code-review, /xsq-code-review, "run the deep code review", "review the squad's work".
---

# /xSq-code-review

This is the deep-review command of the **xSquad** skill. The orchestrator runs it
automatically when every task is verified green; it also runs standalone on any branch.
This file lives inside the xSquad package (its root holds `SKILL.md`, `commands/`,
`agents/`, `references/`).

Read `commands/code-review.md` from the package root — two levels up from this file
(`<package>/commands/code-review.md`) — and follow that procedure exactly: scope the
diff, launch both reviewer subagents in parallel with the rubrics from the package's
`agents/reviewer-security.md` and `agents/reviewer-quality.md`, synthesize deduplicated
prioritized findings, dispatch footprint-disjoint fix briefs to implementer subagents,
re-run validators, and loop until clean or explicitly accepted.

If the package cannot be located from this file's own path, ask the user for the xSquad
package path; do not improvise the procedure.