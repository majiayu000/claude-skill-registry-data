---
name: cursor-no-comments
description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
---

## Codex runtime mapping

For Step 1, call native `collaboration.spawn_agent` with `agent_type: "comment-sicko"` when that exact type is exposed. The named profile is distributed by `model-capability-router`; never substitute a generic reviewer or a prompt that merely says to act as Comment Sicko. If the type is unavailable, report the gap and leave this run incomplete. Pass the exact scope and assign writable files explicitly; the coordinator checks the report and diff, performs accepted in-scope implementation fixes under the caller's authorization, and runs verification. Only the optional constraint encoding waits for the approval required by upstream Step 5. Follow `model-capability-router`; the reviewer is not authority. Use `cursor-how`, `cursor-why`, and `cursor-architect` by their adapted names when the workflow requires them. The profile asset must be installed explicitly before a fresh Codex session can select it. Do not install Cursor hooks. Automatic selection and the complex rejection/rerun branches remain unproven.

# No comments

Spawn Comment Sicko. Act on accepted findings.

Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Call `collaboration.spawn_agent` with `agent_type: "comment-sicko"`, an exact scoped brief, and explicit writable-file ownership. Do not substitute a generic agent type or copy the role into the prompt. If the named type is unavailable, report that gap. The coordinator inspects the reviewer diff and owns accepted implementation fixes.
2. Inspect its report and diff. Reject application-code edits, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat kept intentional code as guilty. Reshape flags on our-code surprises stay actionable. Do not restore those comments. A keep survives only with proof it is about something we cannot change. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions stay actionable `MUST KILL`s. Restore deletions only with exact exceptions and scoped proof. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, run `cursor-how` or `cursor-why` on their symbol. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun one rejected report with the failure named. Reject a second, report it open, and fail `/no-comments`.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `cursor-architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only. Neither authorizes widening the fence nor fixing instances outside it. Never bolt on symptom guards.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Wait for interactive approval. Unattended and eval require caller pre-approval. If approved, encode then delete. Otherwise delete, report the constraint open, and sketch out-of-scope work.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
