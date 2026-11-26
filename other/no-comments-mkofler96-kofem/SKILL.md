---
name: no-comments
description: "Spawn Comment Sicko on a diff or files, act on its accepted findings, and offer lint or type encodings for claimed constraints. Use for /no-comments, or before review."
disable-model-invocation: true
---

# No comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, `develop`, including the working tree.

## Steps

1. Spawn a general subagent (`Agent` with `subagent_type: general-purpose` in Claude Code, `spawn_agent` in Codex). Its prompt is [`references/comment-sicko.md`](references/comment-sicko.md) verbatim, then the scope. Do not restate its rules. If your harness has no subagent tool, run that prompt yourself in a fresh pass over the scope.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, trace their symbol with `git log -S` or `git blame`, and read the Linear issue its `KOF-nn` tag names. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it, except a `REVIEW` keep about an outside rule, which stays until someone checks that rule. Report it open. Revert and rerun one rejected report with the failure named. If you reject the rerun too, revert only its rejected findings, report them open, and go on with the accepted ones.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run the **architect** skill once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** skill guides intent only. It does not authorize widening the fence or fixing instances outside it. Never bolt on symptom guards. A fix that changes behaviour starts with a failing test (`AGENTS.md`, Test-driven development).
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended runs require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, `REVIEW` keeps, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
