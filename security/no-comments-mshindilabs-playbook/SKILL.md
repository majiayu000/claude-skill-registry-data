---
name: no-comments
description: >
  Hunt and delete comments in code, fix the code that needed them, and offer to encode
  claimed constraints as types, tests or lint. Trigger on "remove the comments", "no
  comments", "clean up the comments in this diff", "this comment is a workaround
  apology". For wider code clean-up use the `deslop` skill.
license: MIT
metadata:
  upstream: cursor/plugins@d42aff08 pstack/skills/no-comments
---

# No comments

Run a fresh comment hunt and act on accepted findings.

Defer to the fresh perspective of the subagent, or of your own separate pass if you have no subagents.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Delegate to a subagent if your agent has them, with the contents of [references/comment-rules.md](references/comment-rules.md) pasted in as its brief (a subagent may not be able to open a skill-relative path) and the scope. Without subagents, apply those rules yourself as a separate pass before acting on any finding, and treat the result as the hunt's report.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, trace their symbol or run the `why` skill on it. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run the `architect` skill (or sketch two shapes yourself) once for the accepted set and surrounding code. Stop at the sketch. `architect` shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. Two principles guide intent only: fix the first place the system went wrong rather than where it surfaced ([fix-root-causes](../rigor-mode/principles/fix-root-causes.md)), and redesign as if the requirement had been foundational rather than bolting it on ([redesign-from-first-principles](../rigor-mode/principles/redesign-from-first-principles.md)); see them when `rigor-mode` is installed. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
