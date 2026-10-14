---
name: implement
description: "When implementation intent is clear — deliver the authorized outcome with a small correct diff, meaningful tests, and an uncommitted verification handoff."
---

# Implement

Deliver the approved behavior, not a larger interpretation of it. A clear bounded
request or a ready approved task supplies intent; no extra interview is needed.

- Read the actual flow, callers, contracts and relevant tests before choosing a
  fix. Reuse existing code, the standard library or native host behavior before
  adding machinery. Minimize the correct change, not merely the changed lines.
- Preserve user work, staged changes and unrelated behavior. Change only the files
  you were authorized to change, whether the task came from the user or a parent
  agent; that includes temporary probes and their cleanup. Ask before crossing
  that boundary, changing a contract or deciding a material ambiguity.
- If reality contradicts the approved intent, stop and explain; `design` owns
  renewed approval. Retry only with new evidence, a corrected task or a changed
  hypothesis; an unchanged retry is not progress. A failed delegated task stays
  failed rather than silently becoming yours.
- Leave regression evidence for nontrivial behavior. Prefer a failing
  reproduction before a bug fix; take expected results from the contract or an
  independent worked example, not from the implementation. [TDD](references/TDD.md)
  gives the detailed discipline.
- Run the applicable checks and the original scenario. Separate what actually ran
  from inspection, fixtures and unrun manual or host checks. A missing environment
  is a verification gap, not permission to treat a substitute as equivalent.
- Update current docs whose claims changed, within the authorized scope.

Deliver: outcome, complete changed-file list, commands and results, known gaps or
blockers. Leave the change uncommitted for fresh independent review; passing local
tests does not complete the requirements or grant commit, cleanup, deployment or
publication authority.
