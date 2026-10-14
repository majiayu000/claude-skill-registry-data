---
name: verify
description: "After a change, before commit/merge — independently review the complete candidate against user intent and standards, run real checks, and state the verdict."
---

# Verify

Judge the complete candidate, not the author's confidence or a convenient green.
The **candidate** is everything that would ship: the relevant committed range plus
staged, unstaged and untracked changes, or a named unchanged artifact when that is
the review scope. Tool success and a plausible diff are not acceptance.

Read-only review creates and changes no files, including temporary probes; cleanup
needs permission too. Report a blocked check or ask, rather than writing.

- Pin the candidate and the intent. A supplied ref must resolve. Files that were
  already dirty are still in scope, and so are callers the change affects.
  Preserve user work throughout.
- Derive acceptance from the user's requirements, not only the plan or tests.
  Trace every requirement to evidence, a user-approved deferral, or a blocker.
  Plans can omit requirements, and a reviewer cannot approve its own deferral.
  Resolve material scope or authority questions before passing.
- Keep **Spec** and **Standards** separate. Spec covers behavior, contracts,
  completeness, scope and acceptance. Standards covers repository rules,
  correctness, security, reliability and maintenance; find every repository file
  that documents how code should be written, and cite the rule a finding breaks.
  Use fresh independent reviewers when authorized and available; otherwise do
  separate passes yourself and say so. [SMELLS](references/SMELLS.md) lists contextual review leads.
- Read intent and tests, then trace implementation, callers, configuration and
  failure paths. Check what tests actually import and assert. Separate missing
  evidence from impossibility, and unclear scope from a proven scope violation.
  Include evidence or fixes added during the review. Before demanding a fix in a
  shared function, trace its callers: a correct shared function may need coverage,
  not another fix.
- Run meaningful checks within the allowed environment, and confirm their actual
  exit codes and output. Label each result as observed runtime behavior, fixture,
  static inspection or not run. Skipped cases, empty assertions and missing
  artifacts prove nothing; unrelated unit tests cannot stand in for required
  manual, host, model or integration evidence.

## Findings

- A required fix needs a concrete failing input or a violated requirement; give
  its location, trigger, impact and remedy. Uncertain intent is a question, not a
  violation.
- Report one defect once, not once per consequence. Small style preferences do not
  outweigh correctness. Recheck incoming claims instead of trusting them; a clean
  review is a valid result.
- Send required fixes to the writer, then review the changed candidate fresh.
  Return proposed documentation corrections to whoever may write them.

Return `VERDICT: PASS | PASS_WITH_RISKS | FAIL`, with separate Spec and Standards
findings, candidate and intent references, checks run, required fixes and residual
risks. Use **FAIL** for a required fix, a failed or unrun required check, a missing
requirement or an unresolved material decision. Use **PASS_WITH_RISKS** only for
explicitly non-blocking residuals; otherwise **PASS**. A limit, unavailable tool or
unfinished lane is never completion. A pass lets the unchanged candidate go to a
commit within explicit commit authority; it does not itself permit a commit, merge,
publication, deployment or cleanup.
